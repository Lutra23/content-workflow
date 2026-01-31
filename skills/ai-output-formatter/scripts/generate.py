#!/usr/bin/env python3
"""
Output Formatter CLI - Multi-format export and optimization
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from output_formatter import OutputFormatter, Platform, Quality, Format


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Output Formatter - Multi-format video export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export for YouTube
  %(prog)s export video.mp4 youtube_1080p.mp4 --platform youtube --quality high
  
  # Compress for Discord
  %(prog)s compress video.mp4 small.mp4 --quality medium
  
  # Generate GIF
  %(prog)s gif video.mp4 preview.gif --width 320
  
  # Show video info
  %(prog)s info video.mp4
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Export
    export_parser = subparsers.add_parser("export", help="Export video with preset")
    export_parser.add_argument("input", help="Input video file")
    export_parser.add_argument("output", help="Output file")
    export_parser.add_argument("--platform", "-p", default="youtube",
                               choices=["youtube", "bilibili", "twitter", "instagram", "web", "discord"],
                               help="Target platform")
    export_parser.add_argument("--quality", "-q", default="high",
                               choices=["low", "medium", "high", "ultra"],
                               help="Quality level")
    
    # Compress
    compress_parser = subparsers.add_parser("compress", help="Compress video")
    compress_parser.add_argument("input", help="Input video file")
    compress_parser.add_argument("output", help="Output file")
    compress_parser.add_argument("--quality", default="high",
                                 choices=["high", "medium", "low"],
                                 help="Compression quality")
    
    # GIF
    gif_parser = subparsers.add_parser("gif", help="Generate GIF")
    gif_parser.add_argument("input", help="Input video file")
    gif_parser.add_argument("output", help="Output GIF file")
    gif_parser.add_argument("--width", type=int, default=480, help="GIF width")
    gif_parser.add_argument("--fps", type=int, default=10, help="GIF frame rate")
    
    # Info
    info_parser = subparsers.add_parser("info", help="Show video information")
    info_parser.add_argument("input", help="Input video file")
    
    # Batch
    batch_parser = subparsers.add_parser("batch", help="Batch export")
    batch_parser.add_argument("input_dir", help="Input directory")
    batch_parser.add_argument("output_dir", help="Output directory")
    batch_parser.add_argument("--platform", "-p", default="youtube")
    batch_parser.add_argument("--quality", "-q", default="high")
    batch_parser.add_argument("--pattern", default="*.mp4", help="File pattern")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    formatter = OutputFormatter()
    
    if args.command == "export":
        platform_map = {
            "youtube": Platform.YOUTUBE,
            "bilibili": Platform.BILIBILI,
            "twitter": Platform.TWITTER,
            "instagram": Platform.INSTAGRAM,
            "web": Platform.WEB,
            "discord": Platform.DISCORD,
        }
        quality_map = {
            "low": Quality.LOW,
            "medium": Quality.MEDIUM,
            "high": Quality.HIGH,
            "ultra": Quality.ULTRA,
        }
        
        platform = platform_map.get(args.platform, Platform.YOUTUBE)
        quality = quality_map.get(args.quality, Quality.HIGH)
        
        formatter.export(Path(args.input), Path(args.output), platform, quality)
    
    elif args.command == "compress":
        formatter.compress(Path(args.input), Path(args.output), args.quality)
    
    elif args.command == "gif":
        formatter.generate_gif(Path(args.input), Path(args.output), args.width)
    
    elif args.command == "info":
        info = formatter.get_info(Path(args.input))
        if info:
            streams = info.get("streams", [])
            for s in streams:
                if s.get("codec_type") == "video":
                    print(f"📹 Video: {s.get('width')}x{s.get('height')} @ {s.get('r_frame_rate')}")
                elif s.get("codec_type") == "audio":
                    print(f"🔊 Audio: {s.get('codec_name')} {s.get('channel_layout')}")
            format_info = info.get("format", {})
            duration = float(format_info.get('duration', 0))
            print(f"📁 Duration: {duration:.1f}s")
            size_mb = float(format_info.get('size', 0)) / (1024*1024)
            print(f"💾 Size: {size_mb:.2f} MB")
        else:
            print("❌ Could not read video info")
    
    elif args.command == "batch":
        results = formatter.batch_export(
            Path(args.input_dir),
            Path(args.output_dir),
            Platform(args.platform),
            Quality(args.quality),
            args.pattern,
        )
        success = sum(1 for v in results.values() if v)
        print(f"✅ Batch complete: {success}/{len(results)} files exported")


if __name__ == "__main__":
    main()
