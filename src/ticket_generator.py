import json
import random
from datetime import datetime, timezone
from pathlib import Path

USERS = [
    "anna.kowalska", "jan.wisniewski", "piotr.nowak", "maria.wojcik",
    "tomasz.kaminski", "agnieszka.lewandowska", "krzysztof.zielinski",
    "barbara.szymanska", "adam.wozniak", "ewa.kozlowska", "marek.jankowski",
    "joanna.wisniewska", "pawel.wojcik", "katarzyna.kowalczyk", "lukasz.kaczmarek",
]

MESSAGES: dict[str, list[str]] = {
    "vpn": [
        "Cannot connect to VPN after changing my password. Getting authentication failed error.",
        "VPN client keeps disconnecting every 10 minutes. Cannot stay connected.",
        "VPN connects but I cannot access internal systems. Ping to servers times out.",
        "After laptop update VPN stopped working entirely. Error: connection timeout.",
        "VPN works from home but not from the office network. Getting certificate error.",
        "Getting MFA prompt loop on VPN — approves but immediately asks again.",
    ],
    "outlook": [
        "Outlook not receiving emails since this morning. Sending works fine.",
        "Calendar invites are not showing up in Outlook. Missing all meetings.",
        "Outlook crashes every time I try to open an attachment.",
        "Shared mailbox not visible in Outlook after permissions were updated.",
        "Email search in Outlook returns no results even for recent messages.",
        "Out-of-office reply not working despite being configured correctly.",
    ],
    "printer": [
        "Printer on Floor 2 not printing. Jobs stuck in queue with no error.",
        "Color printer in Room 301 printing blank pages on every job.",
        "Cannot find the network printer after moving to a new desk.",
        "Printer shows online in the system but all jobs go to error state.",
        "Print jobs sent but never appear in the queue at all.",
        "Printer prints but cuts off the right side of every document.",
    ],
    "laptop_slow": [
        "Laptop extremely slow since last Windows update. Takes 10 min to boot.",
        "Applications randomly freeze. Have to force restart multiple times a day.",
        "Laptop fan running at full speed constantly. Very hot and slow.",
        "Teams video calls dropping due to laptop performance issues.",
        "Browser running slowly — opening a new tab takes 30 seconds.",
        "Disk usage at 100% constantly even with no applications open.",
    ],
    "password_reset": [
        "Locked out of account after too many wrong password attempts.",
        "Password expired and the self-service portal is showing an error.",
        "Cannot log in to HR system. Password reset link not arriving by email.",
        "Account locked after returning from two-week vacation. Need urgent access.",
        "New employee cannot set initial password — activation link already expired.",
        "SSO login works but the VPN portal keeps rejecting my password.",
    ],
}

SOURCES = ["slack", "teams", "email", "service_desk"]
PRIORITIES = ["high", "medium", "low"]
CATEGORIES = list(MESSAGES.keys())


def _get_max_id() -> int:
    data_root = Path("data")
    max_id = 1000
    for source_dir in data_root.iterdir():
        if not source_dir.is_dir():
            continue
        tickets_file = source_dir / "tickets.json"
        if not tickets_file.exists():
            continue
        try:
            for t in json.loads(tickets_file.read_text()):
                num = int(t.get("id", "INC-1000").replace("INC-", ""))
                max_id = max(max_id, num)
        except (json.JSONDecodeError, ValueError):
            pass
    return max_id


def generate_tickets(
    n: int,
    category: str | None = None,
    source: str | None = None,
    priority: str | None = None,
) -> list[dict]:
    base_id = _get_max_id()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tickets = []
    for i in range(n):
        cat = category or random.choice(CATEGORIES)
        src = source or random.choice(SOURCES)
        pri = priority or random.choices(PRIORITIES, weights=[25, 50, 25])[0]
        tickets.append({
            "id": f"INC-{base_id + i + 1}",
            "source": src,
            "user": random.choice(USERS),
            "priority": pri,
            "category": cat,
            "status": "open",
            "message": random.choice(MESSAGES[cat]),
            "created_at": now,
        })
    return tickets


def save_tickets(tickets: list[dict]) -> None:
    by_source: dict[str, list] = {}
    for t in tickets:
        by_source.setdefault(t["source"], []).append(t)

    for source, new_tickets in by_source.items():
        source_dir = Path("data") / source
        source_dir.mkdir(parents=True, exist_ok=True)
        tickets_file = source_dir / "tickets.json"
        existing: list = []
        if tickets_file.exists():
            try:
                existing = json.loads(tickets_file.read_text())
            except json.JSONDecodeError:
                pass
        existing.extend(new_tickets)
        tickets_file.write_text(json.dumps(existing, indent=2))
