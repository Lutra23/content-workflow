#!/usr/bin/env python3
"""
Content Factory - Production-grade Content Workflow System

Features:
- Topic discovery via Tavily API + GitHub API
- Multi-AI provider support (Yunwu, OpenRouter, Groq, DeepSeek, Silicon)
- Content generation with templates
- Multi-platform publishing workflow
- Cron-ready automation

API Providers (按性价比排序):
1. Groq - 最快最便宜 ($0.0003/1k)
2. DeepSeek - 便宜 ($0.00014/1k)
3. SiliconFlow - 便宜 ($0.0001/1k)
4. OpenRouter - 多模型 ($0.003/1k Claude)
5. Yunwu - Claude 国内 ($0.003/1k)
"""

import os
import sys
import json
import yaml
import time
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/workflow.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Publishing platforms"""
    ZHIHU = "zhihu"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    GITHUB = "github"
    BLOG = "blog"
    NOTION = "notion"


class ContentStatus(Enum):
    """Content status"""
    DRAFT = "draft"
    REVIEW = "review"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Topic:
    """Discovered topic"""
    id: str
    title: str
    description: str
    keywords: List[str]
    source: str
    url: str
    engagement: int
    discovered_at: str
    used: bool = False
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Content:
    """Content item"""
    id: str
    topic_id: str
    platform: Platform
    title: str
    body: str
    outline: str
    seo_description: str
    tags: List[str]
    status: ContentStatus
    created_at: str
    updated_at: str
    published_at: Optional[str] = None
    views: int = 0
    likes: int = 0
    comments: int = 0
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['platform'] = self.platform.value
        data['status'] = self.status.value
        return data


class TavilyClient:
    """Tavily API client for topic research"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com"
    
    def search(self, query: str, topic: str = "general",
               days: int = 7, max_results: int = 10,
               include_raw_content: bool = False) -> List[Dict]:
        """Search for topics"""
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "query": query,
                    "topic": topic,
                    "days": days,
                    "max_results": max_results,
                    "include_answer": True,
                    "include_raw_content": include_raw_content,
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return []
    
    def get_answer(self, query: str) -> str:
        """Get direct answer"""
        try:
            response = requests.post(
                f"{self.base_url}/answer",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"query": query},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("answer", "")
        except Exception as e:
            logger.error(f"Tavily answer error: {e}")
            return ""


class GitHubClient:
    """GitHub API client for trending topics"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ContentFactory/1.0"
        }
    
    def get_trending(self, language: str = "python", 
                     since: str = "daily") -> List[Dict]:
        """Get trending repositories"""
        try:
            query = f"language:{language} stars:>1000"
            if since == "daily":
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                query += f" created:>{yesterday}"
            
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params={"q": query, "sort": "stars", "order": "desc", "per_page": 10},
                timeout=30
            )
            response.raise_for_status()
            items = response.json().get("items", [])
            
            return [{
                "title": f"{r['owner']['login']}/{r['name']}",
                "description": r.get("description", ""),
                "stars": r["stargazers_count"],
                "url": r["html_url"],
                "language": r.get("language", ""),
            } for r in items]
        except Exception as e:
            logger.error(f"GitHub API error: {e}")
            return []


class AIClient:
    """
    Multi-AI provider client
    
    Priority (性价比):
    1. Groq - 最快最便宜 ($0.0003/1k tokens)
    2. DeepSeek - 便宜 ($0.00014/1k tokens)
    3. SiliconFlow - 便宜 ($0.0001/1k tokens)
    4. OpenRouter - Claude ($0.003/1k tokens)
    5. Yunwu - Claude 国内 ($0.003/1k tokens)
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.primary_provider = config.get("provider", "groq")
        
        # 按优先级排序的提供商
        self.provider_order = config.get(
            "providers", 
            ["groq", "deepseek", "silicon", "openrouter", "yunwu"]
        )
    
    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Try providers in order until one works"""
        errors = {}
        
        for provider in self.provider_order:
            try:
                method = getattr(self, f"_generate_{provider}", None)
                if method:
                    result = method(prompt, max_tokens)
                    if result and not result.startswith("[AI生成内容]"):
                        return result
                    errors[provider] = "empty/placeholder"
                else:
                    errors[provider] = "no method"
            except Exception as e:
                errors[provider] = str(e)[:30]
        
        # Hard-fail so callers don't accidentally persist a fake/placeholder draft.
        logger.error(f"All providers failed: {errors}")
        raise RuntimeError(f"All AI providers failed: {errors}")
    
    def _generate_groq(self, prompt: str, max_tokens: int) -> str:
        """Groq - 最快最便宜"""
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Missing GROQ_API_KEY environment variable")
        
        model = self.config.get("model", "llama-3.3-70b-versatile")
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _generate_deepseek(self, prompt: str, max_tokens: int) -> str:
        """DeepSeek - 便宜"""
        api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Missing DEEPSEEK_API_KEY environment variable")
        
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _generate_silicon(self, prompt: str, max_tokens: int) -> str:
        """SiliconFlow - 便宜"""
        # Support both names; many environments use SILICONFLOW_API_KEY.
        api_key = (os.environ.get("SILICON_API_KEY", "").strip()
                  or os.environ.get("SILICONFLOW_API_KEY", "").strip())
        if not api_key:
            raise RuntimeError("Missing SILICON_API_KEY (or SILICONFLOW_API_KEY) environment variable")
        
        # SiliconFlow model ids differ from DeepSeek/OpenAI-style names.
        # Use a sane default that exists in /v1/models.
        model = (
            self.config.get("silicon_model")
            or self.config.get("siliconflow_model")
            or self.config.get("model")
            or "deepseek-ai/DeepSeek-V3"
        )
        
        response = requests.post(
            "https://api.siliconflow.cn/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _generate_openrouter(self, prompt: str, max_tokens: int) -> str:
        """OpenRouter - 多模型"""
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Missing OPENROUTER_API_KEY environment variable")
        
        model = self.config.get("model", "anthropic/claude-sonnet-4-20250514")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://content-factory.dev",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _generate_yunwu(self, prompt: str, max_tokens: int) -> str:
        """Yunwu - Claude 国内"""
        api_key = os.environ.get("YUNWU_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Missing YUNWU_API_KEY environment variable")
        
        model = self.config.get("model", "claude-3-5-sonnet")
        
        response = requests.post(
            "https://yunwu.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def generate_article(self, topic: Topic, style: str = "professional", research: str = "") -> Dict:
        """Generate full article"""
        prompt = f"""
你是中文内容写作专家，擅长把技术/工具类信息写成能发布的公众号长文。

【硬性要求】
- 输出语言：简体中文
- 直接输出 Markdown 正文（不要包 ```markdown 代码块）
- 不要出现“作为AI/我无法/免责声明/参考资料”等废话
- 内容必须具体、可执行，避免空泛
- **默认禁止出现任何具体数字（百分比/倍数/金额/时间/排名等）**。
  - 只有当【可用资料】的摘要里明确出现了该数字，你才可以使用，并在句末用括号标注对应来源链接（URL）。
  - 如果资料里没写，就把表达改成不含数字的经验判断（例如“明显”“多数”“少数”“大幅”）。

【文章信息】
主题：{topic.title}
补充描述：{topic.description}
关键词：{", ".join(topic.keywords)}
风格：{style}

【可用资料（必须使用，禁止凭空编造事实/数据）】
{research}

【结构要求】
1) 标题：1 行（# 开头）
2) 开头：3~6 句强 hook（痛点 + 结果 + 反常识）
3) 正文：至少 5 个二级标题（##），每节给出要点/步骤/例子；每节至少引用 1 个来源链接（用括号放 URL）。
   - 引用的目的是“告诉读者你是从哪儿来的”，不是给胡编数据贴个链接。
4) 结尾：给一个 7 天行动清单（可打勾的 checklist）——必须完整 7 条，且每条都要具体可执行，禁止留空
5) 总字数：1200~1800 字

现在开始写。
"""
        content = self.generate(prompt, max_tokens=3000)
        
        # Parse outline
        lines = content.split('\n')
        outline_lines = [l for l in lines if l.startswith('##')]
        outline = '\n'.join(outline_lines)
        
        return {
            "title": topic.title if len(topic.title) < 60 else topic.title[:57] + "...",
            "body": content,
            "outline": outline,
            "seo_description": topic.description[:150],
            "tags": topic.keywords[:5],
        }
    
    def generate_video_script(self, topic: Topic) -> Dict:
        """Generate video script"""
        prompt = f"""
你是中文视频编导，给 B 站做技术类口播脚本。

【硬性要求】
- 输出语言：简体中文
- 不要出现“作为AI/我无法/免责声明”
- 口语化、节奏快、能直接念

【视频信息】
主题：{topic.title}
补充描述：{topic.description}

【结构】
[开场白 10秒]
[为什么值得看 20秒]
[正文要点 x4]（每点给例子/类比）
[总结]
[互动引导]

总时长：3-5 分钟。

现在开始写：
"""
        content = self.generate(prompt, max_tokens=2000)
        
        return {
            "title": f"【AI实战】{topic.title}",
            "body": content,
            "outline": "开场白 → 要点1 → 要点2 → 要点3 → 结尾",
            "seo_description": f"分享关于{topic.title}的实战经验",
            "tags": ["AI", "技术分享"] + topic.keywords[:3],
        }


class ContentFactory:
    """Main content workflow system"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config = self._load_config(config_file)
        self.data_dir = Path(self.config.get("data_dir", "./data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize clients
        self._init_clients()
        
        # Data files
        self.topics_file = self.data_dir / "topics.json"
        self.content_file = self.data_dir / "content.json"
        
        # Initialize files
        if not self.topics_file.exists():
            self.topics_file.write_text("[]")
        if not self.content_file.exists():
            self.content_file.write_text("[]")
        
        logger.info("🚀 ContentFactory initialized")
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration"""
        default = {
            "data_dir": "./data",
            "tavily_api_key": os.environ.get("TAVILY_API_KEY", ""),
            # Default to SiliconFlow since this workspace typically has SILICONFLOW_API_KEY configured.
            "ai_provider": "silicon",
            "providers": ["silicon", "deepseek", "groq", "openrouter", "yunwu"],
            # Language control for prompts.
            "output_language": "zh-CN",
            # SiliconFlow model override (must exist in https://api.siliconflow.cn/v1/models)
            "silicon_model": "Pro/moonshotai/Kimi-K2.5",
        }
        
        if Path(config_file).exists():
            with open(config_file) as f:
                user = yaml.safe_load(f)
                default.update(user)
        
        return default
    
    def _init_clients(self):
        """Initialize API clients"""
        # Tavily
        tavily_key = self.config.get("tavily_api_key", "")
        if tavily_key:
            self.tavily = TavilyClient(tavily_key)
            logger.info("✅ Tavily client ready")
        else:
            self.tavily = None
            logger.info("ℹ️  Tavily not configured (using GitHub only)")
        
        # GitHub
        self.github = GitHubClient()
        logger.info("✅ GitHub client ready")
        
        # AI
        ai_config = {
            "provider": self.config.get("ai_provider", "groq"),
            "providers": self.config.get("providers", ["groq", "deepseek", "silicon"]),
        }
        self.ai = AIClient(ai_config)
        logger.info(f"✅ AI client ready ({ai_config['providers'][0]})")
    
    def _gen_id(self, prefix: str) -> str:
        """Generate unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}"
    
    def discover_topics(self, limit: int = 10) -> List[Topic]:
        """Discover trending topics"""
        topics = []
        
        # GitHub trending
        logger.info("📊 Fetching GitHub trending...")
        repos = self.github.get_trending("python", "weekly")
        for r in repos[:5]:
            topic = Topic(
                id=self._gen_id("gh"),
                title=r["title"],
                description=r["description"][:200] if r["description"] else "",
                keywords=[r["language"], "GitHub", "trending"],
                source="github",
                url=r["url"],
                engagement=r["stars"],
                discovered_at=datetime.now().isoformat(),
            )
            topics.append(topic)
        
        # Tavily search
        if self.tavily:
            logger.info("🔍 Searching Tavily...")
            queries = [
                "AI automation tools 2026",
                "ChatGPT workflow examples",
                "productivity system automation",
            ]
            for q in queries[:2]:
                results = self.tavily.search(q, max_results=3)
                for i, r in enumerate(results):
                    topic = Topic(
                        id=self._gen_id("tv"),
                        title=r.get("title", q),
                        description=r.get("content", "")[:200],
                        keywords=q.split(),
                        source="tavily",
                        url=r.get("url", ""),
                        engagement=i * 10,
                        discovered_at=datetime.now().isoformat(),
                    )
                    topics.append(topic)
        
        # Save topics
        existing = json.loads(self.topics_file.read_text()) if self.topics_file.exists() else []
        existing.extend([t.to_dict() for t in topics])
        self.topics_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
        
        logger.info(f"✅ Discovered {len(topics)} topics")
        return topics
    
    def get_unused_topics(self, limit: int = 5) -> List[Topic]:
        """Get unused topics"""
        all_topics = json.loads(self.topics_file.read_text()) if self.topics_file.exists() else []
        unused = [Topic(**t) for t in all_topics if not t.get("used", False)]
        return unused[:limit]
    
    def mark_topic_used(self, topic_id: str):
        """Mark topic as used"""
        topics = json.loads(self.topics_file.read_text())
        for t in topics:
            if t["id"] == topic_id:
                t["used"] = True
        self.topics_file.write_text(json.dumps(topics, indent=2, ensure_ascii=False))

    def build_research_packet(self, topic: Topic, max_sources: int = 5) -> str:
        """Build a compact research packet (bullets + URLs) for grounded writing."""
        lines: List[str] = []

        # Always include the original topic URL (if any)
        if topic.url:
            lines.append(f"- 原始链接：{topic.url}")

        if not getattr(self, "tavily", None):
            lines.append("- （Tavily 未配置：请仅基于常识写作，避免任何具体数字/断言）")
            return "\n".join(lines)

        # Use Tavily search to gather supporting sources
        results = self.tavily.search(
            query=topic.title,
            topic="general",
            days=30,
            max_results=max_sources,
            include_raw_content=False,
        )

        for r in results[:max_sources]:
            title = (r.get("title") or "").strip()
            url = (r.get("url") or "").strip()
            snippet = (r.get("content") or r.get("answer") or "").strip()
            snippet = " ".join(snippet.split())
            if snippet:
                snippet = snippet[:280]
            if url:
                if title:
                    lines.append(f"- {title}（{url}）")
                else:
                    lines.append(f"- {url}")
            if snippet:
                lines.append(f"  - 摘要：{snippet}")

        # Hard constraint reminder
        lines.append("- 写作规则：任何具体数字/统计/法规/功能断言都必须引用以上链接，否则删掉数字。")
        return "\n".join(lines)

    def generate_content(self, topic: Topic, content_type: str = "article") -> Optional[Content]:
        """Generate content from topic"""
        logger.info(f"📝 Generating {content_type} for: {topic.title}")
        
        try:
            if content_type == "article":
                research = self.build_research_packet(topic)
                result = self.ai.generate_article(topic, research=research)
            else:
                result = self.ai.generate_video_script(topic)
            
            content = Content(
                id=self._gen_id("c"),
                topic_id=topic.id,
                platform=Platform.ZHIHU,
                title=result["title"],
                body=result["body"],
                outline=result["outline"],
                seo_description=result["seo_description"],
                tags=result["tags"],
                status=ContentStatus.DRAFT,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
            )
            
            # Save content
            existing = json.loads(self.content_file.read_text()) if self.content_file.exists() else []
            existing.append(content.to_dict())
            self.content_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
            
            self.mark_topic_used(topic.id)
            logger.info(f"✅ Generated: {content.id}")
            return content
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return None
    
    def get_draft_content(self) -> List[Content]:
        """Get all draft content"""
        if not self.content_file.exists():
            return []
        items = json.loads(self.content_file.read_text())
        return [Content(**c) for c in items if c["status"] == "draft"]
    
    def get_status(self) -> Dict:
        """Get workflow status"""
        topics = json.loads(self.topics_file.read_text()) if self.topics_file.exists() else []
        content = json.loads(self.content_file.read_text()) if self.content_file.exists() else []
        
        return {
            "total_topics": len(topics),
            "unused_topics": len([t for t in topics if not t.get("used", False)]),
            "draft_content": len([c for c in content if c["status"] == "draft"]),
            "published_content": len([c for c in content if c["status"] == "published"]),
        }
    
    def run_daily(self):
        """Run complete daily workflow"""
        logger.info("🚀 Starting daily content workflow...")
        
        # 1. Discover topics
        topics = self.discover_topics()
        
        # 2. Get unused topics
        unused = self.get_unused_topics(3)
        
        # 3. Generate content for top topic
        if unused:
            top_topic = unused[0]
            content = self.generate_content(top_topic, "article")
            
            if content:
                logger.info(f"📄 Generated: {content.title}")
        
        # 4. Summary
        status = self.get_status()
        logger.info(f"\n📊 Daily Summary:")
        logger.info(f"   Topics: {status['total_topics']} ({status['unused_topics']} unused)")
        logger.info(f"   Drafts: {status['draft_content']}")
        logger.info(f"   Published: {status['published_content']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Content Factory")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("daily", help="Run daily workflow")
    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("discover", help="Discover topics")
    
    gen_parser = subparsers.add_parser("generate", help="Generate content")
    gen_parser.add_argument("topic_id", help="Topic ID")
    gen_parser.add_argument("--type", "-t", default="article", choices=["article", "video"])
    
    args = parser.parse_args()
    
    factory = ContentFactory()
    
    if args.command == "daily":
        factory.run_daily()
    elif args.command == "status":
        s = factory.get_status()
        for k, v in s.items():
            print(f"  {k}: {v}")
    elif args.command == "discover":
        factory.discover_topics()
    elif args.command == "generate":
        topics = factory.get_unused_topics()
        topic = next((t for t in topics if t.id == args.topic_id), None)
        if topic:
            factory.generate_content(topic, args.type)
        else:
            print(f"Topic not found: {args.topic_id}")
