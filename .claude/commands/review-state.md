---
name: review-state
description: Show current ticket state and flag any tickets stuck in an intermediate status.
---

Read `state/ticket_state.json` and report:

1. Count of tickets per status (`open`, `triaged`, `solution_proposed`, `waiting_for_user`, `resolved`, `escalated`)
2. Any tickets that have been in `solution_proposed` or `waiting_for_user` without a `next_action` field (those are likely bugs)
3. Any tickets missing required fields (`ticket_id`, `status`, `confidence`, `proposed_solution`)

Format the report as a short markdown table.
