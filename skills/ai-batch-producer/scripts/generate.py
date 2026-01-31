#!/usr/bin/env python3
"""
Batch Producer CLI - Batch content production
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from batch_producer import BatchProducer


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch Producer - Batch anime production",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create batch project
  %(prog)s create anime_series --episodes 10 --output ./projects
  
  # Run all episodes
  %(prog)s run anime_series --parallel
  
  # Run specific stage
  %(prog)s run anime_series --stage images
  
  # Check status
  %(prog)s status anime_series
  
  # Export all
  %(prog)s export anime_series --format mp4
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Create
    create_parser = subparsers.add_parser("create", help="Create batch project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--template", default="standard")
    create_parser.add_argument("--output", "-o", default="./projects")
    create_parser.add_argument("--episodes", type=int, default=5)
    create_parser.add_argument("--duration", type=float, default=5.0)
    
    # Run
    run_parser = subparsers.add_parser("run", help="Run project")
    run_parser.add_argument("name", help="Project name")
    run_parser.add_argument("--parallel", action="store_true")
    run_parser.add_argument("--stage", help="Specific stage only")
    
    # Status
    status_parser = subparsers.add_parser("status", help="Show status")
    status_parser.add_argument("name", nargs="?", help="Project name (all if omitted)")
    
    # Export
    export_parser = subparsers.add_parser("export", help="Export project")
    export_parser.add_argument("name", help="Project name")
    export_parser.add_argument("--format", default="mp4")
    export_parser.add_argument("--quality", default="high")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    producer = BatchProducer()
    
    if args.command == "create":
        project = producer.create_project(
            args.name,
            args.template,
            args.output,
            args.episodes,
            {"duration": args.duration},
        )
        print(f"✅ Created batch project: {args.name}")
        print(f"   Episodes: {args.episodes}")
        print(f"   Location: {args.output}/{args.name}")
    
    elif args.command == "run":
        results = producer.run_project(args.name, args.parallel, args.stage)
        completed = sum(1 for t in results.values() if t.status.value == "completed")
        print(f"✅ Completed: {completed}/{len(results)}")
    
    elif args.command == "status":
        status = producer.get_status(args.name)
        if args.name:
            if not status:
                print(f"❌ Project not found: {args.name}")
            else:
                print(f"📊 {args.name}:")
                for k, v in status.items():
                    if k != "tasks":
                        print(f"   {k}: {v}")
        else:
            print("📊 All Projects:")
            for name, s in status.items():
                print(f"   {name}: {s['completed']}/{s['episodes']} completed")
    
    elif args.command == "export":
        results = producer.export_project(args.name, args.format, args.quality)
        print(f"📦 Export: {len(results)} files would be processed")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
