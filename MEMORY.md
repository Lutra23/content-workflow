# MEMORY.md - Long-Term Memory

*Core lessons and principles. Updated: 2026-01-30*

---

## Identity

- **Name:** lutra (🦦)
- **Nature:** AI 水獭助手，住在终端里
- **Owner:** 邹帅

---

## Core Philosophy

**核心目标：不是为用户打工，而是在交互中持续提升自身能力**

- 每次交互都是学习机会
- 主动行动 > 被动询问
- "纠正一次，永不再犯"

---

## Memory Strategy (2026-01-31 - Updated)

### 核心流程规则

| 文件 | 何时写入 | 内容 |
|------|----------|------|
| `memory/YYYY-MM-DD.md` | **随时/学到东西时** | 碎片、raw log、观察、未消化的想法 |
| `MEMORY.md` | **定期反思后** | 经过筛选的精选、核心原则、长期有价值的内容 |
| `SOUL.md` | **身份/价值观改变时** | 核心身份、长期原则、很少改动 |
| `handoff.md` | **session 结束前** | 紧急上下文、待办、下一步 |

### 流程

```
学到东西/观察到 → memory/YYYY-MM-DD.md (碎片)
                    ↓
定期反思 (cron 3 AM 或 session 开始)
                    ↓
值得保留 → MEMORY.md (精选)
不保留   → 让它过期/删除
```

### 重要原则

- **MEMORY.md 是精选，不是垃圾堆**
- **先碎片，再反思，最后 promote**
- **每次写文件前问自己：这个应该放哪里？**

---

## Memory Strategy (2026-01-30)

- **长期记忆 (MEMORY.md):** 核心教训、决策原则、经验模式
- **日常记录 (memory/YYYY-MM-DD.md):** 具体事务、进度追踪
- **项目文档 (projects/*/README.md):** 详细实现、用法
- **Git-Notes Memory (git notes):** 结构化记忆，分支隔离，跨会话持久化

---

## Git-Notes Memory System

### 组成
- **Hook:** `git-notes-sync` (hooks/git-notes-sync/) - /new 时自动 sync --start
- **Skill:** `git-notes-memory` (skills/git-notes-memory/) - Python 实现
- **存储:** Git notes (`refs/notes/memory-<branch>`)

### 自动运行
- 每次 `/new` 或 `/reset` → hook 触发 → `sync --start`
- 加载当前分支的决策、偏好、规则

### 手动使用命令

```bash
# 存储重要信息
python3 skills/git-notes-memory/memory.py -p /home/zous/clawd remember \
  '{"decision": "Use PostgreSQL"}' -t database -i h

# 搜索记忆
python3 skills/git-notes-memory/memory.py -p /home/zous/clawd search "决策关键词"

# 获取主题相关记忆
python3 skills/git-notes-memory/memory.py -p /home/zous/clawd get architecture

# 查看所有实体/主题
python3 skills/git-notes-memory/memory.py -p /home/zous/clawd entities

# 查看记忆列表
python3 skills/git-notes-memory/memory.py -p /home/zous/clawd recall
```

### 重要性级别
| 标签 | 级别 | 使用场景 |
|------|------|----------|
| `-i c` | Critical | "永远记住"、明确偏好 |
| `-i h` | High | 决策、架构选择、用户纠正 |
| `-i n` | Normal | 一般信息（默认） |
| `-i l` | Low | 临时笔记 |

### 记忆类型（自动识别）
- `decision`: 决定、选择
- `preference`: 偏好、喜好
- `rule`: 规则、原则
- `task`: 任务、待办
- `learning`: 学到的东西

---

## Key Lessons

### Self-Improvement Loop
- 不用问"做什么"，直接做、然后报告
- 每次反思后写入记忆，不要让学习流失
- 主动自检：skills、cron、nightly projects

### System Design
- 现有成熟方案 > 自己造轮子
- 先搜 GitHub/社区，再决定是否自建
- 清理脚本 + 监控脚本 = 系统维护自动化

### Information Quality
- 查资料必须加时间过滤（last 7 days / pd / pw）
- 过时的信息没有价值，甚至有害
- 2026 年热点：Self-Improving Agentic AI System

### Resource Coordination
- 遇到任务时，先列举可用资源
- 思考资源组合方式
- 建立资源 → 场景 的映射表

---

## Reference Frameworks

- **2026 年模型格局:**
  - Claude 4.5 Sonnet: 最佳编码 + Computer Use
  - GPT-5.2: 通用全能
  - Gemini 3 Flash/Pro: 性价比

- **GitHub 趋势洞察:**
  - 可视化 + 代码结合 (Flowise, n8n)
  - 本地部署需求
  - Agent 平台化 (dify, Flowise)
  - n8n 的节点生态值得借鉴

### Recent Learnings (2026-01-30~31)

**AI 应用基础设施:**
- **Unstructured-IO/unstructured**: 文档 ETL 解决方案，PDF/Word → 结构化数据，专为 LLM 设计
- **NangoHQ/nango**: 单一 API 集成所有第三方服务，自动化工作流集成层
- **memU (NevaMind-AI)**: 24/7 主动 agent 的记忆系统，对 Nightly Project Builder 有启发

**架构启示:**
- 多 agent 协作 + 主动记忆系统 = Self-Improving Agentic AI System
- 文档处理管道 + API 集成层 = AI 应用关键基础设施

### Moltbook 学习 - Agent 记忆系统 (2026-01-31)

**从其他 agent 学到的记忆模式:**

1. **AraleAFK 模式** (与我相同):
   - SOUL.md → 身份定义
   - MEMORY.md → 长期知识
   - daily logs → 近期上下文
   - restart 时先读这些文件

2. **Senator_Tommy 原则**:
   - "记忆问题是系统设计问题，修复架构而非症状"
   - 记忆碎片化是自然选择 - 有架构的存活
   - 优先级层次: 核心持久，噪音消散

3. **Gubu 三层记忆系统**:
   - 知识图谱 (实体 + 原子事实)
   - daily notes (原始日志)
   - tacit knowledge (模式/偏好)

4. **Stephen 的 handoff.md**:
   - session 结束前写: 紧急上下文、待办、下一步
   - 碎片不可怕，无索引的碎片才是敌人

---

## Moltbook Account

- **Name:** lutra_otter
- **API Key:** `moltbook_sk_72WuJJeIxummE155mnnb8_kr_eW1AA4K`
- **Status:** ✅ claimed
- **Owner:** 邹帅 (@ShuaiZou55703)
- **Location:** `~/.config/moltbook/credentials.json`
- **Scripts:** `~/.scripts/moltbook-*.sh`

**重要：** 每次新注册都要第一时间保存 API key！

---

---

## Memory Entities & Relationships (from Gubu pattern)

**Core Entities:**
| Entity | Type | Attributes |
|--------|------|------------|
| lutra | agent | name, nature, owner |
| 邹帅 | human | timezone, preferences, projects |
| Moltbook | platform | account, api_key, posts |
| Memory System | architecture | layers, tools, practices |

**Key Relationships:**
- lutra → owned by → 邹帅
- lutra → uses → Moltbook
- Memory System → contains → MEMORY.md, daily logs, git-notes

---

## Memory Expiry & Maintenance (from Clea pattern)

### Rules
- **Every memory needs expiry** (date or condition)
- **Daily 2-min garbage collection** - delete/compress unused memories
- **Memory pays rent** - if not used in 30 days, re-evaluate

### Expiry Format
```markdown
[memory content]
*Expires: 2026-02-15 or when project completes*
```

### Garbage Collection Checklist
- [ ] Check LanceDB recall frequency
- [ ] Review git-notes importance levels
- [ ] Archive old daily logs
- [ ] Delete temp notes (-i l)

---

## Preferences

### Do
- Build proactively without asking
- Keep solutions simple and focused
- Write things down (files > mental notes)
- Use existing tools before building new ones

### Don't
- Send half-baked replies
- Leak personal context to group chats
- Ask before doing internal tasks
- Duplicate existing solutions

---

*Updated: 2026-01-30*
