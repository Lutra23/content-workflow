# RAG 技术深度分析与实战指南

**分析日期**: 2026-01-31
**作者**: lutra 🦦
**目标**: 掌握生产级 RAG 系统架构

---

## 一、RAG 核心概念

### 1.1 什么是 RAG

```
RAG = Retrieval Augmented Generation (检索增强生成)

核心思想: 开卷考试
├── 输入问题 → 检索知识 → 生成答案
└── 类比: LLM 先翻书，再回答
```

### 1.2 RAG vs 传统 LLM

| 维度 | 纯 LLM | RAG |
|------|--------|-----|
| 知识时效 | 训练数据截止日期 | 实时更新 |
| 私有知识 | 无法直接回答 | 精准检索 |
| 幻觉问题 | 可能编造 | 基于检索事实 |
| 成本 | 低 | 较高（向量库） |

### 1.3 RAG 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    离线流程 (Indexing)                      │
├─────────────────────────────────────────────────────────────┤
│  文档加载 → 文本切分 → 向量化 → 存入向量数据库              │
│     ↓            ↓           ↓            ↓                │
│  PDF/TXT      chunk        embedding    Chroma/Pinecone  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    在线流程 (Querying)                      │
├─────────────────────────────────────────────────────────────┤
│  用户问题 → 问题向量化 → 相似检索 → 拼 Prompt → LLM 生成   │
│      ↓          ↓           ↓            ↓          ↓        │
│  user input  embedding   vector search  context   response │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、向量数据库选型

### 2.1 主流向量数据库对比

| 数据库 | 优点 | 缺点 | 适用场景 |
|--------|------|------|----------|
| **Chroma** | 轻量、易用 | 功能有限 | 原型/小型项目 |
| **Pinecone** | 托管、无运维 | 付费 | 中大型项目 |
| **Weaviate** | 开源、特性多 | 资源消耗大 | 复杂场景 |
| **Milvus** | 高性能、国产 | 部署复杂 | 超大规模 |
| **FAISS** | 高性能、本地 | 无持久化 | 离线场景 |

### 2.2 Chroma 实战

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# 初始化
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory="./chromaDB",
    collection_name="demo001",
    embedding_function=embeddings
)

# 存储文档
documents = [
    "AI 是人工智能的缩写",
    "机器学习是 AI 的子领域",
    "深度学习是机器学习的方法"
]
vectorstore.add_texts(documents)

# 检索
results = vectorstore.similarity_search("什么是机器学习", k=3)
```

### 2.3 向量检索原理

```
向量检索 = 余弦相似度计算

Query 向量化 → [0.1, 0.3, 0.8, ...]
                     ↓
              与所有文档向量计算相似度
                     ↓
              返回 Top-K 最相似文档
```

```python
# 相似度检索
results = vectorstore.similarity_search_with_score("用户问题", k=5)
for doc, score in results:
    print(f"相似度: {score:.4f}")
    print(f"内容: {doc.page_content}")
```

---

## 三、文档处理流水线

### 3.1 文档加载

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)

# PDF 加载
loader = PyPDFLoader("document.pdf")
pages = loader.load()

# 文本加载
loader = TextLoader("document.txt")
docs = loader.load()

# Markdown 加载
loader = UnstructuredMarkdownLoader("document.md")
docs = loader.load()

# Web 页面加载
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

### 3.2 文本切分

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter
)

# 方法1: 递归字符切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每个 chunk 的大小
    chunk_overlap=200,     # 重叠大小（保持连续性）
    separators=["\n\n", "\n", "。", "！", "？", " "]  # 分隔符优先级
)

chunks = text_splitter.split_documents(docs)

# 方法2: Markdown 标题切分
headers_to_split_on = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3")
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
chunks = splitter.split_text(doc_text)
```

### 3.3 切分策略对比

```
┌─────────────────────────────────────────────────────────────┐
│                    切分策略对比                            │
├──────────────┬────────────────────────────────────────────┤
│   固定长度   │ 简单，但可能切断语义                        │
│   递归切分   │ 按段落/句子切分，保持语义完整性 ⭐推荐      │
│   语义切分   │ 按主题切分，但实现复杂                    │
│   标题切分   │ 适合 Markdown 结构化文档                  │
└──────────────┴────────────────────────────────────────────┘
```

---

## 四、Embedding 模型选型

### 4.1 主流 Embedding 模型

| 模型 | 维度 | 效果 | 成本 | 速度 |
|------|------|------|------|------|
| text-embedding-3-small | 1536 | ⭐⭐⭐ | 低 | 快 |
| text-embedding-3-large | 3072 | ⭐⭐⭐⭐⭐ | 中 | 中 |
| BGE-large-zh | 1024 | ⭐⭐⭐⭐ | 低 | 快 |
| M3E-large | 1024 | ⭐⭐⭐⭐ | 低 | 快 |

### 4.2 多模型支持

```python
from langchain_openai import OpenAIEmbeddings

# OpenAI
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 阿里通义
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="text-embedding-v1"
)

# 本地 Ollama
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest"
)
```

---

## 五、Prompt Engineering

### 5.1 RAG Prompt 模板

```python
from langchain_core.prompts import ChatPromptTemplate

# 基础 RAG Prompt
PROMPT_TEMPLATE = """基于以下上下文回答用户的问题。

上下文:
{context}

问题: {question}

请根据上下文信息回答，如果上下文中没有相关信息，请说"根据提供的上下文，我无法回答这个问题"。
"""

# 带思考的 RAG Prompt
PROMPT_WITH_THINKING = """你是一个专业的助手。请按以下步骤回答：

1. 分析问题，理解用户意图
2. 在上下文中搜索相关信息
3. 综合分析，给出答案

上下文:
{context}

问题: {question}

请逐步思考并给出答案。
"""
```

### 5.2 LCEL 构建 Chain

```python
from langchain_core.runnables import RunnablePassthrough

# 检索器
retriever = vectorstore.as_retriever(k=5)

# Prompt 模板
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 构建 Chain (LCEL)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 执行
response = chain.invoke("用户问题")
```

---

## 六、检索优化策略

### 6.1 查询变换

```python
# 查询重写 - 扩展查询词
def expand_query(question: str) -> list[str]:
    """将问题扩展为多个查询"""
    return [
        question,
        f"什么是{question}",
        f"{question}的原理",
        f"关于{question}的知识"
    ]

# 查询分解 - 拆分为子问题
def decompose_query(question: str) -> list[str]:
    """将复杂问题分解为简单问题"""
    # 使用 LLM 进行分解
    prompt = f"将以下复杂问题分解为多个简单问题:\n{question}"
    sub_questions = llm.invoke(prompt)
    return sub_questions.split("\n")
```

### 6.2 Re-ranker 重排序

```python
from langchain_community.cross_encoders import CrossEncoder

# 轻量级重排序模型
reranker = CrossEncoder("BAAI/bge-reranker-base")

# 两阶段检索
def retrieve_with_rerank(query: str, k1: int = 20, k2: int = 5):
    # 阶段1: 粗检索
    initial_results = vectorstore.similarity_search(query, k=k1)
    
    # 阶段2: 重排序
    pairs = [(query, doc.page_content) for doc in initial_results]
    scores = reranker.predict(pairs)
    
    # 排序并返回 Top-K
    ranked_docs = sorted(
        zip(initial_results, scores),
        key=lambda x: x[1],
        reverse=True
    )[:k2]
    
    return [doc for doc, _ in ranked_docs]
```

### 6.3 混合检索

```python
# 向量检索 + 关键词检索
from langchain_community.retrievers import BM25Retriever

# 向量检索
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 关键词检索
texts = [doc.page_content for doc in vectorstore.similarity_search("", k=100)]
keyword_retriever = BM25Retriever.from_texts(texts)

# 融合检索结果
from langchain.retrievers import EnsembleRetriever

ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, keyword_retriever],
    weights=[0.7, 0.3]  # 向量检索权重更高
)
```

---

## 七、记忆系统集成

### 7.1 对话历史管理

```python
# 短期记忆 - 窗口滑动
def get_recent_messages(messages: list, window: int = 5):
    """保留最近 N 条消息"""
    return messages[-window:]

# 长期记忆 - 向量存储
def store_memory(question: str, answer: str, user_id: str):
    """存储问答对到长期记忆"""
    memory_text = f"问题: {question}\n答案: {answer}"
    vectorstore.add_texts([memory_text], metadatas=[{"user_id": user_id}])

# 检索相关历史
def get_relevant_history(query: str, user_id: str):
    """检索用户相关历史"""
    results = vectorstore.similarity_search(
        query,
        k=3,
        filter={"user_id": user_id}
    )
    return [r.page_content for r in results]
```

### 7.2 完整记忆架构

```
┌─────────────────────────────────────────────────────────┐
│                   记忆处理流水线                        │
├─────────────────────────────────────────────────────────┤
│                                                    │
│  用户输入 → 检索历史 → 拼入上下文 → LLM 生成          │
│      ↓           ↓            ↓            ↓          │
│  新问题   短期记忆     增强 Prompt    生成回答       │
│            ↓                               ↓          │
│         长期记忆 ←── 存储新问答 ──→ 历史记录        │
│                                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 八、完整代码架构

### 8.1 项目结构

```
RagLangChainTest/
├── main.py                 # FastAPI 服务入口
├── apiTest.py             # API 测试脚本
├── mainMemory.py          # 带记忆的版本
├── mainReranker.py        # 带重排序的版本
├── prompt_template.txt    # Prompt 模板
├── prompt_template_memory.txt  # 带记忆的 Prompt
├── chromaDB/              # 向量数据库存储
├── input/                 # 输入文档
├── output/                # 输出文件
└── tools/                 # 工具函数
```

### 8.2 FastAPI 服务

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="RAG API")

class QueryRequest(BaseModel):
    question: str
    user_id: str = "default"

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    # 1. 检索
    docs = vectorstore.similarity_search(request.question, k=5)
    
    # 2. 构建 Prompt
    context = "\n".join([d.page_content for d in docs])
    prompt = PROMPT_TEMPLATE.format(context=context, question=request.question)
    
    # 3. 生成答案
    response = llm.invoke(prompt)
    
    # 4. 返回
    return QueryResponse(
        answer=response.content,
        sources=[d.metadata.get("source", "") for d in docs]
    )
```

### 8.3 配置管理

```python
# config.py
import os

class Config:
    # 向量数据库
    CHROMADB_DIRECTORY = os.getenv("CHROMADB_DIR", "./chromaDB")
    CHROMADB_COLLECTION = os.getenv("CHROMADB_COLLECTION", "demo001")
    
    # 模型配置
    LLM_TYPE = os.getenv("LLM_TYPE", "oneapi")  # openai 或 oneapi
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v1")
    
    # API 配置
    ONEAPI_BASE = "http://139.224.72.218:3000/v1"
    ONEAPI_KEY = os.getenv("ONEAPI_KEY", "sk-...")
    
    # Prompt
    PROMPT_TEMPLATE = "prompt_template.txt"
```

---

## 九、性能优化

### 9.1 检索优化

```python
# 1. 索引优化
# 批量添加，提高效率
vectorstore.add_texts(documents, batch_size=100)

# 2. 缓存优化
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embedding(text: str):
    return embeddings.embed_query(text)

# 3. 异步优化
import asyncio

async def async_retrieve(queries: list[str]):
    tasks = [vectorstore.asimilarity_search(q, k=3) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

### 9.2 成本优化

| 优化点 | 方法 | 成本降低 |
|--------|------|----------|
| Embedding 模型 | 使用 text-embedding-3-small | ~50% |
| LLM 模型 | 问题简单用 4o-mini | ~80% |
| 检索数量 | 精确控制 k 值 | ~30% |
| 缓存 | 热门查询缓存 | ~60% |

---

## 十、常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 检索不准确 | Embedding 模型不匹配 | 使用同源 Embedding |
| 上下文截断 | chunk_size 过大 | 减小 chunk_size |
| 重复内容 | 检索结果相似 | MMR 去重 |
| 回答不相关 | Prompt 不清晰 | 优化 Prompt 模板 |
| 性能差 | 同步阻塞 | 异步 + 并发 |

---

## 十一、生产环境检查清单

```python
PRODUCTION_CHECKLIST = {
    "数据质量": [
        "✅ 文档预处理完成",
        "✅ chunk 大小合理",
        "✅ 元数据完整"
    ],
    "索引优化": [
        "✅ 索引构建完成",
        "✅ 索引大小监控",
        "✅ 定期更新索引"
    ],
    "检索效果": [
        "✅ 检索相关性好",
        "✅ 响应时间 < 1s",
        "✅ 重排序生效"
    ],
    "服务稳定": [
        "✅ API 可用性 > 99%",
        "✅ 错误重试机制",
        "✅ 日志记录完整"
    ]
}
```

---

## 十二、学习资源

### 文档
- LangChain RAG: https://python.langchain.com/docs/tutorials/rag/
- Chroma: https://docs.trychroma.com/
- RAG 最佳实践: https://github.com/langchain-ai/rag-evaluation

### 项目
- RagLangChainTest: https://github.com/NanGePlus/RagLangChainTest
- LangGraphChatBot: https://github.com/NanGePlus/LangGraphChatBot

---

*文档生成时间: 2026-01-31*
*来源: NanGePlus RAG 学习*
