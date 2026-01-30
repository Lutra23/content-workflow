#!/bin/bash
# Quick Status - Check Clawdbot system status

echo "========================================"
echo "🦞 Clawdbot System Status"
echo "========================================"
echo ""

# Gateway status
echo "📡 Gateway:"
if pgrep -f "clawdbot gateway" > /dev/null; then
    echo "   ✅ Running"
else
    echo "   ❌ Not running"
fi

echo ""

# Cron jobs
echo "⏰ Cron Jobs:"
crontab -l 2>/dev/null | grep -q "nightly" && echo "   ✅ Nightly Project scheduled" || echo "   ⚪ No nightly job"

echo ""

# Skills count
SKILLS_COUNT=$(ls -1 /home/zous/clawd/skills/*/SKILL.md 2>/dev/null | wc -l)
echo "🛠️  Skills Installed: $SKILLS_COUNT"

echo ""

# Memory files
TODAY_MEM=$(ls ~/clawd/memory/$(date +%Y-%m-%d).md 2>/dev/null && echo "✅ Exists" || echo "⚪ No notes today")
echo "📝 Today's Memory: $TODAY_MEM"

echo ""

# Recent projects
RECENT_PROJECTS=$(ls -td /home/zous/clawd/nightly-projects/*/ 2>/dev/null | head -3 | wc -l)
echo "🎁 Nightly Projects: $RECENT_PROJECTS recent"

echo ""

# Tools in ~/bin
TOOLS_COUNT=$(ls ~/bin/ 2>/dev/null | wc -l)
echo "🔧 Local Tools: $TOOLS_COUNT in ~/bin/"

echo ""
echo "========================================"
echo "💡 Quick Commands:"
echo "   qn 'note'     - Quick note"
echo "   qc 'task'     - Quick capture"
echo "   clawdbot status - Full status"
echo "========================================"
