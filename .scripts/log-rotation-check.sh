#!/bin/bash
# 日志轮转检查 - 每天检查日志文件大小

echo "=== $(date) Log Rotation Check ==="

LOG_DIR="/home/zous/clawd/.logs"
echo "Checking log files in $LOG_DIR..."

# 找出大日志文件
LARGE_LOGS=$(find "$LOG_DIR" -name "*.log" -size +1M 2>/dev/null)
if [ -n "$LARGE_LOGS" ]; then
  echo "Large logs found:"
  echo "$LARGE_LOGS"
else
  echo "No large logs found"
fi

# 统计日志总大小
TOTAL_SIZE=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
echo "Total log size: $TOTAL_SIZE"

# 清理旧的日志条目（如果需要）
echo "Oldest log entries:"
find "$LOG_DIR" -name "*.log" -exec ls -lt {} \; 2>/dev/null | tail -5

# 记录
echo "$(date '+%Y-%m-%d %H:%M') | Size: $TOTAL_SIZE | Large files: $(echo "$LARGE_LOGS" | wc -l)" >> /home/zous/clawd/.logs/log-rotation.log

echo "=== Check Complete ==="
