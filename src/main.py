import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import agent
import escalation_rules
import kb_search
import report_writer
import sla_tracker
import state_manager
import ticket_loader


def process_ticket(ticket: dict) -> dict | None:
    ticket_id = ticket["id"]
    category = ticket.get("category", "unknown")
    print(f"Processing {ticket_id} [{category}] ...")
    try:
        sla_info = sla_tracker.calculate_sla(ticket)

        should_escalate, reason = escalation_rules.check_auto_escalation(ticket, sla_info)
        if should_escalate:
            print(f"  Auto-escalating: {reason}")
            result = escalation_rules.build_escalation_state(ticket, reason, sla_info)
            state_manager.update_ticket_state(ticket_id, result)
            return result

        use_rag = os.environ.get("USE_RAG", "") == "1"
        if use_rag:
            from kb_search_rag import find_kb_article_rag
            kb_article = find_kb_article_rag(ticket.get("message", ""))
        else:
            kb_article = kb_search.find_kb_article(category)

        result = agent.call_agent(ticket, kb_article)
        result["user"] = ticket.get("user", "")
        result["priority"] = ticket.get("priority", "")
        result["sla_breached"] = sla_info["breached"]
        result["sla_elapsed_minutes"] = sla_info["elapsed_minutes"]
        state_manager.update_ticket_state(ticket_id, result)
        return result
    except Exception as exc:
        print(f"  ERROR processing {ticket_id}: {exc}", file=sys.stderr)
        return None


def print_summary(results: list[dict | None]) -> None:
    processed = [r for r in results if r is not None]
    proposed = sum(1 for r in processed if r.get("status") == "solution_proposed")
    escalated = sum(1 for r in processed if r.get("status") == "escalated")
    print(f"Processed {len(processed)} tickets — {proposed} proposed, {escalated} escalated")
    print(f"Report saved to {report_writer.REPORT_FILE}")


def main() -> None:
    try:
        agent.get_client()
    except EnvironmentError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    tickets = ticket_loader.load_all_tickets()
    open_tickets = ticket_loader.filter_open_tickets(tickets)
    print(f"Found {len(open_tickets)} open tickets across all sources")

    results = [process_ticket(t) for t in open_tickets]

    state = state_manager.load_state()
    report_writer.write_report(state)
    print_summary(results)


if __name__ == "__main__":
    main()
