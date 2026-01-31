# Content Factory - Production Content Workflow System

真正可用的内容生产工作流系统，支持多 AI 提供商自动切换。

## Features

- ✅ **选题发现** - GitHub Trending + Tavily 搜索
- ✅ **内容生成** - 支持 5 个 AI 提供商（自动故障转移）
- ✅ **草稿管理** - 本地存储，自动标记已用选题
- ✅ **Cron Ready** - 每天自动运行

## API Providers (按性价比排序)

| Provider | 模型 | 价格 | 状态 |
|----------|------|------|------|
| Groq | Llama 3.3 70B | $0.0003/1k | ✅ 已配置 |
| DeepSeek | DeepSeek Chat | $0.00014/1k | ✅ 已配置 |
| SiliconFlow | DeepSeek | $0.0001/1k | ✅ 已配置 |
| OpenRouter | Claude Sonnet | $0.003/1k | ✅ 已配置 |
| Yunwu | Claude 3.5 | $0.003/1k | ✅ 已配置 |

## Quick Start

```bash
cd content-workflow

# 1. 运行每日工作流（发现选题 + 生成文章）
python scripts/generate.py daily

# 2. 发现选题
python scripts/generate.py discover

# 3. 生成文章
python scripts/generate.py "你的选题" --type article

# 4. 查看状态
python scripts/generate.py status

# 5. 列出草稿
python scripts/generate.py list --status draft
```

## 自动运行

添加 crontab：

```bash
# 每天 9:00 自动运行
0 9 * * * cd /path/to/content-workflow && PYTHONPATH=. python scripts/generate.py daily >> logs/cron.log 2>&1
```

## 文件结构

```
content-workflow/
├── lib/
│   └── workflow.py      # 核心引擎
├── scripts/
│   └── generate.py      # CLI 入口
├── data/
│   ├── topics.json      # 发现的选题
│   └── content.json     # 生成的内容
├── logs/
│   └── workflow.log     # 运行日志
├── config.yaml          # 配置文件
├── requirements.txt
└── README.md
```

## 生成示例

```
$ python scripts/generate.py generate "如何用AI自动化提升科研工作效率"

✅ Generated article: c_20260131_020900
   Title: 如何用AI自动化提升科研工作效率
   Status: draft
   Words: 142
```

## 下一步

1. **配置发布** - 添加知乎/B站发布 API
2. **模板优化** - 添加更多内容模板
3. **多语言** - 支持英文内容生成
4. **数据分析** - 追踪发布后数据

## 技术栈

- Python 3.9+
- Requests (HTTP)
- PyYAML (配置)
- 多 AI API 集成

---

*Built for solopreneurs who want to automate content production*
