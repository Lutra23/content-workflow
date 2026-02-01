"""Template validation tests"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from template_engine import TemplateEngine


def test_validate_output_counts_cjk_chars():
    engine = TemplateEngine(template_dir=str(ROOT / "templates"))
    content = "字" * 600 + "\n\n## 开场\n内容\n\n## 总结\n结束"
    result = engine.validate_output("article_professional", content)
    assert result["valid"] is True
    assert result["word_count"] >= 500


def test_thread_template_does_not_require_sections():
    engine = TemplateEngine(template_dir=str(ROOT / "templates"))
    content = "1/3 这是第一条\n2/3 第二条\n3/3 第三条"
    result = engine.validate_output("thread_x", content)
    assert result["valid"] is True


if __name__ == "__main__":
    test_validate_output_counts_cjk_chars()
    test_thread_template_does_not_require_sections()
    print("OK: template validation tests passed!")
