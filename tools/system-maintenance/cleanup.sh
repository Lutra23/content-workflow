#!/bin/bash
# Weekly system cleanup script
# Run: bash /home/zous/clawd/tools/system-maintenance/cleanup.sh

echo "🧹 System Cleanup - $(date)"

# Clean npm cache
echo "Cleaning npm cache..."
npm cache clean --force 2>/dev/null

# Clear PM2 logs
echo "Clearing PM2 logs..."
pm2 flush 2>/dev/null || true

# Clean temp files older than 7 days
find /tmp -name "*.tmp" -mtime +7 -delete 2>/dev/null

# Clean npm temp
find ~/.npm/_cacache -type f -mtime +7 -delete 2>/dev/null

echo "✅ Cleanup complete"
