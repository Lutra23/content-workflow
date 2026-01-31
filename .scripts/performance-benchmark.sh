#!/bin/bash
# 性能基准测试 - 每周 2 次运行性能测试

echo "=== $(date) Performance Benchmark ==="

cd /home/zous/clawd

# 启动时间测量
START=$(date +%s%N)

# 模拟一些操作
echo "Running benchmark tasks..."

# 简单文件操作测试
FILE_COUNT=$(find . -type f 2>/dev/null | wc -l)
echo "File count: $FILE_COUNT"

# Python 导入测试
IMPORT_TIME=$(python3 -c "import time; start=time.time(); import json, subprocess, os, sys; print(time.time()-start)" 2>/dev/null || echo "N/A")
echo "Python import time: ${IMPORT_TIME}s"

# 结束时间测量
END=$(date +%s%N)
DURATION=$(( (END - START) / 1000000 ))
echo "Total benchmark duration: ${DURATION}ms"

# 记录基准
echo "$(date '+%Y-%m-%d %H:%M') | Files: $FILE_COUNT | Import: ${IMPORT_TIME}s | Duration: ${DURATION}ms" >> /home/zous/clawd/.logs/performance-benchmark.log

echo "=== Benchmark Complete ==="
