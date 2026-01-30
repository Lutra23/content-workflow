"""
Subtitle Generation Module

提供字幕生成和同步功能，使用OpenAI Whisper进行语音识别。
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class Subtitle:
    """字幕数据类"""
    index: int
    start_time: float  # 秒
    end_time: float    # 秒
    text: str
    
    def to_srt(self, index: int = None) -> str:
        """转换为SRT格式"""
        idx = index if index is not None else self.index
        start = self._format_time(self.start_time, True)
        end = self._format_time(self.end_time, True)
        return f"{idx}\n{start} --> {end}\n{self.text}\n"
    
    def to_vtt(self) -> str:
        """转换为VTT格式"""
        start = self._format_time(self.start_time, False)
        end = self._format_time(self.end_time, False)
        return f"{start} --> {end}\n{self.text}\n"
    
    def to_ass(self, style: Dict = None) -> str:
        """转换为ASS格式"""
        start = self._format_ass_time(self.start_time)
        end = self._format_ass_time(self.end_time)
        text = self._escape_ass_text(self.text)
        return f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}"
    
    def _format_time(self, seconds: float, use_comma: bool = False) -> str:
        """格式化时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        ms = int((secs - int(secs)) * 1000)
        secs = int(secs)
        if use_comma:
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"
    
    def _format_ass_time(self, seconds: float) -> str:
        """ASS时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"
    
    def _escape_ass_text(self, text: str) -> str:
        """转义ASS特殊字符"""
        return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


@dataclass
class SubtitleTrack:
    """字幕轨数据类"""
    subtitles: List[Subtitle] = field(default_factory=list)
    language: str = "unknown"
    format: str = "srt"
    
    def to_string(self, format: str = None) -> str:
        """导出为字符串"""
        fmt = format or self.format
        
        if fmt == "srt":
            return self._to_srt()
        elif fmt == "vtt":
            return self._to_vtt()
        elif fmt == "ass":
            return self._to_ass()
        return ""
    
    def _to_srt(self) -> str:
        """SRT格式"""
        result = ""
        for i, sub in enumerate(self.subtitles, 1):
            result += sub.to_srt(i)
        return result
    
    def _to_vtt(self) -> str:
        """VTT格式"""
        result = "WEBVTT\n\n"
        for sub in self.subtitles:
            result += sub.to_vtt() + "\n"
        return result
    
    def _to_ass(self, styles: Dict = None) -> str:
        """ASS格式"""
        header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,SimHei,24,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        result = header
        for sub in self.subtitles:
            result += sub.to_ass() + "\n"
        return result
    
    def save(self, path: str, format: str = None):
        """保存字幕文件"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        content = self.to_string(format or self.format)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def merge_short(self, max_chars: int = 50):
        """合并短字幕"""
        if len(self.subtitles) <= 1:
            return
            
        merged = []
        current = self.subtitles[0]
        
        for sub in self.subtitles[1:]:
            if len(current.text) + len(sub.text) <= max_chars:
                current.text = f"{current.text} {sub.text}"
                current.end_time = sub.end_time
            else:
                merged.append(current)
                current = sub
                
        merged.append(current)
        self.subtitles = merged
    
    def split_long(self, max_chars: int = 42):
        """拆分长字幕"""
        result = []
        for sub in self.subtitles:
            if len(sub.text) <= max_chars:
                result.append(sub)
            else:
                words = sub.text.split()
                current_text = ""
                current_start = sub.start_time
                
                for word in words:
                    if len(current_text) + len(word) + 1 <= max_chars:
                        current_text = f"{current_text} {word}".strip()
                    else:
                        # 创建当前片段
                        word_duration = sub.end_time - sub.start_time
                        chars_per_second = len(sub.text) / word_duration if word_duration > 0 else 10
                        current_end = current_start + len(current_text) / chars_per_second
                        
                        result.append(Subtitle(
                            index=len(result) + 1,
                            start_time=current_start,
                            end_time=current_end,
                            text=current_text
                        ))
                        
                        current_start = current_end
                        current_text = word
                
                if current_text:
                    result.append(Subtitle(
                        index=len(result) + 1,
                        start_time=current_start,
                        end_time=sub.end_time,
                        text=current_text
                    ))
        
        self.subtitles = result
    
    def adjust_timing(self, offset: float = 0, factor: float = 1.0):
        """调整时间轴"""
        for sub in self.subtitles:
            sub.start_time = sub.start_time * factor + offset
            sub.end_time = sub.end_time * factor + offset


class SubtitleGenerator:
    """字幕生成器"""
    
    def __init__(self, model: str = "medium", device: str = "auto"):
        """初始化
        
        Args:
            model: Whisper模型 (tiny/base/small/medium/large)
            device: 设备 (auto/cuda/cpu)
        """
        self.model_name = model
        self.device = device
        self.model = None
        
    def _load_model(self):
        """加载Whisper模型"""
        import whisper
        if self.model is None:
            self.model = whisper.load_model(self.model_name, device=self.device)
    
    def generate(
        self,
        video_path: str,
        language: Optional[str] = None,
        format: str = "srt"
    ) -> SubtitleTrack:
        """从视频生成字幕
        
        Args:
            video_path: 视频文件路径
            language: 语言 (None=自动检测)
            format: 字幕格式
            
        Returns:
            SubtitleTrack对象
        """
        self._load_model()
        
        # 提取音频
        audio_path = self._extract_audio(video_path)
        
        # 转录
        options = {
            "fp16": False,
            "language": language,
            "best_of": 5,
            "beam_size": 5
        }
        
        result = self.model.transcribe(audio_path, **options)
        
        # 清理临时音频
        if audio_path != video_path:
            os.remove(audio_path)
        
        # 转换为SubtitleTrack
        track = SubtitleTrack(
            language=result.get("language", "unknown"),
            format=format
        )
        
        for i, segment in enumerate(result.get("segments", []), 1):
            track.subtitles.append(Subtitle(
                index=i,
                start_time=segment.get("start", 0),
                end_time=segment.get("end", 0),
                text=segment.get("text", "").strip()
            ))
        
        return track
    
    def _extract_audio(self, video_path: str) -> str:
        """提取音频"""
        audio_path = video_path.replace(
            Path(video_path).suffix,
            ".wav"
        )
        
        if not os.path.exists(audio_path):
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-ac", "1",
                "-ar", "16000",
                "-acodec", "pcm_s16le",
                audio_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        
        return audio_path
    
    def save(
        self,
        track: SubtitleTrack,
        output_path: str,
        format: str = None
    ):
        """保存字幕"""
        track.save(output_path, format)


class SubtitleEditor:
    """字幕编辑器"""
    
    def __init__(self, path: str):
        """加载字幕文件"""
        self.path = path
        self.track = self._load(path)
    
    def _load(self, path: str) -> SubtitleTrack:
        """加载字幕"""
        track = SubtitleTrack()
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if path.endswith('.srt'):
            track = self._parse_srt(content)
        elif path.endswith('.vtt'):
            track = self._parse_vtt(content)
            
        return track
    
    def _parse_srt(self, content: str) -> SubtitleTrack:
        """解析SRT"""
        track = SubtitleTrack(format="srt")
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)'
        import re
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            track.subtitles.append(Subtitle(
                index=int(match[0]),
                start_time=self._parse_time(match[1]),
                end_time=self._parse_time(match[2]),
                text=match[3].strip()
            ))
        
        return track
    
    def _parse_vtt(self, content: str) -> SubtitleTrack:
        """解析VTT"""
        track = SubtitleTrack(format="vtt")
        lines = content.split('\n')
        current = None
        
        for line in lines:
            if '-->' in line:
                parts = line.split('-->')
                current = Subtitle(
                    index=len(track.subtitles) + 1,
                    start_time=self._parse_time(parts[0].strip()),
                    end_time=self._parse_time(parts[1].strip()),
                    text=""
                )
            elif current and line.strip():
                current.text = line.strip()
                track.subtitles.append(current)
        
        return track
    
    def _parse_time(self, time_str: str) -> float:
        """解析时间字符串为秒"""
        if ',' in time_str:
            time_str = time_str.replace(',', '.')
        
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = parts
            return float(h) * 3600 + float(m) * 60 + float(s)
        return 0
    
    def adjust_timing(self, offset: float = 0, factor: float = 1.0):
        """调整时间轴"""
        self.track.adjust_timing(offset, factor)
    
    def merge_lines(self, max_chars: int = 50):
        """合并短行"""
        self.track.merge_short(max_chars)
    
    def split_lines(self, max_chars: int = 42):
        """拆分长行"""
        self.track.split_long(max_chars)
    
    def save(self, output_path: str = None):
        """保存"""
        path = output_path or self.path
        self.track.save(path)


class VideoBurner:
    """视频烧录器"""
    
    def burn_subtitles(
        self,
        video: str,
        subtitles: str,
        output: str,
        style: Dict = None
    ):
        """烧录字幕到视频
        
        Args:
            video: 输入视频路径
            subtitles: 字幕文件路径
            output: 输出视频路径
            style: 样式配置
        """
        font = style.get("font", "SimHei")
        size = style.get("size", 24)
        x = style.get("x", "(w-text_w)/2")
        y = style.get("y", "h-text_h-10")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video,
            "-vf", f"subtitles={subtitles}:force_style='FontName={font},FontSize={size}'",
            "-c:a", "copy",
            output
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
