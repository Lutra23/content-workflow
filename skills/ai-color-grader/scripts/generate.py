#!/usr/bin/env python3
"""
Color Grader CLI - Video color correction and style presets
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from color_grader import ColorGrader, ColorStyle


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Color Grader - Video color correction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply anime style
  %(prog)s apply video.mp4 graded.mp4 --style anime
  
  # Custom settings
  %(prog)s custom video.mp4 graded.mp4 --brightness 0.1 --contrast 0.2 --saturation 1.3
  
  # Auto color correction
  %(prog)s auto video.mp4 graded.mp4
  
  # Denoise
  %(prog)s denoise video.mp4 clean.mp4 --strength 5
  
  # Sharpen
  %(prog)s sharpen video.mp4 sharp.mp4 --strength 1.5
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Apply style
    apply_parser = subparsers.add_parser("apply", help="Apply color style")
    apply_parser.add_argument("input", help="Input video")
    apply_parser.add_argument("output", help="Output video")
    apply_parser.add_argument("--style", default="anime",
                             choices=["anime", "cinematic", "vintage", "bw", "sepia", 
                                     "cool", "warm", "high_contrast", "dreamy"])
    
    # Custom
    custom_parser = subparsers.add_parser("custom", help="Custom color settings")
    custom_parser.add_argument("input", help="Input video")
    custom_parser.add_argument("output", help="Output video")
    custom_parser.add_argument("--brightness", type=float, default=0.0)
    custom_parser.add_argument("--contrast", type=float, default=0.0)
    custom_parser.add_argument("--saturation", type=float, default=1.0)
    
    # Auto
    auto_parser = subparsers.add_parser("auto", help="Auto color correction")
    auto_parser.add_argument("input", help="Input video")
    auto_parser.add_argument("output", help="Output video")
    
    # Denoise
    denoise_parser = subparsers.add_parser("denoise", help="Denoise video")
    denoise_parser.add_argument("input", help="Input video")
    denoise_parser.add_argument("output", help="Output video")
    denoise_parser.add_argument("--strength", type=float, default=5.0)
    
    # Sharpen
    sharp_parser = subparsers.add_parser("sharpen", help="Sharpen video")
    sharp_parser.add_argument("input", help="Input video")
    sharp_parser.add_argument("output", help="Output video")
    sharp_parser.add_argument("--strength", type=float, default=1.0)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    grader = ColorGrader()
    
    if args.command == "apply":
        style = ColorStyle(args.style)
        grader.apply_style(Path(args.input), Path(args.output), style)
    
    elif args.command == "custom":
        grader.apply_custom(Path(args.input), Path(args.output),
                           args.brightness, args.contrast, args.saturation)
    
    elif args.command == "auto":
        grader.auto_color(Path(args.input), Path(args.output))
    
    elif args.command == "denoise":
        grader.denoise(Path(args.input), Path(args.output), args.strength)
    
    elif args.command == "sharpen":
        grader.sharpen(Path(args.input), Path(args.output), args.strength)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
