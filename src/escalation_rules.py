RULES: list[dict] = [
    {
        "name": "high_priority_sla_breach",
        "condition": lambda ticket, sla: ticket.get("priority") == "high" and sla["breached"],
        "reason": "SLA breached for high-priority ticket — immediate escalation required",
    },
    {
        "name": "medium_priority_sla_breach",
        "condition": lambda ticket, sla: ticket.get("priority") == "medium" and sla["breached"],
        "reason": "SLA breached for medium-priority ticket — escalation required",
    },
    {
        "name": "stuck_over_24h",
        "condition": lambda ticket, sla: sla["elapsed_minutes"] > 24 * 60,
        "reason": "Ticket unresolved for over 24 hours — mandatory escalation",
    },
]


def check_auto_escalation(ticket: dict, sla_info: dict) -> tuple[bool, str]:
    for rule in RULES:
        if rule["condition"](ticket, sla_info):
            return True, rule["reason"]
    return False, ""


def build_escalation_state(ticket: dict, reason: str, sla_info: dict) -> dict:
    return {
        "ticket_id": ticket["id"],
        "category": ticket.get("category", "unknown"),
        "confidence": "low",
        "status": "escalated",
        "proposed_solution": [],
        "next_action": "escalate_to_human",
        "escalation_reason": reason,
        "user": ticket.get("user", ""),
        "priority": ticket.get("priority", ""),
        "sla_breached": sla_info["breached"],
        "sla_elapsed_minutes": sla_info["elapsed_minutes"],
    }
