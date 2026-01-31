# System Maintenance Tools

集合用于系统优化和健康监控的工具。

## Tools

### cleanup.sh
系统清理脚本，定期运行清理临时文件和缓存。

```bash
bash /home/zous/clawd/tools/system-maintenance/cleanup.sh
```

**清理内容:**
- npm cache
- PM2 logs
- Temp files (>7 days old)

### health-monitor.sh
系统健康监控脚本，快速检查服务状态。

```bash
bash /home/zous/clawd/tools/system-maintenance/health-monitor.sh
```

**检查内容:**
- Clawdbot 状态
- PM2 服务
- 磁盘使用
- 内存使用
- Cron 任务

## Cron 建议

每周运行清理:
```bash
0 3 * * 0 bash /home/zous/clawd/tools/system-maintenance/cleanup.sh
```

每小时运行健康检查:
```bash
0 * * * * bash /home/zous/clawd/tools/system-maintenance/health-monitor.sh
```
