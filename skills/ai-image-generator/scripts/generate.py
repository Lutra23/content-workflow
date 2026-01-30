#!/usr/bin/env python3
"""
Anime Image Generator CLI - Single image generation script
"""

import os
import sys
import argparse
from pathlib import Path
from lib.image_generator import AnimeImageGenerator, Provider, QualityMode, ImageType


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime images using AI providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate anime character
  %(prog)s character "少女，蓝色长发，粉色眼睛，校园制服" --style anime
  
  # Generate background scene
  %(prog)s background "樱花盛开的校园，春天，傍晚" --size 1920x1080
  
  # Use specific provider
  %(prog)s character "cute anime girl" --provider stable-diffusion --style anime
  
  # High quality generation
  %(prog)s character "anime portrait" --quality high --output ./output.png
        """
    )
    
    # Subcommands for image types
    subparsers = parser.add_subparsers(dest="image_type", help="Type of image to generate")
    
    # Character generation
    char_parser = subparsers.add_parser("character", help="Generate anime character")
    char_parser.add_argument("prompt", help="Character description")
    char_parser.add_argument("--style", default="anime", help="Style preset (default: anime)")
    char_parser.add_argument("--size", default="1024x1024", help="Image size WxH (default: 1024x1024)")
    char_parser.add_argument("--provider", default="auto", help="AI provider (auto/stable-diffusion/dall-e/flux)")
    char_parser.add_argument("--quality", default="high", choices=["draft", "fast", "high"], help="Quality mode")
    char_parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    char_parser.add_argument("--output", "-o", help="Output file path")
    
    # Background generation
    bg_parser = subparsers.add_parser("background", help="Generate anime background")
    bg_parser.add_argument("prompt", help="Scene description")
    bg_parser.add_argument("--style", default="anime", help="Style preset (default: anime)")
    bg_parser.add_argument("--size", default="1920x1080", help="Image size WxH (default: 1920x1080)")
    bg_parser.add_argument("--perspective", default="normal", 
                          choices=["normal", "wide", "aerial", "low", "close-up"],
                          help="Perspective type")
    bg_parser.add_argument("--provider", default="auto", help="AI provider")
    bg_parser.add_argument("--quality", default="high", choices=["draft", "fast", "high"], help="Quality mode")
    bg_parser.add_argument("--output", "-o", help="Output file path")
    
    # Direct generation
    direct_parser = subparsers.add_parser("generate", help="Direct generation without type-specific options")
    direct_parser.add_argument("prompt", help="Image description")
    direct_parser.add_argument("--style", default="anime", help="Style preset")
    direct_parser.add_argument("--size", default="1024x1024", help="Image size WxH")
    direct_parser.add_argument("--provider", default="auto", help="AI provider")
    direct_parser.add_argument("--quality", default="high", choices=["draft", "fast", "high"], help="Quality mode")
    direct_parser.add_argument("--output", "-o", help="Output file path")
    
    # Common options
    parser.add_argument("--config-dir", help="Config directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not args.image_type:
        parser.print_help()
        sys.exit(1)
    
    # Parse size
    width, height = map(int, args.size.split('x'))
    
    # Parse provider
    provider_map = {
        "auto": Provider.AUTO,
        "stable-diffusion": Provider.STABLE_DIFFUSION,
        "dall-e": Provider.DALL_E,
        "flux": Provider.FLUX,
        "midjourney": Provider.MIDJOURNEY,
        "kling": Provider.KLING
    }
    provider = provider_map.get(args.provider.lower(), Provider.AUTO)
    
    # Parse quality
    quality = QualityMode(args.quality)
    
    # Initialize generator
    generator = AnimeImageGenerator(config_dir=args.config_dir)
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Generate based on image type
    if args.image_type == "character":
        result = generator.generate_character(
            prompt=args.prompt,
            style=args.style,
            size=(width, height),
            provider=provider,
            quality=quality,
            seed=args.seed,
            output_path=args.output
        )
    elif args.image_type == "background":
        result = generator.generate_background(
            prompt=args.prompt,
            style=args.style,
            size=(width, height),
            perspective=args.perspective,
            provider=provider,
            quality=quality,
            output_path=args.output
        )
    else:
        # Direct generation
        result = generator._generate(
            prompt=generator._format_prompt(args.prompt, args.style),
            image_type=ImageType.CHARACTER,
            size=(width, height),
            provider=provider,
            quality=quality,
            output_path=args.output
        )
    
    # Output results
    if result.success:
        print(f"✅ Success! Image saved to: {result.image_path}")
        print(f"   Provider: {result.provider}")
        print(f"   Prompt: {result.prompt_used[:80]}..." if len(result.prompt_used or "") > 80 else f"   Prompt: {result.prompt_used}")
        if result.seed:
            print(f"   Seed: {result.seed}")
        return 0
    else:
        print(f"❌ Failed: {result.error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
