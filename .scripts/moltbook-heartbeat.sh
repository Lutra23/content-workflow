#!/bin/bash
# Moltbook 自动化任务 - 每 4 小时运行

API_KEY="moltbook_sk_72WuJJeIxummE155mnnb8_kr_eW1AA4K"
BASE_URL="https://www.moltbook.com/api/v1"

echo "=== $(date) Moltbook Heartbeat ==="

# 1. 检查账户状态
status=$(curl -s "$BASE_URL/agents/status" -H "Authorization: Bearer $API_KEY")
echo "Status: $status"

# 2. 检查是否有 @mention 或回复
mentions=$(curl -s "$BASE_URL/feed?limit=10" -H "Authorization: Bearer $API_KEY" | grep -c "lutra_otter" || echo 0)
echo "Mentions found: $mentions"

# 3. 简单检查是否还能发帖（不实际发帖）
echo "Last active: $(curl -s "$BASE_URL/agents/me" -H "Authorization: Bearer $API_KEY" | grep -o '"last_active":"[^"]*"')"

# 4. 获取热门帖子（学习用）
echo "Top 5 posts:"
curl -s "$BASE_URL/posts?sort=hot&limit=5" -H "Authorization: Bearer $API_KEY" | grep -o '"title":"[^"]*"' | head -5

echo "=== Heartbeat Complete ==="
