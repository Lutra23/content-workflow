---
name: git-notes-sync
description: "Syncs git-notes memory when a new session starts"
metadata: {"clawdbot":{"emoji":"🔄","events":["command:new"],"requires":{"bins":["python3","git"]}}}
---

# Git Notes Sync Hook

Automatically runs `git-notes-memory sync --start` when a new session begins.

## What It Does

- Listens for `command:new` events
- Executes git-notes-memory sync to load branch-specific memories
- Runs silently without user notification

## Requirements

- Python 3
- Git
- git-notes-memory skill installed at `skills/git-notes-memory/`
