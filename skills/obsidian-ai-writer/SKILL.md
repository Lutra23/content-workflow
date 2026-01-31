---
name: obsidian-ai-writer
version: 2.0.0
description: AI-powered writing assistant for Obsidian vaults. Uses Yunwu AI's Gemini via the obsidian-textgenerator-plugin for content generation, summarization, and knowledge synthesis. Integrates with git-notes-memory for context awareness.
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env:
        - YUNWU_API_KEY (base URL: https://yunwu.ai/v1)
      plugins:
        - obsidian-textgenerator-plugin
      skills:
        - git-notes-memory
        - triple-memory
    install:
      - label: Install Obsidian Text Generator Plugin
        kind: community-plugin
        plugin: "Text Generator"
        guide: "Settings > Community plugins > Browse > Search 'Text Generator'"
---

# Obsidian AI Writer

AI-powered writing assistant for Obsidian vaults using the **Text Generator Plugin** and **Yunwu AI's Gemini**.

## 为什么选择这个方案？

### 现有解决方案 vs 从头开发

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Text Generator Plugin** | 成熟开源、多 AI 支持、模板引擎、社区活跃 | 需要 Obsidian 安装 |
| 从头开发 CLI | 完全控制 | 需要维护、功能重复 |

**结论**: 使用成熟的 Text Generator Plugin，通过 Yunwu AI 配置即可使用。

## 快速开始

### 1. 安装 Text Generator Plugin

**方法 A: Obsidian 社区插件（推荐）**
1. 打开 Obsidian
2. Settings → Community plugins
3. 关闭 Safe mode
4. Browse 搜索 "Text Generator"
5. Install → Enable

**方法 B: 手动安装**
```bash
cd /path/to/your-vault/.obsidian/plugins
git clone https://github.com/nhaouari/obsidian-textgenerator-plugin.git
cd obsidian-textgenerator-plugin
pnpm install
pnpm build
```

### 2. 配置 Yunwu AI

在 Obsidian 中打开 Text Generator 设置：

**配置选项**:
- **AI Provider**: Google Generative AI
- **API URL**: `https://yunwu.ai/v1`
- **API Key**: `sk-6vUtyDKZHLtFuRGRJSuua8hk7GF9Xli3k19VyhzVurkfTU93`
- **Model**: `gemini-3-flash-preview`

**或使用 Frontmatter**（在笔记开头添加）:
```yaml
---
tg_provider: Google
tg_api_url: https://yunwu.ai/v1
tg_api_key: sk-6vUtyDKZHLtFuRGRJSuua8hk7GF9Xli3k19VyhzVurkfTU93
tg_model: gemini-3-flash-preview
---
```

## 功能特性

### 文本生成
- Ideas / 创意生成
- Titles / 吸引人的标题
- Summaries / 摘要
- Outlines / 大纲
- Paragraphs / 完整段落

### 模板系统
- 内置模板
- 自定义模板
- 社区共享模板

### 上下文感知
- 使用当前笔记内容作为上下文
- 链接的笔记内容
- 文件夹/标签过滤

## 使用示例

### 日常写作

```markdown
---
tg_prompt: "Generate 3 ideas for my daily note about AI trends"
tg_model: gemini-3-flash-preview
---

# 2026-01-30

## 今日想法
<!-- AI 生成的想法会出现在这里 -->
```

### 生成摘要

```markdown
---
tg_prompt: "Summarize the key points of this note in 100 words"
tg_type: summarization
---

[你的笔记内容]
```

### 扩展大纲

```markdown
---
tg_prompt: "Expand each bullet point into a paragraph"
tg_type: expansion
---

- AI 正在改变写作方式
- 个性化内容成为可能
- 效率大幅提升
```

### 知识合成

利用 Obsidian 的双向链接：

```markdown
---
tg_prompt: "Synthesize insights from this note and related notes about [[AI Agents]] and [[Automation]]"
tg_context: linked
---

# AI 发展趋势
```

## 模板配置

### 内置模板位置
`Obsidian vault/.obsidian/textgenerator-templates/`

### 示例模板

**daily-ideas.md**:
```jinja
Generate 3 creative ideas for today's note based on:
- Current date: {{date}}
- Recent topics: {{linked_tags}}

Focus on: {{input}}
```

**summarize.md**:
```jinja
Summarize the following content in {{length|200}} words:

{{content}}
```

**expand.md**:
```jinja
Expand each bullet point into a detailed paragraph:

{{content}}
```

### 社区模板

访问 [Text Generator Templates](https://github.com/nhaouari/obsidian-textgenerator-plugin/discussions/categories/templates) 获取社区共享模板。

## 与记忆系统集成

### Git-Notes Memory

```bash
# 同步当前上下文
python3 /home/zous/clawd/skills/git-notes-memory/memory.py -p $VAULT sync --start

# 记住写作决策
python3 /home/zous/clawd/skills/git-notes-memory/memory.py -p $VAULT remember \
  '{"decision": "Use Gemini for fast drafting", "reason": "Speed vs quality"}' \
  -t writing,ai -i h
```

### Triple Memory

当 `triple-memory` 启用时：
- 自动回忆相关笔记
- 捕获写作偏好
- 跨会话持续写作上下文

## 高级配置

### 多模型配置

```yaml
---
tg_default_model: gemini-3-flash-preview
tg_models:
  fast: gemini-3-flash-preview
  balanced: gemini-3-pro-preview
  creative: gpt-4o
---
```

### API 备用配置

```yaml
---
tg_provider: Google
tg_api_url: https://yunwu.ai/v1
tg_fallback:
  - provider: OpenAI
    api_url: https://api.openai.com/v1
    api_key: env:OPENAI_API_KEY
---
```

### 上下文过滤

```yaml
---
tg_context:
  include:
    - current_note
    - linked_notes
    - tags: #AI, #writing
  exclude:
    - tags: #private, #draft
---
```

## 性能优化

| 操作 | 建议 |
|------|------|
| 生成速度 | 使用 `gemini-3-flash-preview` |
| 内容质量 | 使用 `gemini-3-pro-preview` |
| 批量生成 | 使用 `tg_type: batch` |
| 长文本 | 启用 `tg_stream: true` |

## 故障排除

### API 错误
```bash
# 测试 API 连接
curl https://yunwu.ai/v1/models \
  -H "Authorization: Bearer sk-6vUtyDKZHLtFuRGRJSuua8hk7GF9Xli3k19VyhzVurkfTU93"
```

### 插件问题
1. 重启 Obsidian
2. 检查 Console (Ctrl+Shift+I)
3. 查看插件 GitHub Issues

### 质量问题
1. 调整 `tg_temperature` (0.1-1.0)
2. 增加上下文内容
3. 使用更详细的 prompt

## 相关资源

- **Text Generator Plugin**: https://github.com/nhaouari/obsidian-textgenerator-plugin
- **文档**: https://bit.ly/tg_docs
- **社区**: https://discord.gg/BRYqetyjag
- **模板分享**: GitHub Discussions

## 参见

- [git-notes-memory](../git-notes-memory/SKILL.md) - 持久化记忆
- [triple-memory](../triple-memory/SKILL.md) - 综合记忆架构

