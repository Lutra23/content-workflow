#!/usr/bin/env python3
"""
Anime Pipeline CLI - Main entry point for anime production workflow
"""

import sys
import os
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from pipeline import AnimePipeline, load_project, create_quick_project, Stage


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Anime Production Pipeline - End-to-end workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize a new project
  %(prog)s init my_anime --scenes 5
  
  # Run full pipeline
  %(prog)s run my_anime/project.yaml
  
  # Run only specific stages
  %(prog)s run my_anime/project.yaml --stages images,video,voice
  
  # Continue from where you left off
  %(prog)s run my_anime/project.yaml
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("--output", "-o", default="./projects", help="Output directory")
    init_parser.add_argument("--scenes", type=int, default=3, help="Number of sample scenes")
    init_parser.add_argument("--template", default="standard", 
                            choices=["standard", "short", "feature"],
                            help="Project template")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run pipeline")
    run_parser.add_argument("config", help="Project config YAML file")
    run_parser.add_argument("--stages", help="Comma-separated stages to run (e.g., images,video)")
    run_parser.add_argument("--parallel", action="store_true", help="Run stages in parallel")
    run_parser.add_argument("--dry-run", action="store_true", help="Show what would run without executing")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.add_argument("config", help="Project config YAML file")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export project")
    export_parser.add_argument("config", help="Project config YAML file")
    export_parser.add_argument("--format", default="mp4", help="Export format")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "init":
        config = create_quick_project(args.name, args.output, args.scenes)
        project_dir = Path(args.output) / args.name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = project_dir / "project.yaml"
        with open(config_file, "w") as f:
            yaml = __import__("yaml")
            yaml.dump(config.to_dict(), f)
        
        print(f"✅ Created project: {args.name}")
        print(f"   Location: {project_dir}")
        print(f"   Scenes: {args.scenes}")
        print(f"\n📝 Next steps:")
        print(f"   1. Edit {config_file}")
        print(f"   2. Add scene descriptions, dialogue, and settings")
        print(f"   3. Run: {sys.argv[0]} run {config_file}")
    
    elif args.command == "run":
        if not os.path.exists(args.config):
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        
        config = load_project(args.config)
        pipeline = AnimePipeline(config)
        
        stages = None
        if args.stages:
            stages = [Stage(s.strip()) for s in args.stages.split(",")]
        
        if args.dry_run:
            print("🔍 Dry run - would execute:")
            for stage in stages or list(Stage):
                print(f"   - {stage.value}")
        else:
            pipeline.run(stages=stages, parallel=args.parallel)
    
    elif args.command == "status":
        if not os.path.exists(args.config):
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        
        config = load_project(args.config)
        print(f"📊 Project: {config.name}")
        print(f"   Scenes: {len(config.scenes)}")
        print(f"   Output: {config.output_dir}")
    
    elif args.command == "export":
        print(f"📦 Exporting to {args.format}...")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
