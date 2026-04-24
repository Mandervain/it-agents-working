---
name: run-agent
description: Run the helpdesk agent against all open tickets and show the summary output.
---

Run the helpdesk agent:

```bash
python src/main.py
```

After it completes, read `output/proposed_solutions.md` and `state/ticket_state.json` and give me a brief summary:
- How many tickets were processed
- How many got solutions proposed vs escalated
- Any errors or unexpected states
