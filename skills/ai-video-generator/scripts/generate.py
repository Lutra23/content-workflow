#!/usr/bin/env python3
"""
Anime Video Generator CLI - Main generation script
"""

import os
import sys
import argparse
from pathlib import Path
from lib.video_generator import AnimeVideoGenerator, VideoProvider, MotionPreset, CameraMotion


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime videos using AI providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to video
  %(prog)s text2video "少女在樱花下跳舞" --style anime --duration 5
  
  # Image to video
  %(prog)s image2video character.png --motion moderate --camera pan-left
  
  # Generate with specific provider
  %(prog)s text2video "anime scene" --provider kling --aspect 16:9
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Generation mode")
    
    # Text to video
    txt2vid_parser = subparsers.add_parser("text2video", help="Generate video from text")
    txt2vid_parser.add_argument("prompt", help="Video description")
    txt2vid_parser.add_argument("--style", default="anime", help="Visual style")
    txt2vid_parser.add_argument("--duration", type=float, default=5.0, help="Duration in seconds")
    txt2vid_parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    txt2vid_parser.add_argument("--aspect", default="16:9", help="Aspect ratio")
    txt2vid_parser.add_argument("--provider", default="auto", help="Video provider")
    txt2vid_parser.add_argument("--output", "-o", help="Output file path")
    
    # Image to video
    img2vid_parser = subparsers.add_parser("image2video", help="Animate static image")
    img2vid_parser.add_argument("image", help="Source image path")
    img2vid_parser.add_argument("--motion", default="moderate", 
                               choices=["none", "slight", "moderate", "strong", "extreme"],
                               help="Motion intensity")
    img2vid_parser.add_argument("--camera", default="static",
                               choices=["static", "pan-left", "pan-right", "tilt-up", "tilt-down", 
                                       "zoom-in", "zoom-out", "dolly-zoom", "orbit"],
                               help="Camera motion")
    img2vid_parser.add_argument("--duration", type=float, default=3.0, help="Duration in seconds")
    img2vid_parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    img2vid_parser.add_argument("--loop", action="store_true", help="Loop the video")
    img2vid_parser.add_argument("--provider", default="auto", help="Video provider")
    img2vid_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Initialize generator
    generator = AnimeVideoGenerator()
    
    # Parse provider
    provider_map = {
        "auto": VideoProvider.AUTO,
        "kling": VideoProvider.KLING,
        "svd": VideoProvider.STABLE_VIDEO_DIFFUSION,
        "runway": VideoProvider.RUNWAY
    }
    provider = provider_map.get(args.provider.lower(), VideoProvider.AUTO)
    
    if args.mode == "text2video":
        result = generator.text_to_video(
            prompt=args.prompt,
            style=args.style,
            duration=args.duration,
            fps=args.fps,
            aspect_ratio=args.aspect,
            provider=provider,
            output_path=args.output
        )
    
    elif args.mode == "image2video":
        result = generator.image_to_video(
            image=args.image,
            motion=args.motion,
            camera_motion=args.camera,
            duration=args.duration,
            fps=args.fps,
            loop=args.loop,
            provider=provider,
            output_path=args.output
        )
    
    # Output results
    if result.success:
        print(f"✅ Success! Video saved to: {result.video_path}")
        print(f"   Provider: {result.provider}")
        print(f"   Duration: {result.duration}s @ {result.fps}fps")
        print(f"   Resolution: {result.resolution[0]}x{result.resolution[1]}")
        return 0
    else:
        print(f"❌ Failed: {result.error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
