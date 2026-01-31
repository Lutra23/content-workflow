#!/bin/bash
# 错误日志分析 - 每天分析错误日志

echo "=== $(date) Error Log Analysis ==="

LOG_DIR="/home/zous/clawd/.logs"

echo "=== Recent Errors ==="
ERROR_COUNT=$(grep -r "ERROR\|Error\|error\|Exception\|FAIL" "$LOG_DIR" 2>/dev/null | wc -l)
echo "Total error mentions: $ERROR_COUNT"

# 找出最常见的错误类型
echo "=== Error Types ==="
grep -r "ERROR\|Error\|error\|Exception\|FAIL" "$LOG_DIR" 2>/dev/null | \
  grep -oE "[A-Za-z]+Error|[A-Za-z]+Exception" | \
  sort | uniq -c | sort -rn | head -10

# 检查 clawdbot 日志
CLAWDBOT_ERRORS=$(tail -100 /home/zous/.clawdbot/logs/*.log 2>/dev/null | grep -c "ERROR" || echo 0)
echo "Clawdbot errors (last 100 lines): $CLAWDBOT_ERRORS"

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Total errors: $ERROR_COUNT | Clawdbot: $CLAWDBOT_ERRORS" >> /home/zous/clawd/.logs/error-analysis.log

echo "=== Analysis Complete ==="
