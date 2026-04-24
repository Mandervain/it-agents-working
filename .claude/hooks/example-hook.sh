#!/usr/bin/env bash
# Example hook — delete this file and replace with real hooks.
#
# Hooks are shell scripts triggered by Claude Code events.
# Wire them up in .claude/settings.json under "hooks".
#
# Available events:
#   PreToolUse   — runs before Claude calls a tool
#   PostToolUse  — runs after Claude calls a tool
#   Stop         — runs when Claude finishes a turn
#
# The hook receives a JSON payload on stdin describing the event.
# Exit 0 to allow, non-zero to block (PreToolUse only).
#
# Example — block any `rm -rf` command:
#
#   input=$(cat)
#   command=$(echo "$input" | jq -r '.tool_input.command // ""')
#   if echo "$command" | grep -q 'rm -rf'; then
#     echo "Blocked: rm -rf is not allowed" >&2
#     exit 1
#   fi
#
# See: https://docs.anthropic.com/claude-code/hooks

exit 0
