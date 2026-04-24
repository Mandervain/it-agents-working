import json
from pathlib import Path

DATA_ROOT = Path("data")
SOURCES = ["slack", "teams", "email", "service_desk"]


def load_tickets_from_source(source_dir: Path) -> list[dict]:
    tickets_file = source_dir / "tickets.json"
    if not tickets_file.exists():
        return []
    with tickets_file.open() as f:
        return json.load(f)


def load_all_tickets() -> list[dict]:
    all_tickets = []
    for source in SOURCES:
        all_tickets.extend(load_tickets_from_source(DATA_ROOT / source))
    return all_tickets


def filter_open_tickets(tickets: list[dict]) -> list[dict]:
    return [t for t in tickets if t.get("status") == "open"]
