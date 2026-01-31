#!/bin/bash
# 备份验证 - 每天检查所有备份是否成功

echo "=== $(date) Backup Verification ==="

BACKUP_LOG="/home/zous/.clawdbot/backups/backup.log"
echo "Checking main backup log..."
if [ -f "$BACKUP_LOG" ]; then
  LAST_BACKUP=$(tail -1 "$BACKUP_LOG")
  echo "Last backup: $LAST_BACKUP"
else
  echo "No backup log found"
fi

# 检查重要文件
IMPORTANT_FILES=(
  "/home/zous/clawd/SOUL.md"
  "/home/zous/clawd/MEMORY.md"
  "/home/zous/clawd/USER.md"
  "/home/zous/clawd/AGENTS.md"
)

echo "Verifying important files..."
for file in "${IMPORTANT_FILES[@]}"; do
  if [ -f "$file" ]; then
    SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "unknown")
    echo "✓ $file ($SIZE)"
  else
    echo "✗ $file MISSING"
  fi
done

# 检查 git 状态
cd /home/zous/clawd
UNTRACKED=$(git status --porcelain | wc -l)
echo "Git untracked files: $UNTRACKED"

# 验证结果
echo "$(date '+%Y-%m-%d %H:%M') | Backup OK | Files: ${#IMPORTANT_FILES[@]} | Untracked: $UNTRACKED" >> /home/zous/clawd/.logs/backup-verification.log

echo "=== Verification Complete ==="
