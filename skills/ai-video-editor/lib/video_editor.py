#!/usr/bin/env python3
"""
Video Editor - Concatenate, trim, and combine video clips

Simple video editing operations with ffmpeg.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transition(Enum):
    """Video transitions"""
    NONE = "none"
    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE = "wipe"


class AspectRatio(Enum):
    """Aspect ratios"""
    AR_16_9 = (16, 9)
    AR_9_16 = (9, 16)  # Vertical
    AR_1_1 = (1, 1)    # Square
    AR_4_3 = (4, 3)
    AR_21_9 = (21, 9)  # Ultrawide


@dataclass
class Clip:
    """Video clip configuration"""
    path: str
    start: float = 0.0      # Start time (seconds)
    duration: Optional[float] = None  # Duration (None = until end)
    speed: float = 1.0      # Playback speed
    fade_in: float = 0.0    # Fade in duration
    fade_out: float = 0.0   # Fade out duration


class VideoEditor:
    """Main video editor class"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        self.ffmpeg = ffmpeg_path
        self.ffprobe = ffprobe_path
    
    def _run_cmd(self, cmd: List[str]) -> bool:
        """Run ffmpeg command"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"❌ FFmpeg error: {result.stderr}")
                return False
            return True
        except FileNotFoundError:
            logger.error("❌ ffmpeg not found. Install with: apt install ffmpeg")
            return False
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False
    
    def get_duration(self, file_path: Path) -> float:
        """Get video duration in seconds"""
        cmd = [
            self.ffprobe, "-v", "error",
            "-print_format", "json",
            "-show_format", "-show_streams",
            str(file_path),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except Exception:
            return 0.0
    
    def concat(
        self,
        input_files: List[Path],
        output_file: Path,
        transition: Transition = Transition.NONE,
        transition_duration: float = 0.5,
    ) -> bool:
        """Concatenate multiple video files"""
        if len(input_files) < 2:
            logger.error("❌ Need at least 2 files to concatenate")
            return False
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create concat list file
        list_file = output_file.with_suffix(".txt")
        with open(list_file, "w") as f:
            for file in input_files:
                f.write(f"file '{file.absolute()}'\n")
        
        # Build ffmpeg command
        cmd = [
            self.ffmpeg, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(output_file),
        ]
        
        logger.info(f"🔀 Concatenating {len(input_files)} files...")
        
        if self._run_cmd(cmd):
            list_file.unlink()  # Clean up
            size_mb = output_file.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Concatenated: {output_file} ({size_mb:.2f} MB)")
            return True
        
        return False
    
    def concat_with_transition(
        self,
        clips: List[Clip],
        output_file: Path,
        transition: Transition = Transition.FADE,
        transition_duration: float = 0.5,
    ) -> bool:
        """Concatenate clips with transitions"""
        if len(clips) < 2:
            logger.error("❌ Need at least 2 clips")
            return False
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Build filter complex for transitions
        filter_parts = []
        inputs = []
        for i, clip in enumerate(clips):
            inputs.extend(["-i", clip.path])
        
        # Simple fade transition
        if transition == Transition.FADE:
            # Use xfade filter
            filter_complex = ""
            for i in range(len(clips)):
                if clip.fade_in > 0:
                    pass  # Would add fade filter here
            
            # Simplified: just concat with dissolve
            cmd = [self.ffmpeg, "-y"]
            for clip in clips:
                cmd.extend(["-i", clip.path])
            
            # Use xfade
            num_inputs = len(clips)
            cmd.extend([
                "-filter_complex",
                f"[0:v][1:v]xfade=transition=dissolve:duration={transition_duration}:offset=1[v];[v][2:v]xfade=transition=dissolve:duration={transition_duration}[v2]",
                "-map", "[v]",
                "-map", "[a]",
                str(output_file),
            ])
        
        else:
            # Simple concat without transition
            return self.concat([Path(c.path) for c in clips], output_file)
        
        return self._run_cmd(cmd)
    
    def trim(
        self,
        input_file: Path,
        output_file: Path,
        start: float,
        end: Optional[float] = None,
        duration: Optional[float] = None,
    ) -> bool:
        """Trim video clip"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.ffmpeg, "-y",
            "-ss", str(start),
        ]
        
        if end:
            cmd.extend(["-to", str(end)])
        elif duration:
            cmd.extend(["-t", str(duration)])
        
        cmd.extend([
            "-i", str(input_file),
            "-c", "copy",
            str(output_file),
        ])
        
        logger.info(f"✂️  Trimming: {input_file.name} {start}s -> {end or duration}s")
        
        if self._run_cmd(cmd):
            size_mb = output_file.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Trimmed: {output_file} ({size_mb:.2f} MB)")
            return True
        
        return False
    
    def change_speed(
        self,
        input_file: Path,
        output_file: Path,
        speed: float = 1.0,
    ) -> bool:
        """Change video playback speed"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # video speed filter
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(input_file),
            "-filter:v", f"setpts={1/speed}*PTS",
            "-filter:a", f"atempo={speed}",
            str(output_file),
        ]
        
        logger.info(f"⏩ Speed: {speed}x")
        
        return self._run_cmd(cmd)
    
    def add_audio(
        self,
        video_file: Path,
        audio_file: Path,
        output_file: Path,
        mix: bool = True,
        audio_offset: float = 0.0,
    ) -> bool:
        """Add/replace audio in video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video_file),
            "-i", str(audio_file),
        ]
        
        if mix:
            # Mix with original audio
            cmd.extend([
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first",
            ])
        else:
            # Replace audio
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        
        cmd.extend([
            "-c:v", "copy",
            str(output_file),
        ])
        
        logger.info(f"🎵 Adding audio: {audio_file.name}")
        
        return self._run_cmd(cmd)
    
    def extract_audio(
        self,
        video_file: Path,
        output_file: Path,
        format: str = "mp3",
    ) -> bool:
        """Extract audio from video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video_file),
            "-vn",
            "-acodec", "libmp3lame" if format == "mp3" else "aac",
            str(output_file),
        ]
        
        return self._run_cmd(cmd)
    
    def resize(
        self,
        input_file: Path,
        output_file: Path,
        width: int,
        height: int,
        keep_aspect: bool = True,
    ) -> bool:
        """Resize video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        scale_filter = f"scale={width}:{height}"
        if keep_aspect:
            scale_filter += ":force_original_aspect_ratio=decrease"
            # Add padding to maintain exact size
            scale_filter += f",pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(input_file),
            "-vf", scale_filter,
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info(f"📐 Resizing: {width}x{height}")
        
        return self._run_cmd(cmd)
    
    def change_ar(
        self,
        input_file: Path,
        output_file: Path,
        aspect_ratio: AspectRatio,
    ) -> bool:
        """Change aspect ratio"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        ar = aspect_ratio.value[0] / aspect_ratio.value[1]
        
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(input_file),
            "-aspect", str(ar),
            "-c", "copy",
            str(output_file),
        ]
        
        logger.info(f"📐 Aspect ratio: {aspect_ratio.value[0]}:{aspect_ratio.value[1]}")
        
        return self._run_cmd(cmd)
    
    def add_subtitles(
        self,
        video_file: Path,
        subtitle_file: Path,
        output_file: Path,
    ) -> bool:
        """Add subtitles to video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video_file),
            "-vf", f"subtitles={subtitle_file}",
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info(f"📝 Adding subtitles: {subtitle_file.name}")
        
        return self._run_cmd(cmd)
    
    def take_screenshot(
        self,
        input_file: Path,
        output_file: Path,
        timestamp: float = 0.0,
        width: Optional[int] = None,
    ) -> bool:
        """Take screenshot at timestamp"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.ffmpeg, "-y",
            "-ss", str(timestamp),
            "-i", str(input_file),
            "-vframes", "1",
        ]
        
        if width:
            cmd.extend(["-vf", f"scale={width}:-1"])
        
        cmd.append(str(output_file))
        
        return self._run_cmd(cmd)
    
    def get_info(self, input_file: Path) -> Dict[str, Any]:
        """Get video information"""
        cmd = [
            self.ffprobe, "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(input_file),
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception:
            return {}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Video Editor")
    subparsers = parser.add_subparsers(dest="command")
    
    # Concat
    concat_parser = subparsers.add_parser("concat", help="Concatenate videos")
    concat_parser.add_argument("inputs", nargs="+", help="Input files")
    concat_parser.add_argument("output", help="Output file")
    
    # Trim
    trim_parser = subparsers.add_parser("trim", help="Trim video")
    trim_parser.add_argument("input", help="Input file")
    trim_parser.add_argument("output", help="Output file")
    trim_parser.add_argument("--start", type=float, required=True)
    trim_parser.add_argument("--end", type=float, help="End time")
    trim_parser.add_argument("--duration", type=float, help="Duration")
    
    # Speed
    speed_parser = subparsers.add_parser("speed", help="Change speed")
    speed_parser.add_argument("input", help="Input file")
    speed_parser.add_argument("output", help="Output file")
    speed_parser.add_argument("--speed", type=float, default=1.0)
    
    # Audio
    add_audio_parser = subparsers.add_parser("audio", help="Add audio")
    add_audio_parser.add_argument("video", help="Video file")
    add_audio_parser.add_argument("audio", help="Audio file")
    add_audio_parser.add_argument("output", help="Output file")
    add_audio_parser.add_argument("--mix", action="store_true", help="Mix with original")
    
    # Resize
    resize_parser = subparsers.add_parser("resize", help="Resize video")
    resize_parser.add_argument("input", help="Input file")
    resize_parser.add_argument("output", help="Output file")
    resize_parser.add_argument("--width", type=int, required=True)
    resize_parser.add_argument("--height", type=int, required=True)
    
    # Info
    info_parser = subparsers.add_parser("info", help="Show video info")
    info_parser.add_argument("input", help="Input file")
    
    args = parser.parse_args()
    
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
    
    elif args.command == "info":
        info = editor.get_info(Path(args.input))
        if info:
            for s in info.get("streams", []):
                if s.get("codec_type") == "video":
                    print(f"📹 {s.get('width')}x{s.get('height')} @ {s.get('r_frame_rate')}")
                elif s.get("codec_type") == "audio":
                    print(f"🔊 {s.get('codec_name')}")
            duration = float(info["format"].get("duration", 0))
            print(f"⏱️  {duration:.1f}s")
    
    else:
        parser.print_help()
