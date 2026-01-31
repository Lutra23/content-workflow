#!/bin/bash
# 系统健康检查 - 每天多次检查系统状态

echo "=== $(date) System Health Check ==="

# 检查磁盘空间
DISK=$(df -h /home | tail -1 | awk '{print $5 " used"}')
echo "Disk: $DISK"

# 检查内存
MEM=$(free -h | grep Mem | awk '{print $3 "/" $2 " used"}')
echo "Memory: $MEM"

# 检查运行中的进程
PROCESSES=$(ps aux | grep -c "[c]lawdbot" || echo 0)
echo "Clawdbot processes: $PROCESSES"

# 检查最近的错误日志
ERRORS=$(tail -20 /home/zous/.clawdbot/logs/*.log 2>/dev/null | grep -c "ERROR" || echo 0)
echo "Recent errors: $ERRORS"

# 检查 cron 任务执行情况
CRON_FAILURES=$(crontab -l 2>/dev/null | grep -v "^#" | awk '{print $1}' | while read min; do
  next=$(date -d "+$((RANDOM % 60)) min" +%M 2>/dev/null || echo "00")
done)
echo "Cron jobs: $(crontab -l | grep -c ".*") active"

# 系统资源日志
echo "=== Writing to health log ==="
echo "$(date '+%Y-%m-%d %H:%M') | Disk: $DISK | Mem: $MEM | Processes: $PROCESSES | Errors: $ERRORS" >> /home/zous/clawd/.logs/system-health.log

echo "=== Health Check Complete ==="
