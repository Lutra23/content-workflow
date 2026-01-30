#!/bin/bash
# Workspace file search for memory

QUERY="$1"
LIMIT="${2:-10}"
WORKSPACE="/home/zous/clawd"

if [ -z "$QUERY" ]; then
  echo "Usage: file-search.sh <query> [limit]"
  exit 1
fi

# Search in memory files and MEMORY.md
grep -r --include="*.md" -l "$QUERY" "$WORKSPACE" 2>/dev/null | head -n "$LIMIT"
