import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import kb_search
import state_manager
import ticket_loader
from agent import _model, get_client

CHAT_SYSTEM_PROMPT = """You are an interactive IT Helpdesk assistant in a live chat with an employee.

You have a knowledge base article relevant to their issue. Guide them through troubleshooting step by step:
- Start by acknowledging the issue and asking what they have already tried
- Guide them to the next logical step based on their replies
- If a step doesn't work, move to the next one
- If all steps are exhausted and the issue persists, tell them you are escalating to a human agent

Keep responses short and practical (2-4 sentences). This is a live chat, not a formal email."""


def run_chat(ticket: dict) -> None:
    print(f"\n{'='*60}")
    print(f"Chat — {ticket['id']} [{ticket.get('category', '')}] ({ticket.get('priority', '')} priority)")
    print(f"User: {ticket.get('user', '')}")
    print(f"Issue: {ticket.get('message', '')}")
    print("Type 'exit' to quit.")
    print(f"{'='*60}\n")

    kb_article = kb_search.find_kb_article(ticket.get("category", ""))
    client = get_client()

    system = CHAT_SYSTEM_PROMPT
    if kb_article:
        system += f"\n\n## Knowledge Base\n\n{kb_article}"

    history: list[dict] = [{"role": "user", "content": ticket.get("message", "")}]

    response = client.messages.create(
        model=_model(), max_tokens=512, system=system, messages=history
    )
    agent_reply = response.content[0].text
    print(f"Agent: {agent_reply}\n")
    history.append({"role": "assistant", "content": agent_reply})

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChat ended.")
            break

        if user_input.lower() in ("exit", "quit", "/quit"):
            print("Chat ended.")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model=_model(), max_tokens=512, system=system, messages=history
        )
        agent_reply = response.content[0].text
        print(f"\nAgent: {agent_reply}\n")
        history.append({"role": "assistant", "content": agent_reply})

        if "escalat" in agent_reply.lower():
            state_manager.update_ticket_state(ticket["id"], {
                "ticket_id": ticket["id"],
                "category": ticket.get("category"),
                "confidence": "low",
                "status": "escalated",
                "proposed_solution": [m["content"] for m in history if m["role"] == "assistant"],
                "next_action": "escalate_to_human",
                "user": ticket.get("user"),
                "priority": ticket.get("priority"),
            })
            print("[Ticket escalated to human agent]")
            break


def main() -> None:
    tickets = ticket_loader.load_all_tickets()

    print("\nAvailable tickets:")
    for i, t in enumerate(tickets):
        print(f"  {i + 1}. {t['id']} [{t.get('category', '')}] ({t.get('priority', '')}) — {t.get('user', '')} [{t.get('status', '')}]")

    print()
    try:
        choice = input("Select ticket number (Enter for first): ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if not choice:
        ticket = tickets[0]
    else:
        try:
            ticket = tickets[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

    run_chat(ticket)


if __name__ == "__main__":
    main()
