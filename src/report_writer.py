from datetime import datetime, timezone
from pathlib import Path

OUTPUT_DIR = Path("output")
REPORT_FILE = OUTPUT_DIR / "proposed_solutions.md"


def count_by_status(state: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in state.values():
        status = entry.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def format_table_row(ticket_id: str, entry: dict) -> str:
    category = entry.get("category", "")
    priority = entry.get("priority", "")
    user = entry.get("user", "")
    confidence = entry.get("confidence", "")
    status = entry.get("status", "")
    next_action = entry.get("next_action", "")
    return f"| {ticket_id} | {category} | {priority} | {user} | {confidence} | {status} | {next_action} |"


def write_report(state: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    counts = count_by_status(state)
    proposed = counts.get("solution_proposed", 0)
    escalated = counts.get("escalated", 0)
    total = len(state)

    lines = [
        "# IT Helpdesk Agent — Proposed Solutions",
        "",
        f"Generated: {now}",
        "",
        "| Ticket ID | Category | Priority | User | Confidence | Status | Next Action |",
        "|-----------|----------|----------|------|------------|--------|-------------|",
    ]

    for ticket_id in sorted(state.keys()):
        lines.append(format_table_row(ticket_id, state[ticket_id]))

    lines += [
        "",
        "## Summary",
        "",
        f"- Total processed: {total}",
        f"- Solutions proposed: {proposed}",
        f"- Escalated: {escalated}",
        "",
    ]

    with REPORT_FILE.open("w") as f:
        f.write("\n".join(lines))
