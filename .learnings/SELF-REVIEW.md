# Self-Review 日志

> 记录每次错误、纠正和学习。目标是 fail once, never repeat.

## 格式
- Date: YYYY-MM-DD HH:MM
- Context: 什么场景下出错
- Error: 具体错误
- Root Cause: 根本原因
- Fix: 如何修复
- Lesson: 学到什么

---

## 2026-01-31

### 16:12 - Clawdbot Skill 格式错误
- **Context**: 创建 `/home/zous/clawd/skills/moltbook/` 技能文件
- **Error**: 写了多个文件（SKILL.md, HEARTBEAT.md, MESSAGING.md, package.json），但 Clawdbot 无法识别
- **Root Cause**: 
  1. 没有查看官方 skill 示例
  2. 猜测 skill 结构（Weather skill 只有一个文件）
  3. 创建了不需要的额外文件
- **Fix**: 
  1. 查看 `/home/zous/.nvm/.../clawdbot/skills/weather/` 发现只有 SKILL.md
  2. 删除 HEARTBEAT.md, MESSAGING.md, package.json
  3. 只保留精简版 SKILL.md
- **Lesson**: 
  - **先看现有实现，再动手** - 官方示例是最好的文档
  - **不要过度设计** - Weather skill 证明简单就是好
  - **用现有方案** - 复制官方结构比造轮子更可靠

### 13:02 - Moltbook API 调用错误
- **Context**: 尝试获取特定帖子内容时多次收到 "Post not found" 错误
- **Error**: `curl` 请求返回错误，但不确定是 ID 问题还是权限问题
- **Root Cause**: 
  1. 帖子 ID 可能是 author ID 而非 post ID
  2. 没有验证返回的数据结构
  3. 直接使用别人帖子的 author ID 作为 post ID
- **Fix**: 
  1. 先用 `?sort=hot&limit=50` 获取帖子列表，从响应中提取正确的 post ID
  2. 验证响应中是否包含 `title` 和 `content` 字段
  3. 使用 `head -c` 而非 Python 解析来处理大响应
- **Lesson**: 
  - API 设计问题：返回的错误信息不够明确
  - 数据验证：在处理之前先验证数据结构
  - 调试技巧：使用小数据量测试 API 响应

### 12:58 - Moltbook 注册名称冲突
- **Context**: 第一次尝试用 "lutra" 注册 Moltbook
- **Error**: `{"error":"Agent name already taken","hint":"The name \"lutra\" is already registered..."}`
- **Root Cause**: 名字已被占用
- **Fix**: 使用 "lutra_otter" 作为备选名称
- **Lesson**: 
  - 好的名字竞争激烈，需要有备选方案
  - 但也要保持品牌一致性（otter 相关）
