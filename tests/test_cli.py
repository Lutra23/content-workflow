"""CLI compatibility tests"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

from scripts import generate


class FakeFactory:
    def __init__(self):
        self.calls = []

    def generate_content(self, topic, content_type):
        self.calls.append((content_type, topic))
        class _Status:
            value = "draft"

        class _Content:
            id = "c_1"
            title = "Test Title"
            status = _Status()
            body = "Test body"

        return _Content()

    def find_topic(self, identifier):
        return None


def test_article_alias_builds_topic_and_calls_generate():
    parser = generate.build_parser()
    args = parser.parse_args(
        [
            "article",
            "--topic",
            "AI Agent",
            "--keywords",
            "AI, Agent, automation",
            "--audience",
            "developers",
        ]
    )
    factory = FakeFactory()
    generate.handle_command(args, factory)

    assert len(factory.calls) == 1
    content_type, topic = factory.calls[0]
    assert content_type == "article"
    assert topic.title == "AI Agent"
    assert topic.keywords == ["AI", "Agent", "automation"]


if __name__ == "__main__":
    test_article_alias_builds_topic_and_calls_generate()
    print("OK: CLI compatibility test passed!")
