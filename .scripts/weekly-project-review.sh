#!/bin/bash
# 每周项目回顾 - 每周 2 次回顾项目进展

echo "=== $(date) Weekly Project Review ==="

PROJECTS_DIR="/home/zous/clawd"

echo "=== Active Projects ==="
for dir in "$PROJECTS_DIR"/*/; do
  if [ -d "$dir" ]; then
    NAME=$(basename "$dir")
    if [ -f "$dir/README.md" ] || [ -f "$dir/SKILL.md" ]; then
      echo "📁 $NAME"
    fi
  fi
done

echo "=== Recent Commits ==="
cd "$PROJECTS_DIR"
git log --oneline -5 2>/dev/null || echo "No git history"

echo "=== Git Status ==="
git status --short 2>/dev/null | head -10 || echo "Not a git repo"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Weekly project review complete" >> /home/zous/clawd/.logs/project-review.log

echo "=== Review Complete ==="
