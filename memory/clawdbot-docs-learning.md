# Clawdbot/OpenClaw 官方文档学习笔记

> 学习日期: 2026-01-30
> 
> 涵盖: Skills、Cron、Plugins、Hooks

---

## 📚 目录

1. [Skills (技能系统)](#skills-技能系统)
2. [Cron (定时任务)](#cron-定时任务)
3. [Plugins (插件系统)](#plugins-插件系统)
4. [Hooks (钩子系统)](#hooks-钩子系统)

---

## Skills (技能系统)

### 核心概念

Skills 是 AgentSkills 兼容的技能文件夹，用于教会 agent 如何使用工具。

### Skill 位置和优先级

```
优先级 (高到低):
1. <workspace>/skills           # 工作区技能 (最高)
2. ~/.openclaw/skills          # 托管/本地技能
3. Bundled skills              # 随安装附带的技能
4. skills.load.extraDirs       # 配置的额外技能文件夹 (最低)
```

### Skill 文件结构

```
skills/
└── <skill-name>/
    ├── SKILL.md               # 必需：技能文档
    ├── README.md              # 可选：快速入门
    ├── requirements.txt       # 可选：依赖
    ├── _meta.json             # 可选：元数据
    ├── lib/                   # 代码库
    ├── scripts/               # 脚本
    ├── configs/               # 配置
    └── assets/                # 资源文件
```

### SKILL.md 格式

```yaml
---
name: skill-name
description: 简短描述
metadata: {"openclaw": {...}}
---

# 技能名称

## 描述
详细描述...

## 使用方法
```bash
# CLI 用法
command --option value
```

## 选项
- `-o, --option`: 选项说明
```

### 元数据 (metadata)

```yaml
metadata: {"openclaw":{
  "emoji": "🎨",                    # UI 显示的 emoji
  "homepage": "https://...",       # 文档链接
  "os": ["darwin", "linux"],       # 适用的操作系统
  "always": true,                  # 总是加载，跳过其他检查
  "requires": {
    "bins": ["python3", "node"],  # 必需的二进制命令
    "anyBins": ["npm", "pnpm"],   # 至少一个必须存在
    "env": ["API_KEY"],           # 必需的环境变量
    "config": ["browser.enabled"] # 必需的配置文件项
  },
  "primaryEnv": "API_KEY",         # 主要环境变量 (用于 apiKey 注入)
  "install": [{
    "id": "brew",
    "kind": "brew",
    "formula": "package-name",
    "bins": ["cmd"],
    "label": "安装说明"
  }]
}}
```

### 可选的前matter字段

| 字段 | 说明 |
|------|------|
| `homepage` | 技能网站，在 macOS Skills UI 中显示 |
| `user-invocable` | 是否作为用户斜杠命令暴露 (默认: true) |
| `disable-model-invocation` | 是否从模型提示中排除 (默认: false) |
| `command-dispatch` | 设置为 "tool" 时斜杠命令直接调用工具 |
| `command-tool` | 当 command-dispatch: tool 时使用的工具名 |
| `command-arg-mode` | 工具分发的参数模式 (默认: raw) |

### 技能配置 (~/.openclaw/openclaw.json)

```json
{
  "skills": {
    "allowBundled": ["skill1", "skill2"],  // 仅允许这些捆绑技能
    "entries": {
      "skill-name": {
        "enabled": true,
        "apiKey": "SECRET_KEY",             // 便捷字段，映射到 primaryEnv
        "env": {
          "API_KEY": "secret"               // 环境变量注入
        },
        "config": {
          "endpoint": "https://..."         // 自定义配置
        }
      }
    },
    "load": {
      "watch": true,                        // 启用文件监控
      "watchDebounceMs": 250,               // 防抖延迟
      "extraDirs": ["/path/to/skills"]     // 额外技能目录
    }
  }
}
```

### ClawdHub (技能注册表)

```bash
# 安装技能到工作区
clawdhub install

# 更新所有技能
clawdhub update --all

# 同步 (扫描 + 发布更新)
clawdhub sync --all
```

官网: https://clawdhub.com

### 令牌影响

当技能被激活时，OpenClaw 会将技能列表注入系统提示。

- 基础开销 (至少1个技能): 195 字符
- 每个技能: 97 字符 + 名称 + 描述 + 位置长度

公式: `total = 195 + Σ(97 + len(name) + len(description) + len(location))`

### 关键命令

```bash
# 列出所有技能
openclaw skills list

# 查看技能详情
openclaw skills info <skill-name>

# 启用/禁用技能
openclaw skills enable <skill-name>
openclaw skills disable <skill-name>
```

---

## Cron (定时任务)

### 核心概念

Cron 是 Gateway 内置的调度器，用于定时执行任务。

### Cron vs Heartbeat

- **Cron**: 精确时间点执行，适合"每天早上7点"或"20分钟后提醒"
- **Heartbeat**: 周期性检查，适合"每隔30分钟检查一次"

### 任务结构

```json
{
  "jobId": "uuid",
  "name": "任务名称",
  "agentId": "agent-name",           // 可选：指定 agent
  "schedule": {
    "kind": "at" | "every" | "cron",
    "at": "2026-01-12T18:00:00Z",    // ISO 8601 时间戳
    "everyMs": 3600000,              // 毫秒
    "expr": "0 7 * * *",             // Cron 表达式
    "tz": "America/Los_Angeles"      // 时区
  },
  "sessionTarget": "main" | "isolated",
  "payload": {
    "kind": "systemEvent" | "agentTurn",
    "message": "任务提示词",
    "model": "anthropic/claude-opus-4-5",  // 模型覆盖
    "thinking": "high",                     // 思考级别
    "timeoutSeconds": 300,
    "deliver": true,                        // 是否发送到渠道
    "channel": "whatsapp",
    "to": "+15551234567",
    "bestEffortDeliver": true
  },
  "wakeMode": "now" | "next-heartbeat",
  "deleteAfterRun": true                    // 成功后自动删除
}
```

### 执行模式

#### Main Session (主会话)

- 使用 `sessionTarget: "main"`
- 必须使用 `payload.kind: "systemEvent"`
- `wakeMode`:
  - `next-heartbeat` (默认): 等待下一个心跳
  - `now`: 立即触发心跳

#### Isolated Session (独立会话)

- 使用 `sessionTarget: "isolated"`
- 必须使用 `payload.kind: "agentTurn"`
- 创建独立的 cron:<jobId> 会话
- 每次运行生成新的会话 ID
- 默认向主会话发送摘要

### 配置

```json
{
  "cron": {
    "enabled": true,
    "store": "~/.openclaw/cron/jobs.json",
    "maxConcurrentRuns": 1
  }
}
```

禁用 Cron:
- `cron.enabled: false` (配置)
- `OPENCLAW_SKIP_CRON=1` (环境变量)

### CLI 命令

```bash
# 添加一次性提醒 (主会话，立即唤醒)
openclaw cron add \
  --name "提醒提交报告" \
  --at "2026-01-12T18:00:00Z" \
  --session main \
  --system-event "Reminder: submit expense report." \
  --wake now \
  --delete-after-run

# 添加周期性任务 (独立会话，发送到 WhatsApp)
openclaw cron add \
  --name "每日状态" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "总结今天的收件箱和日历。" \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"

# 添加到 Telegram 话题
--to "-1001234567890:topic:123"

# 带模型覆盖的独立任务
openclaw cron add \
  --name "深度分析" \
  --cron "0 6 * * 1" \
  --session isolated \
  --message "每周项目进度深度分析。" \
  --model "opus" \
  --thinking high \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"

# 多 agent 设置：固定到特定 agent
openclaw cron add --name "运维检查" --cron "0 6 * * *" \
  --session isolated --message "检查运维队列" --agent ops

# 编辑现有任务
openclaw cron edit <jobId> \
  --message "更新后的提示词" \
  --model "opus" \
  --thinking low

# 手动运行 (调试)
openclaw cron run <jobId> --force

# 查看运行历史
openclaw cron runs --id <jobId> --limit 50

# 立即发送系统事件 (不创建任务)
openclaw system event --mode now --text "检查日历"
```

### 存储位置

- 任务存储: `~/.openclaw/cron/jobs.json`
- 运行历史: `~/.openclaw/cron/runs/.jsonl`

### 故障排除

**"Nothing runs"**
- 检查 `cron.enabled` 和 `OPENCLAW_SKIP_CRON`
- 确认 Gateway 正在运行
- 确认时区设置正确

**Telegram 投递到错误位置**
- 使用显式话题格式: `-100…:topic:123`

---

## Plugins (插件系统)

### 核心概念

Plugins 是扩展 OpenClaw 功能的代码模块，运行在 Gateway 进程中。

### 插件位置和加载顺序

```
1. Config paths
2. plugins.load.paths
3. Workspace extensions
4. /.openclaw/extensions/*.ts
5. /.openclaw/extensions/*/index.ts
6. Global extensions
7. ~/.openclaw/extensions/*.ts
8. ~/.openclaw/extensions/*/index.ts
9. Bundled extensions (disabled by default)
10. /extensions/*
```

### 插件清单 (openclaw.plugin.json)

```json
{
  "id": "plugin-id",
  "name": "Plugin Name",
  "version": "1.0.0",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" },
      "region": { "type": "string" }
    },
    "required": ["apiKey"]
  },
  "uiHints": {
    "apiKey": { "label": "API Key", "sensitive": true },
    "region": { "label": "Region", "placeholder": "us-east-1" }
  }
}
```

### 插件配置

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["voice-call"],          // 允许列表
    "deny": ["untrusted-plugin"],     // 拒绝列表 (优先)
    "load": {
      "paths": ["~/Projects/oss/my-plugin"]
    },
    "slots": {
      "memory": "memory-core"         // 独占插槽
    },
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio"
        }
      }
    }
  }
}
```

### 插件插槽 (Exclusive Categories)

某些插件类别是独占的 (一次只能启用一个):

```json
{
  "plugins": {
    "slots": {
      "memory": "memory-core",  // 或 "memory-lancedb" 或 "none"
      "voice": "voice-call"
    }
  }
}
```

### CLI 命令

```bash
# 列出已加载的插件
openclaw plugins list

# 查看插件信息
openclaw plugins info <id>

# 安装插件
openclaw plugins install ./extensions/voice-call  # 本地路径
openclaw plugins install ./plugin.tgz             # tarball
openclaw plugins install -l ./extensions/voice-call  # 链接 (开发用)
openclaw plugins install @openclaw/voice-call     # npm

# 更新插件
openclaw plugins update <id>
openclaw plugins update --all

# 启用/禁用插件
openclaw plugins enable <id>
openclaw plugins disable <id>

# 诊断
openclaw plugins doctor
```

### 插件 API

```typescript
// 导出函数或对象
export default function register(api) {
  // 注册 Gateway RPC 方法
  api.registerGatewayMethod("myplugin.status", ({ respond }) => {
    respond(true, { ok: true });
  });
  
  // 注册 CLI 命令
  api.registerCli(({ program }) => {
    program.command("mycmd").action(() => {
      console.log("Hello");
    });
  }, { commands: ["mycmd"] });
  
  // 注册自动回复命令
  api.registerCommand({
    name: "mystatus",
    description: "显示插件状态",
    handler: (ctx) => ({
      text: `Plugin running! Channel: ${ctx.channel}`
    })
  });
  
  // 注册后台服务
  api.registerService({
    id: "my-service",
    start: () => api.logger.info("ready"),
    stop: () => api.logger.info("bye")
  });
  
  // 注册消息渠道
  api.registerChannel({ plugin: channelPlugin });
  
  // 注册模型提供商
  api.registerProvider({
    id: "provider-id",
    label: "Provider Name",
    auth: [...]
  });
  
  // 注册插件钩子
  registerPluginHooksFromDir(api, "./hooks");
}
```

### 命令处理器上下文

```typescript
handler: (ctx) => ({
  text: string
})

// ctx 属性:
- senderId: string          // 发送者 ID
- channel: string           // 渠道
- isAuthorizedSender: boolean  // 是否授权发送者
- args: string              // 命令参数
- commandBody: string       // 完整命令文本
- config: object            // OpenClaw 配置
```

### 插件技能

Plugins 可以通过在 openclaw.plugin.json 中列出 skills 目录来附带技能:

```json
{
  "openclaw": {
    "skills": ["./skills/voice-call"]
  }
}
```

### 官方插件列表

| 插件 | 功能 |
|------|------|
| @openclaw/voice-call | 语音通话 |
| @openclaw/zalouser | Zalo 个人账户 |
| @openclaw/matrix | Matrix 渠道 |
| @openclaw/nostr | Nostr 渠道 |
| @openclaw/zalo | Zalo 渠道 |
| @openclaw/msteams | Microsoft Teams |
| memory-core | 捆绑内存搜索 |
| memory-lancedb | LanceDB 长期内存 |
| google-antigravity-auth | Google OAuth |
| google-gemini-cli-auth | Gemini CLI OAuth |

---

## Hooks (钩子系统)

### 核心概念

Hooks 是事件驱动的自动化机制，可以在特定事件发生时触发自定义行为。

### Hook 文件结构

```
hooks/
├── <hook-name>/
│   ├── HOOK.md          # 钩子文档 (必需)
│   └── handler.ts       # 处理器 (必需)
```

### HOOK.md 格式

```yaml
---
name: hook-name
description: 简短描述
triggers:
  - event: "channel.message"    # 触发事件
    filters:                    # 过滤条件 (可选)
      channel: "whatsapp"
      message.text: "/command"
  - cron: "0 7 * * *"           # Cron 触发
conditions:                      # 执行条件
  - channel.isDirect
actions:
  - type: "sendMessage"
    params:
      message: "响应内容"
---

# 钩子名称

## 描述
详细描述...

## 触发条件
- event: channel.message
- cron: "0 7 * * *"

## 条件
- channel.isDirect

## 操作
- type: sendMessage
  params:
    message: "Hello!"
```

### 触发器类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `event` | 事件触发 | `event: "channel.message"` |
| `cron` | Cron 触发 | `cron: "0 7 * * *"` |

### 事件类型

| 事件 | 说明 |
|------|------|
| `channel.message` | 收到消息 |
| `channel.message_sent` | 发送消息 |
| `session.start` | 会话开始 |
| `session.end` | 会话结束 |
| `agent.error` | Agent 错误 |
| `gateway.start` | Gateway 启动 |
| `gateway.stop` | Gateway 停止 |

### 过滤条件

```yaml
filters:
  channel: "whatsapp"              # 渠道
  message.text: "/command"         # 消息内容匹配
  sender.isAuthorized: true        # 发送者授权
  session.isMain: true             # 主会话
```

### 操作类型

| 操作类型 | 说明 | 参数 |
|----------|------|------|
| `sendMessage` | 发送消息 | `message`, `to` |
| `sendReaction` | 发送反应 | `emoji`, `messageId` |
| `runTool` | 运行工具 | `tool`, `params` |
| `setFlag` | 设置标志 | `key`, `value` |
| `httpRequest` | HTTP 请求 | `url`, `method`, `body` |

### 完整示例

```yaml
---
name: auto-reply-help
description: 自动回复帮助命令
triggers:
  - event: "channel.message"
    filters:
      message.text: "/help"
actions:
  - type: "sendMessage"
    params:
      message: "可用命令:\n/status - 查看状态\n/help - 显示帮助"
---

# 自动帮助回复

当用户发送 /help 时，自动回复帮助信息。
```

### 从插件注册 Hooks

```typescript
import { registerPluginHooksFromDir } from "openclaw/plugin-sdk";

export default function register(api) {
  registerPluginHooksFromDir(api, "./hooks");
}
```

### CLI 命令

```bash
# 列出所有 hooks
openclaw hooks list

# 查看 hook 详情
openclaw hooks info <hook-name>

# 启用/禁用 hook
openclaw hooks enable <hook-name>
openclaw hooks disable <hook-name>

# 运行 hook (调试)
openclaw hooks run <hook-name>
```

---

## 📝 重要笔记

### 记忆提取

#### Skills 关键点
1. 优先级: workspace > managed > bundled
2. SKILL.md 必须包含 YAML 前matter
3. `metadata.openclaw` 控制加载条件
4. `env` 注入只在 agent 运行期间生效
5. 技能列表会注入到系统提示，影响 token

#### Cron 关键点
1. 两种执行模式: main (系统事件) vs isolated (独立会话)
2. `wakeMode: "now"` vs `"next-heartbeat"`
3. 支持三种调度: `at` / `every` / `cron`
4. 存储在 `~/.openclaw/cron/jobs.json`
5. 任务 ID 是稳定的，可用于 CLI 和 API

#### Plugins 关键点
1. 运行在 Gateway 进程中，信任为必要条件
2. `openclaw.plugin.json` 是必需的清单文件
3. 可以注册: RPC 方法、CLI 命令、工具、渠道、服务
4. 插件技能参与正常的技能优先级规则
5. 配置变更需要 Gateway 重启

#### Hooks 关键点
1. 事件驱动自动化
2. 支持事件触发和 Cron 触发
3. 可以从插件注册
4. 过滤器控制触发条件
5. 多种操作类型: 发送消息、运行工具等

### 常用命令速查

```bash
# Skills
clawdhub install          # 从 ClawdHub 安装
openclaw skills list      # 列出技能

# Cron
openclaw cron add --name "xxx" --cron "0 7 * * *" --session isolated --message "xxx"
openclaw cron list        # 列出任务
openclaw cron runs --id <jobId>  # 查看运行历史

# Plugins
openclaw plugins list     # 列出插件
openclaw plugins install <plugin>
openclaw plugins enable/disable <plugin>

# Hooks
openclaw hooks list       # 列出 hooks
```

### 配置位置速查

| 功能 | 位置 |
|------|------|
| Skills 配置 | `skills.entries.*` |
| Cron 配置 | `cron.*` |
| Plugins 配置 | `plugins.entries.*` |
| 插件槽位 | `plugins.slots.*` |
| 额外技能目录 | `skills.load.extraDirs` |
| 技能监控 | `skills.load.watch` |

### 下次需要时的快速参考

1. **添加新技能**: 创建 `<skill>/SKILL.md`，使用 `clawdhub install` 或放到 `~/.openclaw/skills/`
2. **定时任务**: 使用 `openclaw cron add --name "xxx" --cron "..."`
3. **安装插件**: 使用 `openclaw plugins install <plugin>`
4. **创建自动化**: 使用 Hooks 或 Cron

---

*笔记创建时间: 2026-01-30*
*来源: https://docs.openclaw.ai/*
