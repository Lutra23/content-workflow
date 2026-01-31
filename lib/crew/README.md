# Content Crew - Multi-Agent Content Generation

基于 CrewAI 框架的多 Agent 内容生成系统。

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      Content Crew                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Researcher  │ →  │   Writer    │ →  │   Editor    │     │
│  │   Agent     │    │   Agent     │    │   Agent     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│       ↓                   ↓                  ↓              │
│   研究主题            生成初稿            质量检查          │
│                                                             │
│  ┌─────────────┐                                            │
│  │  Publisher  │                                            │
│  │   Agent     │                                            │
│  └─────────────┘                                            │
│       ↓                                                     │
│   发布到平台                                                │
└─────────────────────────────────────────────────────────────┘
```

## Agent 定义

### 1. Researcher Agent
```python
researcher = Agent(
    role="{topic}高级研究员",
    goal="探索{topic}的前沿发展和最新信息",
    backstory="你是一名经验丰富的研究员，擅长发现最新发展...",
    tools=[web_search, web_fetch]  # 可调用搜索工具
)
```

### 2. Writer Agent
```python
writer = Agent(
    role="专业内容作家",
    goal="将研究结果转化为高质量内容",
    backstory="你以清晰、引人入胜的写作风格著称...",
    tools=[template_engine]  # 可调用模板引擎
)
```

### 3. Editor Agent
```python
editor = Agent(
    role="资深编辑",
    goal="确保内容质量达到发布标准",
    backstory="你对细节有敏锐的洞察力...",
    tools=[quality_assessor]  # 可调用质量评估
)
```

### 4. Publisher Agent
```python
publisher = Agent(
    role="内容发布专家",
    goal="将内容发布到目标平台",
    backstory="你熟悉各平台的发布规则和最佳实践...",
    tools=[zhihu_api, bilibili_api]
)
```

## Task 定义

### 研究任务
```python
research_task = Task(
    description="深入研究{topic}，找到最新发展和相关资料",
    agent=researcher,
    expected_output="一份包含10个要点的关键信息清单",
    context=[]  # 无前置依赖
)
```

### 写作任务
```python
write_task = Task(
    description="根据研究结果生成一篇完整的{type}内容",
    agent=writer,
    expected_output="完整的内容，格式为 Markdown",
    context=[research_task]  # 依赖研究任务
)
```

### 编辑任务
```python
edit_task = Task(
    description="检查内容质量并提供改进建议",
    agent=editor,
    expected_output="质量评分和改进建议列表",
    context=[write_task]  # 依赖写作任务
)
```

### 发布任务
```python
publish_task = Task(
    description="将内容发布到{platform}平台",
    agent=publisher,
    expected_output="发布成功的确认信息",
    context=[edit_task]  # 依赖编辑任务
)
```

## Crew 配置

```python
from crewai import Crew, Process

content_crew = Crew(
    agents=[researcher, writer, editor, publisher],
    tasks=[research_task, write_task, edit_task, publish_task],
    process=Process.sequential,  # 顺序执行
    verbose=True
)

# 启动工作流
result = content_crew.kickoff(inputs={"topic": "AI Agent", "type": "article"})
```

## Pipeline 模式

```python
from crewai import Crew, Pipeline

# 阶段1: 研究 + 写作
stage1 = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

# 阶段2: 编辑 + 发布
stage2 = Crew(
    agents=[editor, publisher],
    tasks=[edit_task, publish_task],
    process=Process.sequential
)

# 构建 Pipeline
pipeline = Pipeline(
    stages=[stage1, stage2],
    verbose=True
)

result = pipeline.run(inputs={"topic": "AI Agent"})
```

## 使用示例

```python
from lib.crew import ContentCrew

crew = ContentCrew(
    model="llama-3.3-70b-versatile",
    providers=["groq", "deepseek", "silicon"]
)

# 生成文章
result = crew.generate_article(
    topic="AI Agent 开发",
    keywords=["AI", "Agent", "自动化"],
    audience="技术开发者"
)

# 生成视频脚本
result = crew.generate_video_script(
    topic="3分钟讲懂 AI Agent"
)

# 生成并发布
result = crew.generate_and_publish(
    topic="AI Agent 革命",
    platform="zhihu"
)
```

## 工具集成

| Agent | 可用工具 |
|-------|----------|
| Researcher | web_search, web_fetch, tavily_search |
| Writer | template_engine, quality_assessor |
| Editor | quality_assessor, spell_check, seo_check |
| Publisher | zhihu_api, bilibili_api, twitter_api |

## 最佳实践

1. **任务依赖**: 使用 `context` 参数明确任务依赖关系
2. **Agent 背景**: 详细的 `backstory` 提升输出质量
3. **工具选择**: 为每个 Agent 配置合适的工具
4. **流程选择**:
   - `sequential`: 简单任务链
   - `hierarchical`: 需要审核的复杂任务
5. **Pipeline**: 多阶段复杂流程用 Pipeline

## 文件结构

```
lib/
├── crew.py              # CrewAI 集成
├── agents/
│   ├── __init__.py
│   ├── researcher.py    # 研究员 Agent
│   ├── writer.py        # 作家 Agent
│   ├── editor.py        # 编辑 Agent
│   └── publisher.py     # 发布 Agent
├── tasks/
│   ├── __init__.py
│   ├── research.py      # 研究任务
│   ├── write.py         # 写作任务
│   ├── edit.py          # 编辑任务
│   └── publish.py       # 发布任务
└── tools/
    ├── __init__.py
    ├── search.py        # 搜索工具
    ├── template.py      # 模板工具
    └── quality.py       # 质量工具
```

## 参考

- CrewAI 官网: https://www.crewai.com/
- CrewAI GitHub: https://github.com/crewAIInc/crewAI
- 本项目: https://github.com/Lutra23/content-workflow
