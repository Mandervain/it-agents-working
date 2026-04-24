from datetime import datetime, timedelta, timezone

SLA_HOURS: dict[str, int] = {
    "high": 1,
    "medium": 4,
    "low": 8,
}


def calculate_sla(ticket: dict) -> dict:
    created_str = ticket.get("created_at", "")
    created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    elapsed = now - created
    sla_hours = SLA_HOURS.get(ticket.get("priority", "low"), 8)
    sla_limit = timedelta(hours=sla_hours)
    breached = elapsed > sla_limit
    remaining = sla_limit - elapsed

    return {
        "sla_hours": sla_hours,
        "elapsed_minutes": int(elapsed.total_seconds() / 60),
        "breached": breached,
        "remaining_minutes": max(0, int(remaining.total_seconds() / 60)),
    }
