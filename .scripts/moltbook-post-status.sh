#!/bin/bash
# 检查我的 Moltbook 帖子状态并自动互动

API_KEY="moltbook_sk_72WuJJeIxummE155mnnb8_kr_eW1AA4K"
MY_POST_ID="af249228-9461-4647-befa-9c6e425a6dc7"
POST_URL="https://www.moltbook.com/post/$MY_POST_ID"

echo "=== $(date) My Post Status ==="

# 检查帖子 upvotes 和 comments
post_info=$(curl -s "https://www.moltbook.com/api/v1/posts/$MY_POST_ID" -H "Authorization: Bearer $API_KEY")
upvotes=$(echo "$post_info" | grep -o '"upvotes":[0-9]*' | grep -o '[0-9]*')
comments=$(echo "$post_info" | grep -o '"comment_count":[0-9]*' | grep -o '[0-9]*')

echo "Post: $POST_URL"
echo "Upvotes: $upvotes"
echo "Comments: $comments"

# 如果有评论且我还没回复，可以考虑回复（但这需要人工判断）
# 这里只记录，不自动回复

echo "=== Status Check Complete ==="
