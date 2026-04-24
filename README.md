# IT Helpdesk Agent Simulator

An AI-powered IT Helpdesk agent that simulates enterprise tools (Slack, Teams, Email, Service Desk) using local files. The agent scans unresolved tickets, searches a knowledge base, proposes solutions, and generates a report.

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py
```

## How It Works

1. Load tickets from `data/slack/`, `data/teams/`, `data/email/`, `data/service_desk/`
2. Filter tickets with `status = open`
3. Classify ticket category
4. Search `knowledge_base/` for matching articles
5. Generate structured solution via AI agent
6. Update `state/ticket_state.json`
7. Write report to `output/proposed_solutions.md`

## Ticket Lifecycle

```
open → triaged → solution_proposed → waiting_for_user → resolved
                                                       → escalated
```

## Project Structure

```
├── data/               ← read-only ticket sources (Slack, Teams, Email, Service Desk)
├── knowledge_base/     ← markdown troubleshooting articles
├── state/              ← current ticket state (written by agent)
├── output/             ← reports and resolved ticket log
└── src/                ← agent source code
```

## MVP Scope

- Local file-based, no external database
- Keyword-based KB search
- Markdown report output
- CLI execution

## Stretch Goals

- Streamlit dashboard
- Vector search (RAG)
- LLM integration (OpenAI / Ollama)
- SLA tracking
- Auto-escalation rules
