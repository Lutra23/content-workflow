#!/usr/bin/env python3
"""
memory-recall - Quick CLI to search and recall saved memories

Usage:
    python main.py              # List all memories
    python main.py --search KEYWORD   # Search by keyword
    python main.py --recent 5        # Show recent 5
    python main.py --type decision   # Filter by type
    python main.py --critical        # Show critical memories
    python main.py --topics          # List topics
"""

import argparse
import subprocess
import json
import sys
import os

# Import the git-notes-memory module
sys.path.insert(0, "/home/zous/clawd/skills/git-notes-memory")
from memory import recall, search as mem_search, sync_start

VERSION = "1.0.0"
CWD = "/home/zous/clawd"

def run_git_memory(args):
    """Run git-notes-memory CLI"""
    mem_path = "/home/zous/clawd/skills/git-notes-memory/memory.py"
    result = subprocess.run(
        ["python3", mem_path, "-p", CWD] + args,
        capture_output=True, text=True
    )
    return result.stdout.strip()

def list_all():
    """List all memories overview"""
    data = json.loads(run_git_memory(["recall"]))
    print("\n📚 Memory Overview")
    print("=" * 40)
    print(f"Branch: {data.get('b', 'unknown')}")
    print(f"Total memories: {data.get('n', 0)}")
    
    if data.get('topics'):
        print(f"\n🏷️  Topics: {', '.join(data.get('topics', []))}")
    
    if data.get('critical'):
        print("\n🔴 Critical:")
        for m in data.get('critical', []):
            print(f"  • {m['s']}")
    
    if data.get('high'):
        print("\n🟡 High priority:")
        for m in data.get('high', []):
            print(f"  • {m['s']}")

def show_search(query):
    """Search memories"""
    result = json.loads(run_git_memory(["search", query]))
    
    print(f"\n🔍 Search: '{query}'")
    print("=" * 40)
    
    if not result.get('results'):
        print("No results found.")
        return
    
    for m in result['results']:
        icon = {"decision": "🎯", "preference": "❤️", "learning": "📖", 
                "task": "✅", "info": "📝"}.get(m.get('t', 'info'), "📝")
        imp = {"c": "🔴", "h": "🟡", "n": "⚪", "l": "🕸️"}.get(m.get('i', 'n'), "⚪")
        print(f"{icon} {imp} {m['s']}")
        print(f"    └─ Type: {m['t']} | ID: {m['id']} | Branch: {m['b']}")

def show_recent(count):
    """Show recent memories"""
    result = json.loads(run_git_memory(["recall", "--last", str(count)]))
    
    print(f"\n🕐 Recent {count} Memories")
    print("=" * 40)
    
    for mid, entry in result.items():
        icon = {"decision": "🎯", "preference": "❤️", "learning": "📖",
                "task": "✅", "info": "📝"}.get(entry.get('t', 'info'), "📝")
        print(f"{icon} {entry.get('s', 'No summary')}")
        print(f"    └─ {entry.get('t', 'info')} | Updated: {entry.get('u', '?')}")

def show_critical():
    """Show critical memories only"""
    data = sync_start(CWD)
    
    print("\n🔴 CRITICAL MEMORIES")
    print("=" * 40)
    
    if not data.get('critical'):
        print("No critical memories.")
        return
    
    for m in data.get('critical', []):
        print(f"  • {m['s']}")
        print(f"    └─ {m['t']} | ID: {m['id']}")

def show_topics():
    """List all topics with counts"""
    result = json.loads(run_git_memory(["entities"]))
    
    print("\n🏷️  All Topics")
    print("=" * 40)
    
    entities = result.get('entities', {})
    if not entities:
        print("No topics found.")
        return
    
    for topic, count in entities.items():
        print(f"  {count:3} │ {topic}")

def show_by_type(mtype):
    """Filter by memory type"""
    result = json.loads(run_git_memory(["recall"]))
    
    type_names = {
        "decision": "Decisions",
        "preference": "Preferences",
        "learning": "Learnings",
        "task": "Tasks",
        "info": "Info"
    }
    
    print(f"\n📁 {type_names.get(mtype, mtype)}")
    print("=" * 40)
    
    # Search for memories of this type
    search_result = json.loads(run_git_memory(["search", mtype]))
    
    count = 0
    for m in search_result.get('results', []):
        if m.get('t') == mtype:
            print(f"  • {m['s']}")
            count += 1
    
    if count == 0:
        print(f"No {mtype} memories found.")

def install():
    """Install script to PATH"""
    script_path = os.path.abspath(__file__)
    install_dir = os.path.expanduser("~/.local/bin")

    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    wrapper = f"""#!/bin/bash
python3 "{script_path}" "$@"
"""
    wrapper_path = os.path.join(install_dir, "memory-recall")

    with open(wrapper_path, "w") as f:
        f.write(wrapper)
    os.chmod(wrapper_path, 0o755)

    print(f"✅ Installed to {wrapper_path}")
    print(f"💡 Add to PATH: export PATH=\"$HOME/.local/bin:$PATH\"")

def main():
    parser = argparse.ArgumentParser(
        description="🦦 memory-recall - Quick CLI to search saved memories",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--install", action="store_true", help="Install to PATH")
    parser.add_argument("--version", action="store_true", help="Show version")
    
    # Filter options
    parser.add_argument("--search", "-s", metavar="KEYWORD", help="Search memories")
    parser.add_argument("--recent", "-r", type=int, metavar="N", help="Show N recent memories")
    parser.add_argument("--type", "-t", metavar="TYPE", 
                       choices=["decision", "preference", "learning", "task", "info"],
                       help="Filter by type")
    parser.add_argument("--critical", "-c", action="store_true", help="Show critical only")
    parser.add_argument("--topics", action="store_true", help="List all topics")

    args = parser.parse_args()

    if args.version:
        print(f"memory-recall v{VERSION}")
        return

    if args.install:
        install()
        return

    # Route to appropriate function
    if args.search:
        show_search(args.search)
    elif args.recent:
        show_recent(args.recent)
    elif args.type:
        show_by_type(args.type)
    elif args.critical:
        show_critical()
    elif args.topics:
        show_topics()
    else:
        list_all()

if __name__ == "__main__":
    main()
