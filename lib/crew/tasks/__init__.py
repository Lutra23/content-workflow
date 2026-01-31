# Content Tasks

"""
预定义的 Content Tasks for CrewAI.
"""

from typing import List, Optional, Dict, Any

try:
    from crewai import Task
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    Task = None


class ContentTasks:
    """Collection of content generation tasks"""
    
    @staticmethod
    def research(topic: str, keywords: List[str] = None, 
                 output_file: str = None) -> Task:
        """
        Research Task - 研究主题、收集资料
        
        Args:
            topic: Research topic
            keywords: Keywords to focus on
            output_file: Output file path
            
        Returns:
            Research Task
        """
        return Task(
            description=f"""
            请对「{topic}」进行深入研究。
            
            要求：
            1. 收集最新的发展和趋势
            2. 识别关键概念和术语
            3. 找到权威的信息来源
            4. 整理成结构化的研究摘要
            
            {"重点关注关键词：" + ", ".join(keywords) if keywords else ""}
            
            你的输出应该包含：
            - 核心概念解释
            - 最新发展趋势
            - 关键数据或统计
            - 推荐阅读资源
            """,
            expected_output="一份结构化的研究摘要，包含关键要点和发展趋势",
            agent="researcher",
            output_file=output_file,
            context=[]
        )
    
    @staticmethod
    def write(topic: str, content_type: str = "article", 
              audience: str = "general", context: List[Task] = None,
              output_file: str = None) -> Task:
        """
        Write Task - 生成内容
        
        Args:
            topic: Content topic
            content_type: Type of content
            audience: Target audience
            context: Previous tasks (research output)
            output_file: Output file path
            
        Returns:
            Write Task
        """
        type_guides = {
            "article": "技术文章，1500-2000字，Markdown格式",
            "video": "3分钟视频脚本，包含开场、要点、总结",
            "social": "社交媒体帖子，适合分享",
            "thread": "Twitter/X 线程，10条推文"
        }
        
        return Task(
            description=f"""
            根据研究结果，生成一篇关于「{topic}」的{type_guides.get(content_type, '内容')}。
            
            目标受众：{audience}
            
            要求：
            1. 开头要有吸引力（Hook）
            2. 结构清晰，逻辑严密
            3. 提供实用价值
            4. 结尾有总结或 CTA
            
            直接输出内容，不要有其他说明。
            """,
            expected_output=f"完整的{content_type}内容，格式为Markdown",
            agent="writer",
            output_file=output_file,
            context=context or []
        )
    
    @staticmethod
    def edit(content: str = None, criteria: List[str] = None,
             context: List[Task] = None, output_file: str = None) -> Task:
        """
        Edit Task - 质量检查
        
        Args:
            content: Content to edit (optional, can use context)
            criteria: Quality criteria to check
            context: Previous tasks (write output)
            output_file: Output file path
            
        Returns:
            Edit Task
        """
        default_criteria = [
            "可读性（句子长度、专业术语）",
            "结构（标题层级、段落分配）",
            "逻辑（论点连贯、论据充分）",
            "语法（错别字、标点、格式）",
            "SEO（关键词密度、标题优化）",
            "原创性（避免重复内容）"
        ]
        
        return Task(
            description="""
            请检查内容的质量并提供改进建议。
            
            评估维度：
            1. 可读性
            2. 结构
            3. 逻辑
            4. 语法
            5. SEO 优化
            6. 原创性
            """,
            expected_output="质量评分（0-100）和具体改进建议列表",
            agent="editor",
            output_file=output_file,
            context=context or []
        )
    
    @staticmethod
    def publish(platform: str, content: str = None,
                context: List[Task] = None) -> Task:
        """
        Publish Task - 发布内容到平台
        
        Args:
            platform: Target platform
            content: Content to publish
            context: Previous tasks (edit output)
            
        Returns:
            Publish Task
        """
        platform_actions = {
            "zhihu": "发布到知乎专栏，优化标题和摘要，添加相关标签",
            "bilibili": "发布到B站，优化封面和标签，选择合适分区",
            "twitter": "发布为推文或线程，添加话题标签",
            "weibo": "发布到微博，使用话题标签"
        }
        
        return Task(
            description=f"""
            将内容发布到{platform}平台。
            
            平台特定操作：
            {platform_actions.get(platform, '按照平台规范发布')}
            
            确保：
            1. 格式符合平台要求
            2. 添加合适的标签
            3. 选择最佳发布时间
            4. 记录发布链接
            """,
            expected_output=f"发布确认信息，包含发布链接和状态",
            agent="publisher",
            context=context or []
        )
    
    @staticmethod
    def seo_optimize(content: str = None, keywords: List[str] = None,
                     context: List[Task] = None, output_file: str = None) -> Task:
        """
        SEO Optimize Task - SEO 优化
        
        Args:
            content: Content to optimize
            keywords: Target keywords
            context: Previous tasks
            output_file: Output file path
            
        Returns:
            SEO Task
        """
        return Task(
            description=f"""
            对内容进行 SEO 优化。
            
            目标关键词：{', '.join(keywords) if keywords else '待确定'}
            
            需要完成：
            1. 优化标题（包含主关键词）
            2. 优化描述标签
            3. 检查关键词密度
            4. 优化标题层级结构
            5. 添加内部链接建议
            6. 图片 alt 标签建议
            """,
            expected_output="SEO 优化报告，包含具体的优化建议",
            agent="seo_specialist",
            output_file=output_file,
            context=context or []
        )
    
    @staticmethod
    def fact_check(content: str = None, 
                   context: List[Task] = None, 
                   output_file: str = None) -> Task:
        """
        Fact Check Task - 事实核查
        
        Args:
            content: Content to fact check
            context: Previous tasks
            output_file: Output file path
            
        Returns:
            Fact Check Task
        """
        return Task(
            description="""
            请对内容中的所有声明进行事实核查。
            
            需要检查：
            1. 数据和统计的准确性
            2. 引用来源的可信度
            3. 事实陈述的真实性
            4. 时间信息的时效性
            
            对于每个可疑的声明：
            - 标记问题
            - 提供正确的替代信息
            - 给出来源建议
            """,
            expected_output="事实核查报告，包含所有声明的准确性评估",
            agent="fact_checker",
            output_file=output_file,
            context=context or []
        )


# Factory function
def get_task(task_type: str, **kwargs) -> Task:
    """
    Get a specific type of task
    
    Args:
        task_type: Type of task (research, write, edit, publish, seo, fact_check)
        **kwargs: Additional arguments
        
    Returns:
        Configured Task
    """
    tasks = ContentTasks()
    
    task_methods = {
        "research": tasks.research,
        "write": tasks.write,
        "edit": tasks.edit,
        "publish": tasks.publish,
        "seo": tasks.seo_optimize,
        "fact_check": tasks.fact_check,
    }
    
    method = task_methods.get(task_type)
    if method:
        return method(**kwargs)
    
    raise ValueError(f"Unknown task type: {task_type}")


if __name__ == "__main__":
    print("📋 Content Tasks Available:")
    print("   - research(topic, keywords)")
    print("   - write(topic, content_type, audience)")
    print("   - edit(content, criteria)")
    print("   - publish(platform, content)")
    print("   - seo_optimize(content, keywords)")
    print("   - fact_check(content)")
    
    print("\n🔧 Factory function:")
    print("   get_task(task_type, **kwargs)")
