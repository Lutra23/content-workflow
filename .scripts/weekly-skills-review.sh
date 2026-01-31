#!/bin/bash
# 每周技能回顾 - 每周 2 次回顾已学技能

echo "=== $(date) Skills Review ==="

SKILLS_DIR="/home/zous/clawd/skills"

if [ -d "$SKILLS_DIR" ]; then
  echo "Installed skills:"
  ls -la "$SKILLS_DIR" | tail -n +4 | awk '{print $9, $5}'
fi

# 检查技能使用频率（基于 cron 和调用日志）
echo "=== Recently Used Skills ==="

# 简单的使用统计
echo "Skill usage would be tracked here"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Skills review complete" >> /home/zous/clawd/.logs/skills-review.log

echo "=== Review Complete ==="
