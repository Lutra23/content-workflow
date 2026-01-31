#!/bin/bash
# 代码质量扫描 - 每周 2 次扫描代码质量

echo "=== $(date) Code Quality Scan ==="

PROJECT_DIR="/home/zous/clawd"

# 检查 TODO/FIXME 注释
TODOS=$(grep -r "TODO\|FIXME\|BUG\|HACK" "$PROJECT_DIR" --include="*.py" --include="*.js" --include="*.md" 2>/dev/null | wc -l)
echo "TODO/FIXME comments: $TODOS"

# 检查代码行数统计
LINES_PY=$(find "$PROJECT_DIR" -name "*.py" -exec wc -l {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
LINES_MD=$(find "$PROJECT_DIR" -name "*.md" -exec wc -l {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
echo "Lines of Python: $LINES_PY"
echo "Lines of Markdown: $LINES_MD"

# 检查测试覆盖率（如果有）
if [ -f "coverage.xml" ]; then
  COVERAGE=$(grep -o 'line-rate="[0-9.]*" coverage.xml | grep -o '[0-9.]*' || echo "N/A")
  echo "Test coverage: $COVERAGE%"
fi

# 检查依赖更新
echo "Checking for dependency updates..."
pip list --outdated 2>/dev/null | head -5 || echo "No pip or no updates"

# 扫描结果日志
echo "$(date '+%Y-%m-%d %H:%M') | TODOs: $TODOS | Python: $LINES_PY | Markdown: $LINES_MD" >> /home/zous/clawd/.logs/code-quality.log

echo "=== Scan Complete ==="
