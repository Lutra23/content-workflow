# Content Crew - Multi-Agent Content Generation System

"""
基于 CrewAI 框架的多 Agent 内容生成系统。

使用 CrewAI 实现:
- Researcher Agent: 研究主题、收集资料
- Writer Agent: 生成内容
- Editor Agent: 质量检查
- Publisher Agent: 发布到平台
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

# CrewAI imports (optional, graceful fallback)
try:
    from crewai import Agent, Task, Crew, Process
    from crewai.tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("⚠️ CrewAI not installed. Run: pip install crewai crewai-tools")


@dataclass
class ContentConfig:
    """Content generation configuration"""
    topic: str
    content_type: str = "article"
    keywords: List[str] = None
    audience: str = "general"
    platform: str = None
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7


class ContentCrew:
    """Multi-agent content generation crew"""
    
    def __init__(self, config: Dict = None):
        """
        Initialize Content Crew
        
        Args:
            config: Configuration dict with model/providers settings
        """
        self.config = config or {}
        self.providers = self.config.get("providers", ["groq", "deepseek"])
        self.model = self.config.get("model", "llama-3.3-70b-versatile")
        
        if CREWAI_AVAILABLE:
            self._setup_agents()
            self._setup_tasks()
    
    def _setup_agents(self):
        """Setup all agents"""
        if not CREWAI_AVAILABLE:
            return
        
        # Researcher Agent
        self.researcher = Agent(
            role="{topic}研究员",
            goal="深入研究{topic}，找到最新发展和关键信息",
            backstory="你是一名经验丰富的研究员，擅长发现和整理关键信息。",
            verbose=True,
            allow_delegation=False
        )
        
        # Writer Agent
        self.writer = Agent(
            role="专业作家",
            goal="将研究结果转化为高质量内容",
            backstory="你以清晰、引人入胜的写作风格著称。",
            verbose=True,
            allow_delegation=False
        )
        
        # Editor Agent
        self.editor = Agent(
            role="资深编辑",
            goal="确保内容质量达到发布标准",
            backstory="你对内容质量有严格的标准，确保每篇文章都达到最佳状态。",
            verbose=True,
            allow_delegation=False
        )
        
        # Publisher Agent
        self.publisher = Agent(
            role="内容发布专家",
            goal="将内容发布到目标平台",
            backstory="你熟悉各平台的发布规则和最佳实践。",
            verbose=True,
            allow_delegation=False
        )
    
    def _setup_tasks(self):
        """Setup all tasks"""
        if not CREWAI_AVAILABLE:
            return
        
        # Research Task
        self.research_task = Task(
            description="研究{topic}相关资料，收集最新发展信息",
            expected_output="一份包含关键要点的研究摘要",
            agent=self.researcher
        )
        
        # Write Task
        self.write_task = Task(
            description="根据研究结果生成一篇关于{topic}的{type}内容",
            expected_output="完整的{type}内容，格式为Markdown",
            agent=self.writer,
            context=[self.research_task]
        )
        
        # Edit Task
        self.edit_task = Task(
            description="检查内容质量，提供改进建议",
            expected_output="质量评分和改进建议",
            agent=self.editor,
            context=[self.write_task]
        )
        
        # Publish Task
        self.publish_task = Task(
            description="将内容发布到{platform}平台",
            expected_output="发布确认信息",
            agent=self.publisher,
            context=[self.edit_task]
        )
    
    def generate_article(self, topic: str, keywords: List[str] = None, 
                         audience: str = "general") -> Dict:
        """
        Generate a professional article
        
        Args:
            topic: Article topic
            keywords: Keywords to include
            audience: Target audience
            
        Returns:
            Dict with article content and metadata
        """
        if not CREWAI_AVAILABLE:
            return self._fallback_generate("article", topic, keywords, audience)
        
        # Create crew for article generation
        crew = Crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[self.research_task, self.write_task, self.edit_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={
            "topic": topic,
            "type": "article",
            "keywords": ", ".join(keywords or []),
            "audience": audience
        })
        
        return {
            "type": "article",
            "topic": topic,
            "content": result,
            "status": "generated"
        }
    
    def generate_video_script(self, topic: str, duration: str = "3min") -> Dict:
        """
        Generate a video script
        
        Args:
            topic: Video topic
            duration: Video duration (3min, 5min, 10min)
            
        Returns:
            Dict with script content and metadata
        """
        if not CREWAI_AVAILABLE:
            return self._fallback_generate("video", topic, None, None)
        
        crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[self.research_task, self.write_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={
            "topic": topic,
            "type": f"video_script_{duration}"
        })
        
        return {
            "type": "video_script",
            "topic": topic,
            "duration": duration,
            "content": result,
            "status": "generated"
        }
    
    def generate_thread(self, topic: str, n: int = 10) -> Dict:
        """
        Generate a Twitter/X thread
        
        Args:
            topic: Thread topic
            n: Number of tweets
            
        Returns:
            Dict with thread content and metadata
        """
        if not CREWAI_AVAILABLE:
            return self._fallback_generate("thread", topic, None, None)
        
        crew = Crew(
            agents=[self.writer],
            tasks=[self.write_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={
            "topic": topic,
            "type": f"thread_{n}tweets"
        })
        
        return {
            "type": "thread",
            "topic": topic,
            "n": n,
            "content": result,
            "status": "generated"
        }
    
    def generate_and_publish(self, topic: str, platform: str, 
                             content_type: str = "article") -> Dict:
        """
        Generate content and publish to platform
        
        Args:
            topic: Content topic
            platform: Target platform (zhihu, bilibili, etc.)
            content_type: Type of content
            
        Returns:
            Dict with publish result
        """
        if not CREWAI_AVAILABLE:
            return {"error": "CrewAI not available"}
        
        crew = Crew(
            agents=[self.researcher, self.writer, self.editor, self.publisher],
            tasks=[self.research_task, self.write_task, self.edit_task, self.publish_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={
            "topic": topic,
            "type": content_type,
            "platform": platform
        })
        
        return {
            "type": content_type,
            "topic": topic,
            "platform": platform,
            "result": result,
            "status": "published"
        }
    
    def _fallback_generate(self, content_type: str, topic: str, 
                           keywords: List[str], audience: str) -> Dict:
        """Fallback when CrewAI is not available"""
        from lib.template_engine import TemplateEngine
        from lib.workflow import ContentWorkflow
        
        # Use template engine
        engine = TemplateEngine()
        template = engine.suggest_template(content_type, audience)
        
        variables = {
            "topic": topic,
            "keywords": ", ".join(keywords or []),
            "audience": audience,
        }
        
        # Use workflow to generate
        workflow = ContentWorkflow(self.config)
        prompt = engine.render(template, variables)
        system_prompt = engine.render_system_prompt(template, variables)
        
        content = workflow.generate(prompt)
        
        # Validate quality
        quality_result = engine.validate_output(template, content)
        
        return {
            "type": content_type,
            "topic": topic,
            "content": content,
            "quality": quality_result,
            "status": "generated_fallback"
        }


# Convenience functions
def create_crew(config: Dict = None) -> ContentCrew:
    """Create a content crew"""
    return ContentCrew(config)


def generate_quick_article(topic: str, **kwargs) -> Dict:
    """Quick article generation"""
    crew = create_crew()
    return crew.generate_article(topic, **kwargs)


if __name__ == "__main__":
    print("🤖 Content Crew - Multi-Agent Content Generation")
    print("=" * 50)
    
    if not CREWAI_AVAILABLE:
        print("⚠️ CrewAI not installed. Install with:")
        print("   pip install crewai crewai-tools")
        print("\n📝 Using fallback generation (template + workflow)")
    
    # Demo
    crew = ContentCrew()
    
    print("\n📋 Available methods:")
    print("   - crew.generate_article(topic, keywords, audience)")
    print("   - crew.generate_video_script(topic, duration)")
    print("   - crew.generate_thread(topic, n)")
    print("   - crew.generate_and_publish(topic, platform, type)")
    
    print("\n✅ Content Crew initialized successfully!")
