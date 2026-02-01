"""Ensure manual topics are persisted before generation."""

import sys
from pathlib import Path
import tempfile
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

from workflow import ContentFactory, Topic


class FakeAI:
    def __init__(self, output):
        self.output = output

    def generate_article(self, topic):
        return {
            "title": topic.title,
            "body": self.output,
            "outline": "## Intro\n## Conclusion",
            "seo_description": topic.description,
            "tags": topic.keywords,
        }


def _make_config(tmp_path: Path) -> Path:
    templates_dir = ROOT / "templates"
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                f"data_dir: {tmp_path / 'data'}",
                f"template_dir: {templates_dir}",
                "ai_provider: groq",
                "providers:",
                "  - groq",
                "model: test-model",
                "quality_thresholds:",
                "  overall_min: 0",
                "  max_rewrites: 0",
                "",
            ]
        )
    )
    return config_path


def test_generate_content_inserts_and_marks_topic_used():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        factory = ContentFactory(str(_make_config(tmp_path)))
        factory.ai = FakeAI("## Intro\nBody\n\n## Conclusion\nDone")

        topic = Topic(
            id="manual_1",
            title="Manual Topic",
            description="desc",
            keywords=["AI"],
            source="manual",
            url="",
            engagement=0,
            discovered_at="2024-01-01T00:00:00",
        )

        content = factory.generate_content(topic)
        assert content is not None

        topics = json.loads(factory.topics_file.read_text())
        stored = next((t for t in topics if t.get("id") == "manual_1"), None)
        assert stored is not None
        assert stored.get("used") is True


if __name__ == "__main__":
    test_generate_content_inserts_and_marks_topic_used()
    print("OK: workflow persistence test passed!")
