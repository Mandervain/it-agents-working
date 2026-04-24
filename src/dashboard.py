import os
import subprocess
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

import sla_tracker
import state_manager
import ticket_generator
import ticket_loader

st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🎫", layout="wide")
st.title("🎫 IT Helpdesk Agent Dashboard")

STATUS_ICONS = {
    "open": "🔵",
    "triaged": "🟣",
    "solution_proposed": "🟢",
    "waiting_for_user": "🟡",
    "resolved": "⚪",
    "escalated": "🔴",
}

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Backend")
    backend = st.radio("Provider", ["AWS Bedrock", "Anthropic API"])

    if backend == "AWS Bedrock":
        aws_region = st.text_input("AWS Region", value=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
        api_key_val = ""
    else:
        api_key_val = st.text_input(
            "ANTHROPIC_API_KEY",
            type="password",
            value=os.environ.get("ANTHROPIC_API_KEY", ""),
        )
        aws_region = ""

    use_rag = st.checkbox(
        "Vector Search (RAG)",
        value=False,
        help="TF-IDF cosine similarity over KB articles instead of keyword matching",
    )

    st.divider()

    if st.button("▶ Run Agent", use_container_width=True, type="primary"):
        env = os.environ.copy()
        if backend == "AWS Bedrock":
            env["CLAUDE_CODE_USE_BEDROCK"] = "1"
            env["AWS_DEFAULT_REGION"] = aws_region
            env.pop("ANTHROPIC_API_KEY", None)
        else:
            env.pop("CLAUDE_CODE_USE_BEDROCK", None)
            if api_key_val:
                env["ANTHROPIC_API_KEY"] = api_key_val

        env["USE_RAG"] = "1" if use_rag else ""

        project_root = Path(__file__).parent.parent
        with st.spinner("Agent processing tickets..."):
            proc = subprocess.run(
                [sys.executable, str(project_root / "src" / "main.py")],
                capture_output=True,
                text=True,
                env=env,
                cwd=str(project_root),
            )

        if proc.returncode == 0:
            st.success("Done!")
            st.code(proc.stdout)
        else:
            st.error("Agent failed")
            st.code(proc.stderr)

        st.rerun()

    st.divider()
    st.header("🎲 Generate Tickets")

    n_tickets = st.slider("Number of tickets", min_value=1, max_value=10, value=2)
    gen_category = st.selectbox("Category", ["Random"] + ticket_generator.CATEGORIES)
    gen_priority = st.selectbox("Priority", ["Random", "high", "medium", "low"])
    gen_source = st.selectbox("Source", ["Random"] + ticket_generator.SOURCES)

    if st.button("🎲 Generate & Add", use_container_width=True):
        new_tickets = ticket_generator.generate_tickets(
            n=n_tickets,
            category=None if gen_category == "Random" else gen_category,
            priority=None if gen_priority == "Random" else gen_priority,
            source=None if gen_source == "Random" else gen_source,
        )
        ticket_generator.save_tickets(new_tickets)
        st.success(f"Added {len(new_tickets)} ticket(s)")
        for t in new_tickets:
            st.caption(f"**{t['id']}** [{t['category']}] {t['priority']} · {t['user']}")
        st.rerun()

    st.divider()
    st.header("🔍 Filters")
    filter_status = st.multiselect("Status", list(STATUS_ICONS.keys()))
    filter_priority = st.multiselect("Priority", ["high", "medium", "low"])
    filter_source = st.multiselect("Source", ["slack", "teams", "email", "service_desk"])

# ── Load data ─────────────────────────────────────────────────────────────────
tickets = ticket_loader.load_all_tickets()
state = state_manager.load_state()

enriched = []
for t in tickets:
    entry = {**t}
    if t["id"] in state:
        entry.update(state[t["id"]])
    entry["sla"] = sla_tracker.calculate_sla(t)
    enriched.append(entry)

# ── Metrics ───────────────────────────────────────────────────────────────────
total = len(enriched)
proposed = sum(1 for e in enriched if e.get("status") == "solution_proposed")
escalated_count = sum(1 for e in enriched if e.get("status") == "escalated")
breached_count = sum(1 for e in enriched if e["sla"]["breached"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Tickets", total)
m2.metric("Solutions Proposed", proposed)
m3.metric("Escalated", escalated_count)
m4.metric("⚠️ SLA Breached", breached_count)

st.divider()

# ── Apply filters ─────────────────────────────────────────────────────────────
visible = enriched
if filter_status:
    visible = [e for e in visible if e.get("status") in filter_status]
if filter_priority:
    visible = [e for e in visible if e.get("priority") in filter_priority]
if filter_source:
    visible = [e for e in visible if e.get("source") in filter_source]

visible = sorted(visible, key=lambda e: PRIORITY_ORDER.get(e.get("priority", "low"), 2))

if not visible:
    st.info("No tickets match the current filters.")

# ── Ticket cards ──────────────────────────────────────────────────────────────
for entry in visible:
    status = entry.get("status", "open")
    sla = entry["sla"]
    icon = STATUS_ICONS.get(status, "⚪")
    sla_tag = "⚠️ SLA BREACHED" if sla["breached"] else f"✅ {sla['remaining_minutes']}m left"

    with st.expander(
        f"{icon} **{entry['id']}** — {entry.get('category', '')} | "
        f"{entry.get('priority', '')} priority | {sla_tag}"
    ):
        left, right = st.columns(2)

        with left:
            st.markdown(f"**User:** {entry.get('user', '')}")
            st.markdown(f"**Source:** `{entry.get('source', '')}`")
            st.markdown(f"**Status:** `{status}`")
            st.markdown(f"**Confidence:** {entry.get('confidence', '—')}")
            if entry.get("escalation_reason"):
                st.error(f"🚨 {entry['escalation_reason']}")

        with right:
            st.markdown(f"**SLA limit:** {sla['sla_hours']}h")
            st.markdown(f"**Elapsed:** {sla['elapsed_minutes']} min")
            if sla["breached"]:
                st.error("SLA BREACHED")
            else:
                st.success(f"{sla['remaining_minutes']} min remaining")

        st.markdown(f"**Issue:** _{entry.get('message', '')}_")

        if entry.get("proposed_solution"):
            st.markdown("**Proposed Solution:**")
            for i, step in enumerate(entry["proposed_solution"], 1):
                st.markdown(f"{i}. {step}")

        na = entry.get("next_action", "—")
        st.markdown(f"**Next Action:** `{na}`")
