#!/usr/bin/env python3
"""
Git-Notes Memory Integration for Obsidian AI Writer
2026-01-30

Integrates with git-notes-memory skill for persistent context.
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime


class GitNotesMemory:
    """Wrapper for git-notes-memory operations."""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.memory_script = Path("/home/zous/clawd/skills/git-notes-memory/memory.py")
    
    def _run(self, *args) -> dict:
        """Run memory.py command and return JSON result."""
        cmd = ["python3", str(self.memory_script), "-p", str(self.workspace)] + list(args)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    
    def sync_start(self) -> dict:
        """Start session sync, get context."""
        return self._run("sync", "--start")
    
    def sync_end(self, summary: str) -> dict:
        """End session sync with summary."""
        return self._run("sync", "--end", json.dumps({"summary": summary}))
    
    def remember(self, data: dict, tags: list = None, importance: str = "n") -> dict:
        """Store a new memory."""
        cmd = ["remember", json.dumps(data)]
        if tags:
            cmd.extend(["-t", ",".join(tags)])
        cmd.extend(["-i", importance])
        return self._run(*cmd)
    
    def get(self, topic: str) -> dict:
        """Get memories related to a topic."""
        return self._run("get", topic)
    
    def search(self, query: str) -> dict:
        """Full-text search across memories."""
        return self._run("search", query)
    
    def recall_last(self, count: int = 10) -> dict:
        """Get last N memories."""
        return self._run("recall", "--last", str(count))
    
    def entities(self) -> dict:
        """List all extracted entities."""
        return self._run("entities")


# Integration helper for Obsidian AI Writer
def get_memory_context(workspace: str = ".", query: str = None) -> dict:
    """Get relevant memory context for writing."""
    memory = GitNotesMemory(workspace)
    
    context = {
        "session": memory.sync_start(),
        "entities": memory.entities()
    }
    
    if query:
        context["related"] = memory.get(query)
    
    return context


def remember_decision(workspace: str, decision: str, reason: str = "", 
                      tags: list = None, importance: str = "h"):
    """Remember a decision made during writing."""
    memory = GitNotesMemory(workspace)
    
    data = {
        "decision": decision,
        "reason": reason,
        "context": "Obsidian AI Writer session"
    }
    
    return memory.remember(data, tags, importance)


# Example usage
if __name__ == "__main__":
    print("📝 Git-Notes Memory Integration")
    print("=" * 40)
    
    # Get session context
    ctx = get_memory_context(".")
    print(f"\n🔄 Session: {ctx['session'].get('b', 'unknown')} branch")
    print(f"📊 Topics: {ctx['session'].get('t', {})} ({ctx['session'].get('n', 0)} memories)")
    
    # Get entities
    entities = ctx.get('entities', {})
    print(f"🏷️  Top entities: {list(entities.keys())[:5]}")
