# Content Workflow - 项目计划

## 1. Brainstorming (设计)

### 问题定义
**解决什么问题？**
- 内容创作者需要高效生成多平台内容（文章、视频、社交媒体）
- AI 生成内容质量不稳定，缺乏质量评估
- 每次都要写 prompt，重复劳动

### 目标用户
- 技术博主、内容创作者
- 需要批量生产内容的运营人员

### 核心功能
1. **模板引擎**：预定义内容模板，变量替换
2. **多 AI 提供商**：Groq/DeepSeek/SiliconFlow 故障转移
3. **质量评估**：可读性、SEO、结构、互动性评分
4. **CLI 工具**：一条命令生成内容

### 成功标准
- [ ] CLI 命令 < 3 条即可生成一篇完整文章
- [ ] 支持 3 种以上内容类型（文章、视频、社交媒体）
- [ ] 质量评分 > 70/100
- [ ] 有单元测试覆盖核心功能

### 风险点
- API 依赖：提供商故障时降级方案
- 质量不稳定：模板 + 质量检查双重保障

---

## 2. Planning (任务拆解)

### v0.3.0 - CLI 完善 + 文档

| ID | 任务 | 文件 | 验证方式 |
|----|------|------|----------|
| CF-001 | 完善 README | README.md | 阅读流畅 |
| CF-002 | 添加 CHANGELOG | CHANGELOG.md | 格式规范 |
| CF-003 | 更新 requirements.txt | requirements.txt | pip install 成功 |
| CF-004 | 添加 Makefile | Makefile | make help 正常 |

### v0.4.0 - 发布功能

| ID | 任务 | 文件 | 验证方式 |
|----|------|------|----------|
| CF-005 | 知乎发布模块 | lib/publishers/zhihu.py | 单测通过 |
| CF-006 | B 站发布模块 | lib/publishers/bilibili.py | 单测通过 |
| CF-007 | 通用发布接口 | lib/publishers/base.py | 接口测试 |
| CF-008 | CLI 集成发布命令 | scripts/publish.py | 命令可用 |

### v0.5.0 - 高级功能

| ID | 任务 | 文件 | 验证方式 |
|----|------|------|----------|
| CF-009 | RAG 知识库集成 | lib/rag.py | 检索测试 |
| CF-010 | A/B 测试分析 | lib/analytics.py | 数据准确 |
| CF-011 | Docker 部署 | Dockerfile | 构建成功 |

---

## 3. 当前状态

### 已完成 (v0.2.1)
- ✅ 模板引擎 (template_engine.py)
- ✅ 质量评估 (quality.py)
- ✅ 4 种内容模板
- ✅ 单元测试
- ✅ 核心 workflow 引擎

### 待完成
- README / CHANGELOG / Makefile
- 发布功能
- RAG 集成
- Docker 部署

---

## 4. 下一步

从 **CF-001** 开始：完善 README
