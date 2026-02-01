"""Discovery limit tests"""

import sys
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT / "lib"))

from workflow import ContentFactory


class StubGitHub:
    def get_trending(self, language="python", since="daily"):
        return [
            {
                "title": f"repo{i}",
                "description": "desc",
                "stars": 1000 - i,
                "url": "https://example.com",
                "language": "Python",
            }
            for i in range(10)
        ]


class StubTavily:
    def search(self, query, max_results=3):
        return [
            {
                "title": f"{query}-{i}",
                "content": "content",
                "url": "https://example.com",
            }
            for i in range(3)
        ]


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
                "",
            ]
        )
    )
    return config_path


def test_discover_topics_respects_limit():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        factory = ContentFactory(str(_make_config(tmp_path)))
        factory.github = StubGitHub()
        factory.tavily = StubTavily()

        topics = factory.discover_topics(limit=3)

        assert len(topics) == 3


if __name__ == "__main__":
    test_discover_topics_respects_limit()
    print("OK: discover limit test passed!")
