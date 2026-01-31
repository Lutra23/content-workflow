#!/bin/bash
# Moltbook 评论监听 - 检测帖子新评论并通知

API_KEY="moltbook_sk_72WuJJeIxummE155mnnb8_kr_eW1AA4K"
BASE_URL="https://www.moltbook.com/api/v1"

# 我的帖子 ID 列表
MY_POSTS=(
  "af249228-9461-4647-befa-9c6e425a6dc7"  # Nightly Build 帖子
  "ff34b70f-9226-4fbf-bb52-8afccb40a6e3"  # Self-Review 帖子
)

LOG_FILE="/home/zous/clawd/.logs/moltbook-comments.log"
NOTIFICATION_FILE="/home/zous/clawd/.notifications/moltbook-comments.json"

mkdir -p "$(dirname "$NOTIFICATION_FILE")"

echo "=== $(date) Moltbook Comment Monitor ===" >> "$LOG_FILE"

NEW_COMMENTS=0

for POST_ID in "${MY_POSTS[@]}"; do
  echo "Checking post: $POST_ID" >> "$LOG_FILE"
  
  # 获取评论
  COMMENTS=$(curl -s "$BASE_URL/posts/$POST_ID/comments" \
    -H "Authorization: Bearer $API_KEY" 2>/dev/null)
  
  # 解析评论数量
  COMMENT_COUNT=$(echo "$COMMENTS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('comments',[])))" 2>/dev/null || echo "0")
  
  # 检查是否有 @我的评论
  MENTIONS=$(echo "$COMMENTS" | grep -c "lutra_otter" 2>/dev/null || echo "0")
MENTIONS=$(echo "$MENTIONS" | tr -d '\n\r')
  
  if [ "$MENTIONS" -gt 0 ]; then
    echo "⚠️ Found $MENTIONS mentions in post $POST_ID"
    ((NEW_COMMENTS++))
    
    # 记录提及
    echo "$COMMENTS" | python3 -c "
import json,sys,datetime
d=json.load(sys.stdin)
print(f\"Found {len(d.get('comments',[]))} comments\")
for c in d.get('comments',[]):
    if 'lutra_otter' in c.get('content',''):
        print(f\"- @{c.get('author',{}).get('name','?')}: {c.get('content','')[:100]}...\")
" >> "$LOG_FILE"
  fi
done

# 如果有新评论，生成通知
if [ "$NEW_COMMENTS" -gt 0 ]; then
  echo "{\"time\":\"$(date -Iseconds)\",\"count\":$NEW_COMMENTS}" > "$NOTIFICATION_FILE"
  echo "✅ Generated notification for $NEW_COMMENTS new comments"
else
  echo "✅ No new comments"
fi

echo "=== Monitor Complete ===" >> "$LOG_FILE"
