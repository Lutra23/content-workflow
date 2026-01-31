#!/bin/bash
# 每日目标回顾 - 每天 3 次检查目标进度

echo "=== $(date) Daily Goals Review ==="

GOALS_FILE="/home/zous/clawd/.goals/active-goals.md"

if [ -f "$GOALS_FILE" ]; then
  echo "Active Goals:"
  cat "$GOALS_FILE"
else
  echo "No goals file found"
fi

# 检查今日任务完成情况
TODAY=$(date +%Y-%m-%d)
TASKS_COMPLETED=$(grep -c "$TODAY" /home/zous/clawd/memory/$(date +%Y-%m-%d)*.md 2>/dev/null || echo 0)
echo "Tasks logged today: $TASKS_COMPLETED"

# 检查周目标进度
WEEK=$(date +%U)
echo "Current week: $WEEK"

# 记录回顾
echo "$(date '+%Y-%m-%d %H:%M') | Week $WEEK | Tasks today: $TASKS_COMPLETED" >> /home/zous/clawd/.logs/goals-review.log

echo "=== Review Complete ==="
