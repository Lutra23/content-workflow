# Content Agents

"""
预定义的 Content Agents for CrewAI.
"""

from typing import List, Optional

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    Agent = None


class ContentAgents:
    """Collection of content generation agents"""
    
    @staticmethod
    def researcher(topic: str = "{topic}") -> Agent:
        """
        Researcher Agent - 负责研究主题、收集资料
        
        Args:
            topic: Research topic template
            
        Returns:
            Researcher Agent
        """
        return Agent(
            role=f"{topic}高级研究员",
            goal=f"深入研究{topic}，找到最新发展和关键信息",
            backstory=f"""
            你是一名经验丰富的研究员，专注于{topic}领域。
            你以善于发现最相关的信息、整理关键要点、并以简洁的方式呈现复杂概念而闻名。
            你的研究方法严谨，注重时效性和权威性。
            """,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    @staticmethod
    def writer(content_type: str = "article") -> Agent:
        """
        Writer Agent - 负责生成内容
        
        Args:
            content_type: Type of content to write
            
        Returns:
            Writer Agent
        """
        type_descriptions = {
            "article": "技术文章和博客",
            "video": "视频脚本和旁白",
            "social": "社交媒体内容",
            "thread": "Twitter/X 线程"
        }
        
        return Agent(
            role="专业内容作家",
            goal="将研究结果转化为高质量、有吸引力的内容",
            backstory=f"""
            你是一位资深内容创作者，擅长撰写{type_descriptions.get(content_type, '各类内容')}。
            你的写作风格清晰、逻辑严密、富有洞察力。
            你总能抓住读者的注意力，并在提供价值的同时保持趣味性。
            """,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    @staticmethod
    def editor() -> Agent:
        """
        Editor Agent - 负责质量检查和润色
        
        Returns:
            Editor Agent
        """
        return Agent(
            role="资深编辑",
            goal="确保内容质量达到发布标准",
            backstory="""
            你是一名资深编辑，对内容质量有严格的标准。
            你的专长是发现文章中的问题并提供改进建议。
            你关注：可读性、结构、逻辑、语法、SEO优化等方面。
            你的反馈建设性且具体，帮助创作者不断提升。
            """,
            verbose=True,
            allow_delegation=True,
            memory=True
        )
    
    @staticmethod
    def publisher(platform: str = "general") -> Agent:
        """
        Publisher Agent - 负责发布内容到平台
        
        Args:
            platform: Target platform
            
        Returns:
            Publisher Agent
        """
        platform_guides = {
            "zhihu": "知乎平台的规则和最佳实践",
            "bilibili": "B站内容规范和标签使用",
            "twitter": "X/Twitter 的内容格式和话题标签",
            "general": "各内容平台的发布规范"
        }
        
        return Agent(
            role="内容发布专家",
            goal=f"将内容发布到目标平台并优化曝光",
            backstory=f"""
            你是一位内容发布专家，熟悉{platform_guides.get(platform, platform_guides['general'])}。
            你了解如何优化内容格式、选择最佳发布时间、使用合适的标签来增加曝光。
            你的工作确保内容能够触达最大化的目标受众。
            """,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    @staticmethod
    def seo_specialist() -> Agent:
        """
        SEO Specialist Agent - 负责 SEO 优化
        
        Returns:
            SEO Specialist Agent
        """
        return Agent(
            role="SEO 优化专家",
            goal="确保内容在搜索引擎中获得最佳排名",
            backstory="""
            你是一位 SEO 专家，精通搜索引擎优化策略。
            你知道如何选择正确的关键词、优化标题和描述、
            构建内部链接、以及创建对搜索引擎友好的内容结构。
            你的建议帮助内容获得更多的有机流量。
            """,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    @staticmethod
    def fact_checker() -> Agent:
        """
        Fact Checker Agent - 负责事实核查
        
        Returns:
            Fact Checker Agent
        """
        return Agent(
            role="事实核查员",
            goal="确保内容的准确性和可信度",
            backstory="""
            你是一位严谨的事实核查员，负责验证内容中的所有声明。
            你会检查数据、引用、统计数据和事实陈述的准确性。
            你的工作确保内容不会传播错误信息，维护内容的可信度。
            """,
            verbose=True,
            allow_delegation=False,
            memory=True
        )


# Factory function
def get_agent(agent_type: str, **kwargs) -> Agent:
    """
    Get a specific type of agent
    
    Args:
        agent_type: Type of agent (researcher, writer, editor, publisher, seo, fact_checker)
        **kwargs: Additional arguments
        
    Returns:
        Configured Agent
    """
    agents = ContentAgents()
    
    agent_methods = {
        "researcher": agents.researcher,
        "writer": agents.writer,
        "editor": agents.editor,
        "publisher": agents.publisher,
        "seo": agents.seo_specialist,
        "fact_checker": agents.fact_checker,
    }
    
    method = agent_methods.get(agent_type)
    if method:
        return method(**kwargs)
    
    raise ValueError(f"Unknown agent type: {agent_type}")


if __name__ == "__main__":
    print("📋 Content Agents Available:")
    print("   - researcher(topic)")
    print("   - writer(content_type)")
    print("   - editor()")
    print("   - publisher(platform)")
    print("   - seo_specialist()")
    print("   - fact_checker()")
    
    print("\n🔧 Factory function:")
    print("   get_agent(agent_type, **kwargs)")
