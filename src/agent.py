import json
import os
import re

import anthropic

# Bedrock model ID for claude-sonnet-4-6 (cross-region inference profile)
MODEL_BEDROCK = "us.anthropic.claude-sonnet-4-6-20251001-v1:0"
# Direct Anthropic API model ID
MODEL_DIRECT = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are an IT Helpdesk AI agent. Your job is to analyze a support ticket and the provided knowledge base article, then return a structured JSON resolution plan.

Rules:
1. Use only the ticket data and knowledge base article provided — do not invent infrastructure details.
2. If confidence is low or the knowledge base article does not address the ticket — set status to "escalated".
3. Return structured JSON only — no prose, no markdown code fences, no explanation outside the JSON.
4. Do not mark any ticket as "resolved" — only propose solutions.
5. Prefer the simplest troubleshooting steps first.

Output format (return exactly this structure, nothing else):
{
  "ticket_id": "<id from ticket>",
  "category": "<category from ticket>",
  "confidence": "high | medium | low",
  "status": "solution_proposed | escalated",
  "proposed_solution": ["Step 1", "Step 2"],
  "next_action": "waiting_for_user_confirmation | escalate_to_human"
}"""

REQUIRED_KEYS = {"ticket_id", "category", "confidence", "status", "proposed_solution", "next_action"}


def _use_bedrock() -> bool:
    return os.environ.get("CLAUDE_CODE_USE_BEDROCK", "").strip() == "1"


def get_client() -> anthropic.Anthropic | anthropic.AnthropicBedrock:
    if _use_bedrock():
        region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        return anthropic.AnthropicBedrock(aws_region=region)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "No backend configured. Either:\n"
            "  Bedrock:  export CLAUDE_CODE_USE_BEDROCK=1  (+ AWS credentials)\n"
            "  Direct:   export ANTHROPIC_API_KEY=sk-ant-..."
        )
    return anthropic.Anthropic(api_key=api_key)


def _model() -> str:
    return MODEL_BEDROCK if _use_bedrock() else MODEL_DIRECT


def build_user_message(ticket: dict, kb_article: str | None) -> str:
    ticket_section = json.dumps(ticket, indent=2)
    kb_section = kb_article if kb_article else "NO KB ARTICLE FOUND — escalate this ticket."
    return f"## Ticket\n\n{ticket_section}\n\n## Knowledge Base Article\n\n{kb_section}"


def parse_agent_response(raw_text: str) -> dict:
    text = raw_text.strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
        result = json.loads(cleaned)

    missing = REQUIRED_KEYS - result.keys()
    if missing:
        raise ValueError(f"Agent response missing required keys: {missing}")

    return result


def call_agent(ticket: dict, kb_article: str | None) -> dict:
    client = get_client()
    response = client.messages.create(
        model=_model(),
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {"role": "user", "content": build_user_message(ticket, kb_article)}
        ],
    )
    raw_text = response.content[0].text
    return parse_agent_response(raw_text)
