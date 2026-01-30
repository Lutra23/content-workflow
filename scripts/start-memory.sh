#!/bin/bash
# Git-Notes Memory startup script

WORKSPACE="/home/zous/clawd"
PYTHON_PATH="/usr/bin/python3"

# Sync Git-Notes memory at session start
if [ -f "$WORKSPACE/skills/git-notes-memory/memory.py" ]; then
  cd "$WORKSPACE"
  $PYTHON_PATH skills/git-notes-memory/memory.py -p "$WORKSPACE" sync --start
else
  echo "git-notes-memory not installed, skipping sync"
fi
