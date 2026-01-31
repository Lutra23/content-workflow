#!/bin/bash
# System Health Monitor
# Run: bash /home/zous/clawd/tools/system-maintenance/health-monitor.sh

echo "🏥 System Health Report - $(date)"
echo "================================"

# Clawdbot Status
echo "📦 Clawdbot:"
clawdbot status --deep 2>/dev/null | grep -E "Dashboard|Gateway|Status|Agents|Memory" | head -5 || echo "  Unable to get status"

# PM2 Services
echo ""
echo "🚀 PM2 Services:"
pm2 jlist 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for p in data:
    print(f'  {p[\"name\"]}: {p[\"pm2_env\"][\"status\"]} ({p[\"pm2_env\"][\"pm_uptime\"] // 1000 // 60}min uptime)')
" 2>/dev/null || echo "  Unable to get PM2 status"

# Disk Usage
echo ""
echo "💾 Disk Usage:"
df -h /home | tail -1 | awk '{print "  Root: " $5 " used (" $3 "/" $2 ")"}'

# Memory Check
echo ""
echo "🧠 Memory:"
free -h | grep Mem | awk '{print "  Used: " $3 "/" $2}'

# Cron Jobs
echo ""
echo "⏰ Cron Jobs:"
clawdbot cron list 2>/dev/null | grep -E "enabled|nextRun" | head -4 || echo "  Unable to get cron status"

echo ""
echo "================================"
echo "✅ Health check complete"
