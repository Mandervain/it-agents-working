import json
import os
from pathlib import Path

STATE_FILE = Path("state/ticket_state.json")


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open() as f:
        return json.load(f)


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = STATE_FILE.with_suffix(".tmp")
    with tmp_file.open("w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp_file, STATE_FILE)


def update_ticket_state(ticket_id: str, agent_result: dict) -> None:
    state = load_state()
    state[ticket_id] = agent_result
    save_state(state)
