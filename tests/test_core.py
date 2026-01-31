"""Core functionality tests"""

import sys
from pathlib import Path

# Add lib to path
lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(lib_dir))

from template_engine import TemplateEngine
from quality import QualityAssessor

def test_template_engine():
    engine = TemplateEngine(template_dir=str(Path(__file__).parent.parent / "templates"))
    assert len(engine.templates) > 0, "Should load templates"
    print("✅ Template engine loaded", len(engine.templates), "templates")

def test_render():
    engine = TemplateEngine(template_dir=str(Path(__file__).parent.parent / "templates"))
    prompt = engine.render("article_professional", {
        "topic": "AI Test",
        "keywords": "AI, test",
        "audience": "developers",
        "references": "docs",
    })
    assert "AI Test" in prompt
    print("✅ Template render works")

def test_quality_assessor():
    assessor = QualityAssessor()
    content = "大家好！今天聊聊测试。"
    score = assessor.assess("测试文章", content, ["测试"])
    assert score.overall > 0
    print("✅ Quality assessor works")

if __name__ == "__main__":
    test_template_engine()
    test_render()
    test_quality_assessor()
    print("\n✅ All tests passed!")
