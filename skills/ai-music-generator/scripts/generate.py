#!/usr/bin/env python3
"""
Anime Music Generator CLI - Music generation script
"""

import os
import sys
import argparse
from pathlib import Path
from lib.music_generator import AnimeMusicGenerator, MusicProvider, MusicStyle, SceneType


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime music and sound effects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate background music
  %(prog)s bgm "anime school, gentle, warm" --duration 120 --style calm
  
  # Generate character theme
  %(prog)s theme "hero theme, epic, orchestral" --duration 60
  
  # Generate ambient soundscape
  %(prog)s ambient "forest, birds, wind" --duration 60
  
  # Generate sound effect
  %(prog)s sfx "sword swing" --category combat --intensity high
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Generation mode")
    
    # BGM mode
    bgm_parser = subparsers.add_parser("bgm", help="Generate background music")
    bgm_parser.add_argument("prompt", help="Music description")
    bgm_parser.add_argument("--style", 
                           choices=["calm", "upbeat", "dramatic", "action", "mysterious", "romantic"],
                           help="Music style")
    bgm_parser.add_argument("--duration", type=float, default=120.0, help="Duration in seconds")
    bgm_parser.add_argument("--bpm", type=int, help="Beats per minute")
    bgm_parser.add_argument("--loop", action="store_true", default=True, help="Loop seamlessly")
    bgm_parser.add_argument("--no-loop", dest="loop", action="store_false", help="Don't loop")
    bgm_parser.add_argument("--provider", default="auto", help="Music provider")
    bgm_parser.add_argument("--output", "-o", help="Output file path")
    bgm_parser.add_argument("--format", default="mp3", help="Output format")
    
    # Theme mode
    theme_parser = subparsers.add_parser("theme", help="Generate character theme")
    theme_parser.add_argument("prompt", help="Theme description")
    theme_parser.add_argument("--character", help="Character name")
    theme_parser.add_argument("--duration", type=float, default=60.0, help="Duration in seconds")
    theme_parser.add_argument("--lyrics", help="Song lyrics")
    theme_parser.add_argument("--output", "-o", help="Output file path")
    
    # Ambient mode
    ambient_parser = subparsers.add_parser("ambient", help="Generate ambient soundscape")
    ambient_parser.add_argument("prompt", help="Ambient description")
    ambient_parser.add_argument("--duration", type=float, default=60.0, help="Duration in seconds")
    ambient_parser.add_argument("--provider", default="auto", help="Music provider")
    ambient_parser.add_argument("--output", "-o", help="Output file path")
    
    # SFX mode
    sfx_parser = subparsers.add_parser("sfx", help="Generate sound effect")
    sfx_parser.add_argument("prompt", help="Sound description")
    sfx_parser.add_argument("--category", default="combat",
                           choices=["combat", "ambient", "ui", "voice", "environmental"],
                           help="SFX category")
    sfx_parser.add_argument("--duration", type=float, default=2.0, help="Duration in seconds")
    sfx_parser.add_argument("--intensity", default="medium",
                           choices=["low", "medium", "high"],
                           help="Sound intensity")
    sfx_parser.add_argument("--output", "-o", help="Output file path")
    
    # Scene mode
    scene_parser = subparsers.add_parser("scene", help="Generate music for scene")
    scene_parser.add_argument("description", help="Scene description")
    scene_parser.add_argument("scene_type",
                             choices=["school_day", "battle", "emotional", "romance", 
                                     "suspense", "comedy", "intro", "outro"],
                             help="Type of scene")
    scene_parser.add_argument("--duration", type=float, help="Duration in seconds")
    scene_parser.add_argument("--provider", default="auto", help="Music provider")
    scene_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Initialize generator
    generator = AnimeMusicGenerator()
    
    # Parse provider
    provider_map = {
        "auto": MusicProvider.AUTO,
        "mubert": MusicProvider.MUBERT,
        "musicgen": MusicProvider.MUSICGEN,
        "soundful": MusicProvider.SOUNDFUL
    }
    provider = provider_map.get(args.provider.lower(), MusicProvider.AUTO)
    
    if args.mode == "bgm":
        style = MusicStyle(args.style) if args.style else None
        
        result = generator.generate_bgm(
            prompt=args.prompt,
            style=style,
            duration=args.duration,
            bpm=args.bpm,
            loop=args.loop,
            provider=provider,
            output_path=args.output,
            output_format=args.format
        )
    
    elif args.mode == "theme":
        result = generator.generate_theme(
            prompt=args.prompt,
            character=args.character,
            duration=args.duration,
            lyrics=args.lyrics,
            output_path=args.output
        )
    
    elif args.mode == "ambient":
        result = generator.generate_ambient(
            prompt=args.prompt,
            duration=args.duration,
            provider=provider,
            output_path=args.output
        )
    
    elif args.mode == "sfx":
        result = generator.generate_sfx(
            prompt=args.prompt,
            category=args.category,
            duration=args.duration,
            intensity=args.intensity,
            output_path=args.output
        )
    
    elif args.mode == "scene":
        scene_type = SceneType(args.scene_type)
        
        result = generator.generate_for_scene(
            scene_description=args.description,
            scene_type=scene_type,
            duration=args.duration,
            provider=provider,
            output_path=args.output
        )
    
    # Output results
    if result.success:
        print(f"✅ Success! Audio saved to: {result.audio_path}")
        print(f"   Provider: {result.provider}")
        print(f"   Duration: {result.duration:.1f}s")
        if result.bpm:
            print(f"   BPM: {result.bpm}")
        if result.loopable:
            print(f"   Loopable: Yes")
        return 0
    else:
        print(f"❌ Failed: {result.error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
