#!/usr/bin/env bash
# Blocks any write to the data/ directory — those files are read-only ticket sources.
# Wired up as a PreToolUse hook in settings.json for Edit and Write tools.

input=$(cat)
file_path=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

if echo "$file_path" | grep -q '^data/'; then
  echo "Blocked: data/ is read-only. Write to state/ or output/ instead." >&2
  exit 1
fi

exit 0
