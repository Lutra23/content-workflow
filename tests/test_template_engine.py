"""Tests for Template Engine"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from template_engine import TemplateEngine

def test_load_templates():
    engine = TemplateEngine(template_dir="templates")
    assert len(engine.templates) > 0, "Should load templates"
    print("✅ test_load_templates passed")

def test_list_templates():
    engine = TemplateEngine(template_dir="templates")
    templates = engine.list_templates()
    assert "article_professional" in templates
    print("✅ test_list_templates passed")

def test_render():
    engine = TemplateEngine(template_dir="templates")
    prompt = engine.render("article_professional", {
        "topic": "AI Test",
        "keywords": "AI, test",
        "audience": "developers",
        "references": "docs",
    })
    assert "AI Test" in prompt
    assert "{{topic}}" not in prompt
    print("✅ test_render passed")

def test_validate():
    engine = TemplateEngine(template_dir="templates")
    result = engine.validate_output("article_professional", "a" * 1000)
    assert "valid" in result
    print("✅ test_validate passed")

def test_quality_assessor():
    from quality import QualityAssessor
    assessor = QualityAssessor()
    content = """
    # Test Article
    
    大家好！今天聊聊测试。
    
    ## 什么是测试
    测试是验证代码正确性的过程。
    
    ## 总结
    测试很重要。
    """
    score = assessor.assess("测试文章", content, ["测试", "代码"])
    assert score.overall > 0
    print("✅ test_quality_assessor passed")

if __name__ == "__main__":
    test_load_templates()
    test_list_templates()
    test_render()
    test_validate()
    test_quality_assessor()
    print("\n✅ All tests passed!")
