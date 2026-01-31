# 资源调度参考

## 完整资源清单 (30+ skills + 系统资产)

### 🎨 AI 创作 (7)
| Skill | 用途 |
|-------|------|
| ai-image-generator | 图片生成 |
| ai-video-generator | 视频生成 |
| ai-voice-generator | 语音合成 |
| ai-music-generator | 音乐生成 |
| ai-character-consistency | 角色一致性 |
| ai-storyboard-gen | 分镜生成 |
| ai-subtitle-sync | 字幕同步 |

### 🔍 搜索与信息 (5)
| Skill | 用途 | 限制 |
|-------|------|------|
| serpapi | Google/Bing 搜索，rich snippets | 100次/月 |
| tavily-search | AI 优化搜索 | 10 req/min |
| brave-search | 文档搜索 | 需要 API Key |
| read-github | 语义搜索 GitHub 文档 | 无 |
| web_fetch | 抓取 URL 内容 | 无 |

### 💾 记忆与学习 (4)
| Skill | 用途 |
|-------|------|
| triple-memory | 自动记忆注入 (LanceDB + Git-Notes) |
| git-notes-memory | 结构化分支记忆 |
| reflect | 自改进反思 (记录教训) |
| context7 | 获取最新文档 |

### 🛠️ 开发与编程 (6)
| Skill | 用途 |
|-------|------|
| coding-agent | Codex CLI 编程 |
| cursor-agent | IDE 编程 |
| github | Issue/PR/Run 管理 |
| github-pr | PR 本地测试 |
| mcporter | MCP 服务器管理 |
| oracle | 第二模型审查 |

### 📚 内容与媒体 (6)
| Skill | 用途 |
|-------|------|
| summarize | URL/文件摘要 |
| youtube-summarizer | YouTube 摘要 |
| figma | 设计分析导出 |
| agent-browser | 浏览器自动化 |
| tmux | 远程终端控制 |
| weather | 天气查询 |

### 🔗 集成与平台 (5)
| Skill | 用途 |
|-------|------|
| notion | Notion API |
| slack | Slack 控制 |
| bluebubbles | iMessage 集成 |
| clawdhub | 技能市场 |
| skill-creator | 创建新技能 |

### 📊 系统工具 (2)
| 工具 | 用途 |
|------|------|
| cleanup.sh | 系统清理 (npm cache, logs) |
| health-monitor.sh | 健康检查 (Clawdbot + PM2) |

## 🚀 组合工作流

### 场景 1: AI 新闻简报
```
 serpapi (搜索) → tavily (验证) → summarize (摘要) → newsletter (生成)
```

### 场景 2: 代码开发任务
```
 github (查问题) → cursor-agent (编码) → github-pr (测试) → git-notes (记录)
```

### 场景 3: 学习新技能
```
 context7 (查文档) → web_fetch (抓取) → summarize (摘要) → memory (存储)
```

### 场景 4: 系统维护
```
 health-monitor.sh (检查) → cleanup.sh (清理) → cron (定时) → reflect (反思)
```

### 场景 5: 创作项目
```
 ai-image-generator (图) → ai-voice-generator (声) → ai-video-generator (视频)
```

### 场景 6: 信息验证
```
 read-github (搜文档) → tavily (深度) → oracle (二审) → memory (记住)
```

## 调度原则

1. **遇到任务** → 匹配场景工作流
2. **串联工具** → 按顺序执行
3. **记录结果** → 用 git-notes 或 memory
4. **反思改进** → 用 reflect 总结

## 资源 → 场景 映射

| 任务 | 资源组合 |
|------|----------|
| 搜索最新信息 | serpapi + tavily + time filter |
| 写代码 | cursor-agent + github + reflect |
| 学习新东西 | context7 + web_fetch + summarize |
| 内容创作 | image/video/voice generator 组合 |
| 系统维护 | health-monitor → cleanup → cron |
| 查 GitHub | read-github + github-pr |
| 获取文档 | context7 + web_fetch |
| 多平台发布 | notion + slack + bluebubbles |
| 自改进 | reflect + cron (每日3点) |

---

*Updated: 2026-01-30 21:30*
