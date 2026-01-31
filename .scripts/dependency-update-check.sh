#!/bin/bash
# 项目依赖更新检查 - 每周 2 次检查依赖更新

echo "=== $(date) Dependency Update Check ==="

cd /home/zous/clawd

# Python 依赖
echo "=== Python Dependencies ==="
if [ -f "requirements.txt" ]; then
  pip list --outdated 2>/dev/null | head -10 || echo "No updates or pip not available"
fi

# Node 依赖（如果有）
echo "=== Node Dependencies ==="
if [ -f "package.json" ]; then
  npm outdated 2>/dev/null | head -10 || echo "No updates or npm not available"
fi

# Git submodules
echo "=== Git Submodules ==="
git submodule status 2>/dev/null || echo "No submodules"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Dependency check complete" >> /home/zous/clawd/.logs/dependency-updates.log

echo "=== Check Complete ==="
