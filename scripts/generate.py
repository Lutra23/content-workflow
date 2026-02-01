#!/usr/bin/env python3
"""
Content Factory CLI - Production content workflow
"""

import sys
from pathlib import Path
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from lib.workflow import ContentFactory, Platform, Topic


def _parse_keywords(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _build_manual_topic(title: str, keywords: list[str], audience: str | None) -> Topic:
    description = f"Content about {title}"
    if audience:
        description = f"{description}. Audience: {audience}"
    return Topic(
        id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title=title,
        description=description,
        keywords=keywords,
        source="manual",
        url="",
        engagement=100,
        discovered_at=datetime.now().isoformat(),
    )


def build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Content Factory - Production content workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run daily workflow (discover + generate)
  python scripts/generate.py daily
  
  # Discover trending topics
  python scripts/generate.py discover
  
  # Generate article
  python scripts/generate.py generate topic_xxx --type article
  
  # Generate video script
  python scripts/generate.py generate topic_xxx --type video
  
  # Show status
  python scripts/generate.py status
  
  # List drafts
  python scripts/generate.py list --status draft

API Providers (按性价比):
  1. Groq - 最快 ($0.0003/1k tokens)
  2. DeepSeek - 便宜 ($0.00014/1k tokens)
  3. SiliconFlow - 便宜 ($0.0001/1k tokens)
  4. OpenRouter - Claude ($0.003/1k tokens)
  5. Yunwu - Claude 国内 ($0.003/1k tokens)
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # Daily run
    daily_parser = subparsers.add_parser("daily", help="Run complete daily workflow")
    daily_parser.add_argument("--dry-run", action="store_true", help="Preview without executing")

    # Discover
    disc_parser = subparsers.add_parser("discover", help="Discover trending topics")
    disc_parser.add_argument("-n", type=int, default=10, help="Number of topics")

    # Generate
    gen_parser = subparsers.add_parser("generate", help="Generate content from topic")
    gen_parser.add_argument("topic", help="Topic title or ID")
    gen_parser.add_argument(
        "--type",
        "-t",
        default="article",
        choices=["article", "video"],
        help="Content type",
    )
    gen_parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    gen_parser.add_argument("--audience", default="", help="Audience description")

    # Legacy aliases (Makefile compatibility)
    article_parser = subparsers.add_parser("article", help="Generate article (legacy)")
    article_parser.add_argument("--topic", required=True, help="Article topic")
    article_parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    article_parser.add_argument("--audience", default="", help="Audience description")

    video_parser = subparsers.add_parser("video", help="Generate video script (legacy)")
    video_parser.add_argument("--topic", required=True, help="Video topic")
    video_parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    video_parser.add_argument("--audience", default="", help="Audience description")

    # List
    list_parser = subparsers.add_parser("list", help="List content")
    list_parser.add_argument("--status", default="draft", choices=["draft", "published"])

    # Status
    subparsers.add_parser("status", help="Show workflow status")

    return parser


def handle_command(args, factory: ContentFactory) -> None:
    if args.command == "daily":
        if args.dry_run:
            print("🔍 Dry run - would execute:")
            print("   1. Discover trending topics (GitHub + Tavily)")
            print("   2. Generate article for top topic")
            print("   3. Save as draft")
        else:
            factory.run_daily()

    elif args.command == "discover":
        topics = factory.discover_topics(limit=args.n)
        print(f"\n📊 Found {len(topics)} topics:")
        for i, t in enumerate(topics[:10], 1):
            print(f"  {i}. {t.title}")
            print(f"     Score: {t.engagement} | Source: {t.source}")
            print(f"     Keywords: {', '.join(t.keywords[:3])}")

    elif args.command == "generate":
        keywords = _parse_keywords(args.keywords)
        topic = _build_manual_topic(args.topic, keywords, args.audience)

        content = factory.generate_content(topic, args.type)
        if content:
            print(f"\n✅ Generated {args.type}: {content.id}")
            print(f"   Title: {content.title}")
            print(f"   Status: {content.status.value}")
            print(f"   Words: {len(content.body.split())}")

    elif args.command in ("article", "video"):
        keywords = _parse_keywords(args.keywords)
        topic = _build_manual_topic(args.topic, keywords, args.audience)

        content = factory.generate_content(topic, args.command)
        if content:
            print(f"\n✅ Generated {args.command}: {content.id}")
            print(f"   Title: {content.title}")
            print(f"   Status: {content.status.value}")
            print(f"   Words: {len(content.body.split())}")

    elif args.command == "list":
        items = factory.get_draft_content() if args.status == "draft" else []
        if items:
            print(f"\n📄 {args.status.capitalize()} content ({len(items)}):")
            for c in items:
                print(f"  - {c.title[:50]}...")
        else:
            print(f"\nNo {args.status} content")

    elif args.command == "status":
        s = factory.get_status()
        print("\n📊 Content Factory Status:")
        print(f"   Total Topics: {s['total_topics']}")
        print(f"   Unused Topics: {s['unused_topics']}")
        print(f"   Draft Content: {s['draft_content']}")
        print(f"   Published: {s['published_content']}")

    else:
        raise SystemExit(f"Unknown command: {args.command}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    factory = ContentFactory()
    handle_command(args, factory)


if __name__ == "__main__":
    main()
