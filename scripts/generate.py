#!/usr/bin/env python3
"""
Content Factory CLI - Production content workflow
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from lib.workflow import ContentFactory, Platform


def main():
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
        """
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
    gen_parser.add_argument("--type", "-t", default="article",
                           choices=["article", "video"],
                           help="Content type")
    
    # List
    list_parser = subparsers.add_parser("list", help="List content")
    list_parser.add_argument("--status", default="draft",
                            choices=["draft", "published"])
    
    # Status
    subparsers.add_parser("status", help="Show workflow status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    factory = ContentFactory()
    
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
        # Create topic from input
        from lib.workflow import Topic
        topic = Topic(
            id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=args.topic,
            description=f"Content about {args.topic}",
            keywords=["AI", "automation"],
            source="manual",
            url="",
            engagement=100,
            discovered_at=datetime.now().isoformat(),
        )
        
        content = factory.generate_content(topic, args.type)
        if content:
            print(f"\n✅ Generated {args.type}: {content.id}")
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
        parser.print_help()


if __name__ == "__main__":
    from datetime import datetime
    main()
