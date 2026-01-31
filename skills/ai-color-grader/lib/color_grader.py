#!/usr/bin/env python3
"""
Color Grader - Video color correction and style presets

Apply anime-style color grading with ffmpeg filters.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ColorStyle(Enum):
    """Preset color styles"""
    NONE = "none"
    ANIME = "anime"          # Anime-style punchy colors
    CINEMATIC = "cinematic"  # Cinematic teal/orange
    VINTAGE = "vintage"      # Vintage film look
    B_W = "bw"               # Black and white
    SEPIA = "sepia"          # Sepia tone
    COOL = "cool"            # Cool blue tones
    WARM = "warm"            # Warm orange tones
    HIGH_CONTRAST = "high_contrast"  # Punchy contrast
    DREAMY = "dreamy"        // Soft, dreamy look


@dataclass
class ColorParams:
    """Color correction parameters"""
    brightness: float = 0.0      # -1.0 to 1.0
    contrast: float = 0.0        # -2.0 to 2.0
    saturation: float = 1.0      # 0.0 to 3.0
    hue_saturation: float = 0.0  # Hue shift
    temperature: float = 0.0     # Cool (-1) to Warm (+1)
    vibrance: float = 1.0        # 0.0 to 3.0
    shadows: float = 0.0         # Shadows adjustment
    highlights: float = 0.0      # Highlights adjustment
    gamma: float = 1.0           # 0.1 to 3.0
    
    def to_3dlut(self) -> str:
        """Generate 3DLUT string (simplified)"""
        return f"eq=brightness={self.brightness}:contrast={self.contrast}:saturation={self.saturation}"


# Style presets
STYLES = {
    ColorStyle.ANIME: ColorParams(
        brightness=0.05,
        contrast=0.2,
        saturation=1.3,
        vibrance=1.2,
    ),
    ColorStyle.CINEMATIC: ColorParams(
        brightness=0.0,
        contrast=0.3,
        saturation=0.9,
        temperature=0.1,
        shadows=-0.1,
        highlights=0.1,
    ),
    ColorStyle.VINTAGE: ColorParams(
        brightness=0.05,
        contrast=0.1,
        saturation=0.8,
        temperature=0.2,
    ),
    ColorStyle.B_W: ColorParams(
        brightness=0.0,
        contrast=0.2,
        saturation=0.0,
    ),
    ColorStyle.SEPIA: ColorParams(
        brightness=0.0,
        contrast=0.1,
        saturation=0.3,
    ),
    ColorStyle.COOL: ColorParams(
        brightness=0.0,
        contrast=0.1,
        saturation=1.1,
        temperature=-0.2,
    ),
    ColorStyle.WARM: ColorParams(
        brightness=0.0,
        contrast=0.1,
        saturation=1.1,
        temperature=0.2,
    ),
    ColorStyle.HIGH_CONTRAST: ColorParams(
        brightness=0.0,
        contrast=0.5,
        saturation=1.2,
        vibrance=1.3,
    ),
    ColorStyle.DREAMY: ColorParams(
        brightness=0.1,
        contrast=-0.1,
        saturation=0.9,
        vibrance=0.8,
    ),
}


class ColorGrader:
    """Main color grader class"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg = ffmpeg_path
    
    def _run_cmd(self, cmd: List[str]) -> bool:
        """Run ffmpeg command"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"❌ FFmpeg error: {result.stderr}")
                return False
            return True
        except FileNotFoundError:
            logger.error("❌ ffmpeg not found")
            return False
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False
    
    def apply_style(
        self,
        input_file: Path,
        output_file: Path,
        style: ColorStyle,
        custom_params: Optional[ColorParams] = None,
    ) -> bool:
        """Apply color style to video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if style == ColorStyle.NONE:
            # Just copy
            cmd = ["ffmpeg", "-y", "-i", str(input_file), "-c", "copy", str(output_file)]
            return self._run_cmd(cmd)
        
        # Get params
        params = custom_params or STYLES.get(style, ColorParams())
        
        # Build color filter
        filter_parts = []
        
        # Brightness/Contrast
        if params.brightness != 0 or params.contrast != 0:
            filter_parts.append(f"eq=brightness={params.brightness}:contrast={params.contrast}")
        
        # Saturation
        if params.saturation != 1.0:
            filter_parts.append(f"eq=saturation={params.saturation}")
        
        # Vibrance (using colorbalance for similar effect)
        if params.vibrance != 1.0:
            filter_parts.append(f"vibrance={params.vibrance}")
        
        # Temperature (color balance)
        if params.temperature != 0:
            # Adjust shadows and highlights for temperature effect
            shadow_adj = params.temperature * -0.1
            highlight_adj = params.temperature * 0.1
            filter_parts.append(f"colorbalance=rs={shadow_adj}:gs={shadow_adj}:bs={shadow_adj}:rh={highlight_adj}:gh={highlight_adj}:bh={highlight_adj}")
        
        # Special filters for styles
        if style == ColorStyle.ANIME:
            # Anime punchiness
            filter_parts.append("curves=vintage")
            filter_parts.append("色度键=0.1:0.5")  # Simplify
        
        elif style == ColorStyle.VINTAGE:
            filter_parts.append("colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131")
        
        elif style == ColorStyle.SEPIA:
            filter_parts.append("colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131")
        
        elif style == ColorStyle.B_W:
            filter_parts.append("format=gray")
        
        elif style == ColorStyle.DREAMY:
            # Soften
            filter_parts.append("boxblur=lr=2")
        
        # Build filter string
        filter_str = ",".join(filter_parts) if filter_parts else "null"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", filter_str,
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info(f"🎨 Applying style: {style.value}")
        
        if self._run_cmd(cmd):
            size_mb = output_file.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Graded: {output_file} ({size_mb:.2f} MB)")
            return True
        
        return False
    
    def apply_custom(
        self,
        input_file: Path,
        output_file: Path,
        brightness: float = 0.0,
        contrast: float = 0.0,
        saturation: float = 1.0,
        vibrance: float = 1.0,
    ) -> bool:
        """Apply custom color settings"""
        params = ColorParams(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            vibrance=vibrance,
        )
        return self.apply_style(input_file, output_file, ColorStyle.NONE, params)
    
    def auto_color(
        self,
        input_file: Path,
        output_file: Path,
    ) -> bool:
        """Auto color correction using histogram equalization"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Use histogram equalization for auto correction
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", "histeq=strength=0.5:intensity=0.5",
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info("🎨 Auto color correction")
        
        return self._run_cmd(cmd)
    
    def adjust_exposure(
        self,
        input_file: Path,
        output_file: Path,
        exposure: float = 0.0,  # -1.0 to 1.0
    ) -> bool:
        """Adjust exposure"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # exposure adjustment via eq
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", f"eq=brightness={exposure}",
            "-c:a", "copy",
            str(output_file),
        ]
        
        return self._run_cmd(cmd)
    
    def auto_levels(
        self,
        input_file: Path,
        output_file: Path,
    ) -> bool:
        """Auto levels correction"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", "normalize",
            "-c:a", "copy",
            str(output_file),
        ]
        
        return self._run_cmd(cmd)
    
    def denoise(
        self,
        input_file: Path,
        output_file: Path,
        strength: float = 5.0,
    ) -> bool:
        """Denoise video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", f"nlmeans=s={strength}",
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info(f"🧹 Denoising (strength={strength})")
        
        return self._run_cmd(cmd)
    
    def sharpen(
        self,
        input_file: Path,
        output_file: Path,
        strength: float = 1.0,
    ) -> bool:
        """Sharpen video"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", f"unsharp=5:5:{strength}:5:5:{strength}",
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info(f"🔪 Sharpening (strength={strength})")
        
        return self._run_cmd(cmd)
    
    def get_info(self, input_file: Path) -> Dict[str, Any]:
        """Get video color info"""
        cmd = [
            "ffprobe", "-v", "error",
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


class AnimeColorGrader(ColorGrader):
    """Anime-specific color grading"""
    
    def apply_anime_style(
        self,
        input_file: Path,
        output_file: Path,
        strength: float = 1.0,
    ) -> bool:
        """Apply anime-style color grading"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Anime-style filter chain
        # 1. Slight contrast bump
        # 2. Vibrance boost
        # 3. Subtle saturation
        filter_str = (
            "eq=contrast=1.1,"
            "vibrance=1.1,"
            "eq=saturation=1.1,"
            "curves=vintage"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", filter_str,
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info("🎨 Applying anime style")
        
        return self._run_cmd(cmd)
    
    def fix_anime_upscaling(
        self,
        input_file: Path,
        output_file: Path,
    ) -> bool:
        """Fix common anime upscaling artifacts"""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Sharpen slightly to fix soft upscaling
        # Denoise to remove compression artifacts
        filter_str = "unsharp=3:3:1.5:3:3:1.5,nlmeans=s=3"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vf", filter_str,
            "-c:a", "copy",
            str(output_file),
        ]
        
        logger.info("🔧 Fixing upscaling artifacts")
        
        return self._run_cmd(cmd)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Color Grader")
    subparsers = parser.add_subparsers(dest="command")
    
    # Apply style
    style_parser = subparsers.add_parser("apply", help="Apply color style")
    style_parser.add_argument("input", help="Input video")
    style_parser.add_argument("output", help="Output video")
    style_parser.add_argument("--style", default="anime",
                             choices=["anime", "cinematic", "vintage", "bw", "sepia", "cool", "warm", "high_contrast", "dreamy"])
    
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
