# Obsidian AI Writer Skill

📝 AI-powered writing for Obsidian using **Text Generator Plugin** + **Yunwu AI**

## 🎯 核心思想

> **不要重复造轮子** - 使用成熟的 Text Generator Plugin，通过 Yunwu AI 配置即可使用。

## 📦 整合来源

| 来源 | 内容 |
|------|------|
| [obsidian-textgenerator-plugin](https://github.com/nhaouari/obsidian-textgenerator-plugin) | 核心插件 |
| Yunwu AI | Gemini API (免费额度) |
| git-notes-memory | 记忆集成 |

## 🚀 快速开始

### 1. 安装插件
1. Obsidian → Settings → Community plugins
2. 关闭 Safe mode
3. Browse 搜索 "Text Generator"
4. Install → Enable

### 2. 配置 Yunwu AI

在笔记 frontmatter 中添加：
```yaml
---
tg_provider: Google
tg_api_url: https://yunwu.ai/v1
tg_api_key: sk-6vUtyDKZHLtFuRGRJSuua8hk7GF9Xli3k19VyhzVurkfTU93
tg_model: gemini-3-flash-preview
---
```

或在插件设置中配置。

### 3. 使用

```markdown
---
tg_prompt: "Generate 3 ideas for today's note about AI"
---

# 今日想法
<!-- AI 生成的内容 -->
```

## 📁 简化后的文件结构

```
obsidian-ai-writer/
├── SKILL.md              # 完整文档
├── README.md             # 本文件
├── config.example.json   # 配置示例
└── scripts/
    └── memory.py         # Git-Notes 集成
```

## ✨ 功能

- ✅ 生成 ideas、标题、摘要、大纲
- ✅ 模板系统（自定义 + 社区模板）
- ✅ 多 AI 支持（Google, OpenAI, Anthropic）
- ✅ 记忆集成（git-notes-memory）
- ✅ 免费开源

## 📖 详细文档

见 [SKILL.md](./SKILL.md)

## 💡 经验教训

**不要重复造轮子！**
- GitHub 上有成熟方案
- 使用现有插件 + 配置即可
- 把精力放在内容和使用上

## 📄 许可

MIT - Created 2026-01-30
