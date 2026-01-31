#!/usr/bin/env python3
"""
Video Editor CLI - Concatenate, trim, and combine video clips
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from video_editor import VideoEditor, Transition, AspectRatio


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Video Editor - Simple video editing with ffmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Concatenate videos
  %(prog)s concat clip1.mp4 clip2.mp4 clip3.mp4 -o combined.mp4
  
  # Trim video
  %(prog)s trim video.mp4 clip.mp4 --start 10 --end 30
  
  # Change speed
  %(prog)s speed video.mp4 fast.mp4 --speed 1.5
  
  # Add audio
  %(prog)s audio video.mp4 bgm.mp4 output.mp4
  
  # Resize
  %(prog)s resize video.mp4 small.mp4 --width 720 --height 480
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Concat
    concat_parser = subparsers.add_parser("concat", help="Concatenate videos")
    concat_parser.add_argument("inputs", nargs="+", help="Input files")
    concat_parser.add_argument("-o", "--output", required=True, help="Output file")
    
    # Trim
    trim_parser = subparsers.add_parser("trim", help="Trim video")
    trim_parser.add_argument("input", help="Input file")
    trim_parser.add_argument("output", help="Output file")
    trim_parser.add_argument("--start", type=float, required=True)
    trim_parser.add_argument("--end", type=float)
    trim_parser.add_argument("--duration", type=float)
    
    # Speed
    speed_parser = subparsers.add_parser("speed", help="Change speed")
    speed_parser.add_argument("input", help="Input file")
    speed_parser.add_argument("output", help="Output file")
    speed_parser.add_argument("--speed", type=float, default=1.0)
    
    # Audio
    audio_parser = subparsers.add_parser("audio", help="Add audio")
    audio_parser.add_argument("video", help="Video file")
    audio_parser.add_argument("audio", help="Audio file")
    audio_parser.add_argument("output", help="Output file")
    audio_parser.add_argument("--mix", action="store_true")
    
    # Resize
    resize_parser = subparsers.add_parser("resize", help="Resize video")
    resize_parser.add_argument("input", help="Input file")
    resize_parser.add_argument("output", help="Output file")
    resize_parser.add_argument("--width", type=int, required=True)
    resize_parser.add_argument("--height", type=int, required=True)
    
    # Subtitle
    sub_parser = subparsers.add_parser("subtitle", help="Add subtitles")
    sub_parser.add_argument("video", help="Video file")
    sub_parser.add_argument("subtitle", help="Subtitle file (SRT)")
    sub_parser.add_argument("output", help="Output file")
    
    # Info
    info_parser = subparsers.add_parser("info", help="Show video info")
    info_parser.add_argument("input", help="Input file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    editor = VideoEditor()
    
    if args.command == "concat":
        editor.concat([Path(f) for f in args.inputs], Path(args.output))
    
    elif args.command == "trim":
        editor.trim(Path(args.input), Path(args.output), args.start, args.end, args.duration)
    
    elif args.command == "speed":
        editor.change_speed(Path(args.input), Path(args.output), args.speed)
    
    elif args.command == "audio":
        editor.add_audio(Path(args.video), Path(args.audio), Path(args.output), args.mix)
    
    elif args.command == "resize":
        editor.resize(Path(args.input), Path(args.output), args.width, args.height)
    
    elif args.command == "subtitle":
        editor.add_subtitles(Path(args.video), Path(args.subtitle), Path(args.output))
    
    elif args.command == "info":
        info = editor.get_info(Path(args.input))
        if info:
            print("📹 Video Info:")
            for s in info.get("streams", []):
                if s.get("codec_type") == "video":
                    print(f"   Resolution: {s.get('width')}x{s.get('height')}")
                    print(f"   Frame Rate: {s.get('r_frame_rate')}")
                    print(f"   Codec: {s.get('codec_name')}")
                elif s.get("codec_type") == "audio":
                    print(f"   Audio: {s.get('codec_name')} ({s.get('channel_layout')})")
            duration = float(info["format"].get("duration", 0))
            size_mb = float(info["format"].get("size", 0)) / (1024*1024)
            print(f"   Duration: {duration:.1f}s")
            print(f"   Size: {size_mb:.2f} MB")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
