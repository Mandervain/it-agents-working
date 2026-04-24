# IT Helpdesk Agent Simulator

An AI-powered IT Helpdesk agent that simulates enterprise support across Slack, Teams, Email, and Service Desk using local files. The agent scans open tickets, searches a knowledge base, enforces SLA rules, auto-escalates breached tickets, and proposes AI-generated solutions.

## Quick Start

```bash
# Create virtual environment
uv venv .venv
uv pip install -r requirements.txt --python .venv/bin/python

# Authenticate
aws login --profile bootcamp

# Run
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_PROFILE=bootcamp
export AWS_REGION=us-west-2

.venv/bin/python src/main.py
```

## All Run Modes

| Mode | Command |
|------|---------|
| CLI agent | `.venv/bin/python src/main.py` |
| CLI with vector search | `USE_RAG=1 .venv/bin/python src/main.py` |
| Streamlit dashboard | `.venv/bin/streamlit run src/dashboard.py --server.address 0.0.0.0 --server.port 8501 --server.headless true` |
| Interactive chat | `.venv/bin/python src/chat.py` |

## How It Works

1. Load tickets from `data/slack/`, `data/teams/`, `data/email/`, `data/service_desk/`
2. Calculate SLA per ticket (high=1h, medium=4h, low=8h)
3. Auto-escalate tickets with breached SLA — no API call needed
4. Search `knowledge_base/` for matching article (keyword or TF-IDF vector search)
5. Call Claude Sonnet 4.6 via AWS Bedrock → structured JSON solution
6. Update `state/ticket_state.json` atomically after each ticket
7. Write report to `output/proposed_solutions.md`

## Ticket Lifecycle

```
open → triaged → solution_proposed → waiting_for_user → resolved
                                                       → escalated
```

## Project Structure

```
├── data/               ← read-only ticket sources
├── knowledge_base/     ← markdown troubleshooting articles (vpn, outlook, printer, laptop, password)
├── state/              ← runtime ticket state (gitignored)
├── output/             ← generated reports (gitignored)
└── src/
    ├── main.py              ← orchestrator
    ├── agent.py             ← Bedrock/Anthropic API, dual backend
    ├── sla_tracker.py       ← SLA calculation
    ├── escalation_rules.py  ← auto-escalation logic
    ├── kb_search.py         ← keyword search
    ├── kb_search_rag.py     ← TF-IDF vector search
    ├── ticket_loader.py     ← multi-source ticket loader
    ├── state_manager.py     ← atomic state persistence
    ├── report_writer.py     ← markdown report generator
    ├── dashboard.py         ← Streamlit frontend
    └── chat.py              ← interactive chat simulation
```

## Backend Options

| Backend | Setup |
|---------|-------|
| AWS Bedrock (default) | `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials |
| Anthropic API | `ANTHROPIC_API_KEY=sk-ant-...` |

Model: `us.anthropic.claude-sonnet-4-6-20251001-v1:0` (Bedrock) / `claude-sonnet-4-6` (direct)
