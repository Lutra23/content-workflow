#!/usr/bin/env python3
"""
Output Formatter - Multi-format export and optimization for anime productions

Supports: MP4, WebM, GIF, MOV, with platform-specific presets.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Format(Enum):
    """Output formats"""
    MP4 = "mp4"
    WEBM = "webm"
    GIF = "gif"
    MOV = "mov"
    MKV = "mkv"


class Platform(Enum):
    """Target platforms"""
    YOUTUBE = "youtube"
    BILIBILI = "bilibili"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    WEB = "web"
    DISCORD = "discord"
    CUSTOM = "custom"


class Quality(Enum):
    """Quality presets"""
    LOW = "low"      # 480p
    MEDIUM = "medium" # 720p
    HIGH = "high"    # 1080p
    ULTRA = "ultra"  # 4K


@dataclass
class ExportPreset:
    """Export preset configuration"""
    name: str
    format: Format
    platform: Platform
    resolution: tuple  # (width, height)
    fps: int = 24
    bitrate: str = "8M"
    codec: str = "libx264"
    audio_codec: str = "aac"
    extra_args: List[str] = field(default_factory=list)
    
    def get_cmd_args(self, input_file: Path, output_file: Path) -> List[str]:
        """Generate ffmpeg arguments"""
        args = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-c:v", self.codec,
            "-c:a", self.audio_codec,
            "-b:v", self.bitrate,
            "-vf", f"scale={self.resolution[0]}:{self.resolution[1]}",
            "-r", str(self.fps),
        ]
        args.extend(self.extra_args)
        args.extend(["-movflags", "+faststart"])  # For web streaming
        args.append(str(output_file))
        return args


# Presets
PRESETS = {
    # YouTube presets
    (Platform.YOUTUBE, Quality.HIGH): ExportPreset(
        name="youtube_1080p",
        format=Format.MP4,
        platform=Platform.YOUTUBE,
        resolution=(1920, 1080),
        fps=30,
        bitrate="12M",
    ),
    (Platform.YOUTUBE, Quality.ULTRA): ExportPreset(
        name="youtube_4k",
        format=Format.MP4,
        platform=Platform.YOUTUBE,
        resolution=(3840, 2160),
        fps=30,
        bitrate="35M",
    ),
    
    # Bilibili presets
    (Platform.BILIBILI, Quality.HIGH): ExportPreset(
        name="bilibili_1080p",
        format=Format.MP4,
        platform=Platform.BILIBILI,
        resolution=(1920, 1080),
        fps=30,
        bitrate="10M",
    ),
    
    # Twitter/X presets (shorter, smaller)
    (Platform.TWITTER, Quality.MEDIUM): ExportPreset(
        name="twitter_720p",
        format=Format.MP4,
        platform=Platform.TWITTER,
        resolution=(1280, 720),
        fps=30,
        bitrate="5M",
        extra_args=["-tune", "film"],
    ),
    
    # Instagram presets (square/portrait)
    (Platform.INSTAGRAM, Quality.MEDIUM): ExportPreset(
        name="instagram_1080p",
        format=Format.MP4,
        platform=Platform.INSTAGRAM,
        resolution=(1080, 1080),
        fps=30,
        bitrate="6M",
    ),
    
    # Web presets (smaller, optimized)
    (Platform.WEB, Quality.MEDIUM): ExportPreset(
        name="web_720p",
        format=Format.WEBM,
        platform=Platform.WEB,
        resolution=(1280, 720),
        fps=24,
        bitrate="3M",
        codec="libvpx-vp9",
        audio_codec="libopus",
    ),
    
    # Discord presets (small file size)
    (Platform.DISCORD, Quality.LOW): ExportPreset(
        name="discord_480p",
        format=Format.MP4,
        platform=Platform.DISCORD,
        resolution=(854, 480),
        fps=24,
        bitrate="2M",
    ),
}


class OutputFormatter:
    """Main formatter class"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg = ffmpeg_path
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            result = subprocess.run(
                [self.ffmpeg, "-version"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                logger.warning("⚠️  ffmpeg not found. Some features will be limited.")
        except FileNotFoundError:
            logger.warning("⚠️  ffmpeg not found. Install with: apt install ffmpeg")
    
    def get_preset(self, platform: Platform, quality: Quality) -> ExportPreset:
        """Get export preset"""
        key = (platform, quality)
        if key not in PRESETS:
            # Fallback to custom
            return ExportPreset(
                name="custom",
                format=Format.MP4,
                platform=platform,
                resolution=(1280, 720),
            )
        return PRESETS[key]
    
    def export(
        self,
        input_file: Path,
        output_file: Path,
        platform: Platform,
        quality: Quality = Quality.HIGH,
        preset: Optional[ExportPreset] = None,
    ) -> bool:
        """Export video with preset"""
        if not input_file.exists():
            logger.error(f"❌ Input file not found: {input_file}")
            return False
        
        if preset is None:
            preset = self.get_preset(platform, quality)
        
        logger.info(f"📦 Exporting: {input_file.name}")
        logger.info(f"   Platform: {platform.value}, Quality: {quality.value}")
        logger.info(f"   Resolution: {preset.resolution[0]}x{preset.resolution[1]}")
        
        # Create output directory
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Build and run ffmpeg command
        cmd = preset.get_cmd_args(input_file, output_file)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 min timeout
            )
            
            if result.returncode == 0:
                size_mb = output_file.stat().st_size / (1024 * 1024)
                logger.info(f"✅ Exported: {output_file}")
                logger.info(f"   Size: {size_mb:.2f} MB")
                return True
            else:
                logger.error(f"❌ Export failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Export timeout (10 min)")
            return False
        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return False
    
    def compress(
        self,
        input_file: Path,
        output_file: Path,
        quality: str = "high",
    ) -> bool:
        """Compress video with quality trade-off"""
        quality_map = {
            "high": {"crf": 18, "preset": "slow"},
            "medium": {"crf": 23, "preset": "medium"},
            "low": {"crf": 28, "preset": "fast"},
        }
        
        q = quality_map.get(quality, quality_map["medium"])
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-crf", str(q["crf"]),
            "-preset", q["preset"],
            "-c:a", "aac",
            "-b:a", "128k",
            str(output_file),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                orig_size = input_file.stat().st_size / (1024 * 1024)
                new_size = output_file.stat().st_size / (1024 * 1024)
                ratio = (1 - new_size / orig_size) * 100
                logger.info(f"✅ Compressed: {orig_size:.2f}MB → {new_size:.2f}MB ({ratio:.1f}% smaller)")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Compress error: {e}")
            return False
    
    def extract_frames(
        self,
        input_file: Path,
        output_dir: Path,
        fps: int = 1,
    ) -> bool:
        """Extract frames from video"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", f"fps={fps}",
            str(output_dir / "frame_%04d.png"),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                frames = list(output_dir.glob("frame_*.png"))
                logger.info(f"✅ Extracted {len(frames)} frames to {output_dir}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Extract error: {e}")
            return False
    
    def generate_gif(
        self,
        input_file: Path,
        output_file: Path,
        width: int = 480,
        fps: int = 10,
    ) -> bool:
        """Generate GIF from video"""
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos",
            "-c:v", "gif",
            str(output_file),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size_kb = output_file.stat().st_size / 1024
                logger.info(f"✅ GIF: {output_file} ({size_kb:.1f} KB)")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ GIF error: {e}")
            return False
    
    def batch_export(
        self,
        input_dir: Path,
        output_dir: Path,
        platform: Platform,
        quality: Quality,
        pattern: str = "*.mp4",
    ) -> Dict[str, bool]:
        """Batch export videos"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        for input_file in input_dir.glob(pattern):
            output_file = output_dir / f"{input_file.stem}_{platform.value}.{Format.MP4.value}"
            success = self.export(input_file, output_file, platform, quality)
            results[str(input_file)] = success
        
        return results
    
    def get_info(self, input_file: Path) -> Dict[str, Any]:
        """Get video information"""
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(input_file),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception:
            pass
        return {}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Output Formatter")
    subparsers = parser.add_subparsers(dest="command")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export with preset")
    export_parser.add_argument("input", help="Input video file")
    export_parser.add_argument("output", help="Output file")
    export_parser.add_argument("--platform", default="youtube", help="Target platform")
    export_parser.add_argument("--quality", default="high", help="Quality level")
    
    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress video")
    compress_parser.add_argument("input", help="Input video file")
    compress_parser.add_argument("output", help="Output file")
    compress_parser.add_argument("--quality", default="high", help="Compression quality")
    
    # GIF command
    gif_parser = subparsers.add_parser("gif", help="Generate GIF")
    gif_parser.add_argument("input", help="Input video file")
    gif_parser.add_argument("output", help="Output GIF file")
    gif_parser.add_argument("--width", type=int, default=480, help="GIF width")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show video info")
    info_parser.add_argument("input", help="Input video file")
    
    args = parser.parse_args()
    
    formatter = OutputFormatter()
    
    if args.command == "export":
        platform = Platform(args.platform)
        quality = Quality(args.quality)
        formatter.export(Path(args.input), Path(args.output), platform, quality)
    
    elif args.command == "compress":
        formatter.compress(Path(args.input), Path(args.output), args.quality)
    
    elif args.command == "gif":
        formatter.generate_gif(Path(args.input), Path(args.output), args.width)
    
    elif args.command == "info":
        info = formatter.get_info(Path(args.input))
        if info:
            # Print simplified info
            streams = info.get("streams", [])
            for s in streams:
                if s.get("codec_type") == "video":
                    print(f"📹 Video: {s.get('width')}x{s.get('height')} @ {s.get('r_frame_rate')}")
                elif s.get("codec_type") == "audio":
                    print(f"🔊 Audio: {s.get('codec_name')} {s.get('channel_layout')}")
            format = info.get("format", {})
            print(f"📁 Duration: {float(format.get('duration', 0)):.1f}s")
            print(f"💾 Size: {float(format.get('size', 0)) / (1024*1024):.2f} MB")
        else:
            print("❌ Could not read video info")
    
    else:
        parser.print_help()
