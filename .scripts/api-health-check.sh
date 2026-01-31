#!/bin/bash
# API 健康检查 - 每 4 小时检查外部 API

echo "=== $(date) API Health Check ==="

APIS=(
  "https://api.moltbook.com/health"
  "https://api.github.com"
  "https://hacker-news.firebaseio.com/v0"
)

for api in "${APIS[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$api" 2>/dev/null || echo "000")
  echo "$api: $STATUS"
done

# 检查内部服务
echo "=== Internal Services ==="
CLAWDBOT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:18789/health" 2>/dev/null || echo "000")
echo "Clawdbot Gateway: $CLAWDBOT_STATUS"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | API health check complete" >> /home/zous/clawd/.logs/api-health-check.log

echo "=== Check Complete ==="
