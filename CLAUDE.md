# IT Helpdesk Agent Simulator

An AI-powered IT Helpdesk agent that reads unresolved tickets from simulated enterprise sources (Slack, Teams, Email, Service Desk), searches a local knowledge base, proposes solutions, updates ticket state, and generates a report. Built as a hackathon MVP — local file-based, no external database.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| AI / LLM | Anthropic Claude API (stretch: Ollama) |
| Storage | Local JSON files + Markdown |
| Package manager | pip / requirements.txt |
| UI (stretch) | Streamlit |
| Search (stretch) | Vector search / RAG |

---

## Running Locally

```bash
# Create virtual environment (first time — system Python is PEP 668 restricted)
uv venv .venv
uv pip install anthropic --python .venv/bin/python

# Set API key and run
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python src/main.py
```

Required env var: `ANTHROPIC_API_KEY` — the agent prints a clear error and exits if missing.
No database, no external services required for the MVP. All data lives under `data/`, `knowledge_base/`, `state/`, and `output/`.

---

## Project Structure

```
helpdesk-agent-demo/
├── data/
│   ├── slack/tickets.json
│   ├── teams/tickets.json
│   ├── email/tickets.json
│   └── service_desk/tickets.json
├── knowledge_base/
│   ├── vpn.md
│   ├── password_reset.md
│   ├── outlook.md
│   ├── printer.md
│   └── laptop_slow.md
├── state/
│   └── ticket_state.json
├── output/
│   ├── proposed_solutions.md
│   └── resolved_tickets.json
├── src/
│   ├── main.py           ← entry point, orchestrates the agent loop
│   ├── ticket_loader.py  ← reads tickets from all data/ sources
│   ├── state_manager.py  ← reads/writes state/ticket_state.json
│   ├── kb_search.py      ← keyword search over knowledge_base/
│   ├── agent.py          ← Claude API call, returns structured JSON
│   └── report_writer.py  ← writes output/proposed_solutions.md
├── requirements.txt
└── README.md
```

---

## Ticket Lifecycle

```
open → triaged → solution_proposed → waiting_for_user → resolved
                                                       → escalated
```

Never mark a ticket `resolved` without explicit user confirmation. When confidence is low, set status to `escalated`.

---

## Key Conventions

- Ticket IDs follow the pattern `INC-NNNN` (e.g. `INC-1001`).
- All ticket JSON must include: `id`, `source`, `user`, `priority`, `category`, `status`, `message`, `created_at`.
- Agent output is always structured JSON — never freeform prose from `agent.py`.
- `kb_search.py` is keyword-based for MVP. Do not add vector/embedding logic here until the stretch phase.
- State is persisted to `state/ticket_state.json` after every ticket — do not batch-write at the end.
- One source of truth per ticket: `state/ticket_state.json` owns current status; raw `data/` files are read-only inputs.

---

## Agent Rules (enforce these in prompts and code)

1. Use ticket data + knowledge base only — do not invent infrastructure details.
2. If confidence is low or no KB article matches → escalate, never guess.
3. Return structured JSON only from the agent — no markdown prose in agent output.
4. Do not mark resolved without user confirmation.
5. Prefer the simplest troubleshooting steps first.

---

## What NOT to Do

- Do not write to `data/` — those are read-only source inputs.
- Do not add a database (SQLite, Postgres, etc.) in the MVP phase.
- Do not inline the agent prompt in `main.py` — it lives in `agent.py`.
- Do not swallow exceptions in `state_manager.py` — corrupt state is worse than a crash.
- Do not add Streamlit or RAG until the core CLI loop works end-to-end.

---

## Expected MVP Output

```
AI Helpdesk Agent processed 5 tickets
4 solutions proposed
1 ticket escalated
Report saved to output/proposed_solutions.md
```

---

## Claude-Specific Guidance

- Prefer editing existing files over creating new ones.
- Default to no comments — function and variable names should be self-explanatory.
- Never skip hooks (`--no-verify`) or force-push without explicit instruction.
- When adding a stretch goal feature, confirm scope before starting — do not gold-plate the MVP.
- Match response length to task complexity.
