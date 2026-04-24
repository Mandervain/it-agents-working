# IT Helpdesk Agent Simulator

An AI-powered IT Helpdesk agent that reads unresolved tickets from simulated enterprise sources (Slack, Teams, Email, Service Desk), searches a local knowledge base, proposes solutions, updates ticket state, and generates a report.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| AI / LLM | Anthropic Claude Sonnet 4.6 via AWS Bedrock |
| Storage | Local JSON files + Markdown |
| Package manager | uv + requirements.txt |
| Frontend | Streamlit |
| Search | TF-IDF vector search (scikit-learn) |

---

## Running

```bash
# First time — create venv
uv venv .venv
uv pip install -r requirements.txt --python .venv/bin/python

# Authenticate (corporate SSO)
aws login --profile bootcamp

# Set env vars
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_PROFILE=bootcamp
export AWS_REGION=us-west-2

# CLI agent run
.venv/bin/python src/main.py

# Streamlit dashboard
.venv/bin/streamlit run src/dashboard.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

# Interactive chat
.venv/bin/python src/chat.py

# CLI with vector search (RAG)
USE_RAG=1 .venv/bin/python src/main.py
```

---

## Project Structure

```
├── data/                    ← read-only ticket sources (Slack, Teams, Email, Service Desk)
│   ├── slack/tickets.json
│   ├── teams/tickets.json
│   ├── email/tickets.json
│   └── service_desk/tickets.json
├── knowledge_base/          ← markdown troubleshooting articles
│   ├── vpn.md
│   ├── outlook.md
│   ├── printer.md
│   ├── laptop_slow.md
│   └── password_reset.md
├── state/                   ← runtime ticket state (gitignored)
├── output/                  ← generated reports (gitignored)
└── src/
    ├── main.py              ← orchestrator
    ├── ticket_loader.py     ← reads all data/ sources
    ├── state_manager.py     ← atomic read/write of ticket_state.json
    ├── kb_search.py         ← keyword search over knowledge_base/
    ├── kb_search_rag.py     ← TF-IDF vector search (USE_RAG=1)
    ├── agent.py             ← Bedrock / Anthropic API call, structured JSON output
    ├── sla_tracker.py       ← SLA calculation per priority
    ├── escalation_rules.py  ← auto-escalation rules (SLA breach, 24h stall)
    ├── report_writer.py     ← writes output/proposed_solutions.md
    ├── dashboard.py         ← Streamlit frontend
    └── chat.py              ← interactive multi-turn CLI chat
```

---

## Ticket Lifecycle

```
open → triaged → solution_proposed → waiting_for_user → resolved
                                                       → escalated
```

---

## SLA Rules

| Priority | SLA Limit | Auto-escalation trigger |
|----------|-----------|------------------------|
| high | 1 hour | SLA breached |
| medium | 4 hours | SLA breached |
| low | 8 hours | 24h stall |

---

## Key Conventions

- Ticket IDs follow `INC-NNNN` format.
- All ticket JSON must include: `id`, `source`, `user`, `priority`, `category`, `status`, `message`, `created_at`.
- Agent output is always structured JSON — never freeform prose from `agent.py`.
- State is persisted after every ticket (atomic write) — never batch at the end.
- `data/` is read-only — the guard hook blocks writes at the Claude Code level.
- One source of truth per ticket: `state/ticket_state.json` owns current status.

---

## Agent Rules

1. Use ticket data + knowledge base only — do not invent infrastructure details.
2. If confidence is low or no KB article matches → escalate, never guess.
3. Return structured JSON only — no prose, no markdown fences.
4. Never mark resolved without user confirmation.
5. Prefer the simplest troubleshooting steps first.

---

## What NOT to Do

- Do not write to `data/` — read-only source inputs.
- Do not add a database in the MVP.
- Do not inline the agent prompt in `main.py` — it lives in `agent.py`.
- Do not swallow exceptions in `state_manager.py` — corrupt state is worse than a crash.
- Do not gold-plate beyond task scope without confirming first.

---

## Claude-Specific Guidance

- Prefer editing existing files over creating new ones.
- Default to no comments — self-explanatory names only.
- Never skip hooks (`--no-verify`) or force-push without explicit instruction.
- Match response length to task complexity.
