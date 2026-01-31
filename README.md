# Content Factory

AI-powered 内容生成工作流 - 模板驱动、质量评估、多提供商支持。

## ✨ 特性

- **模板系统**：YAML 定义的内容模板，支持变量替换
- **多提供商**：Groq / DeepSeek / SiliconFlow / OpenRouter / Yunwu 故障转移
- **质量评估**：可读性、SEO、结构、互动性评分
- **CLI 工具**：一条命令生成内容

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/Lutra23/content-workflow.git
cd content-workflow

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API keys
```

## 🚀 快速开始

### 1. 生成文章

```bash
python scripts/generate.py article --topic "AI Agent 开发" \
  --keywords "AI, Agent, 自动化" \
  --audience "技术开发者"
```

### 2. 生成视频脚本

```bash
python scripts/generate.py video --topic "3分钟讲懂 AI Agent"
```

### 3. 生成社交媒体线程

```bash
python scripts/generate.py thread --topic "AI Agent 革命" --n 10
```

## 📋 模板列表

| 模板 | 用途 | 场景 |
|------|------|------|
| `article_professional` | 专业文章 | 技术博客、知乎 |
| `article_viral` | 病毒式文章 | 社交媒体传播 |
| `video_script_3min` | 3分钟视频脚本 | B站、YouTube |
| `thread_x` | X/Twitter 线程 | 社交媒体 |

## ⚙️ 配置

### 环境变量

```bash
# AI Providers (至少配置一个)
GROQ_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
SILICON_API_KEY=your_key

# 可选
OPENROUTER_API_KEY=your_key
YUNWU_API_KEY=your_key
```

### 自定义模板

编辑 `templates/content.yaml` 添加你的模板。

## 🧪 测试

```bash
# 运行单元测试
python tests/test_core.py

# 运行质量评估
python -c "
from lib.quality import QualityAssessor
score = QualityAssessor().assess('标题', '内容', ['关键词'])
print(f'Score: {score.overall}/100')
"
```

## 📁 项目结构

```
content-workflow/
├── lib/
│   ├── workflow.py        # 核心引擎
│   ├── template_engine.py # 模板系统
│   └── quality.py        # 质量评估
├── templates/
│   └── content.yaml      # 模板定义
├── scripts/
│   └── generate.py       # CLI 入口
├── tests/
│   └── test_core.py      # 测试
├── .plans/               # 项目计划
├── requirements.txt      # 依赖
└── README.md            # 文档
```

## 🔧 开发

```bash
# 运行测试
make test

# 代码检查
make lint

# 生成文档
make docs
```

## 📝 CHANGELOG

见 [CHANGELOG.md](./CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT
