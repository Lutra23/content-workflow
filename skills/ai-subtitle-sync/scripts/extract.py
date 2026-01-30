#!/usr/bin/env python3
"""
从视频提取字幕脚本

使用Whisper进行语音识别生成字幕。
"""

import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="从视频提取字幕")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入视频路径"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出字幕路径"
    )
    parser.add_argument(
        "--model", "-m",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper模型"
    )
    parser.add_argument(
        "--language", "-l",
        default=None,
        choices=["zh", "en", "ja", "ko", "zh-CN", "zh-TW"],
        help="语言 (默认: 自动检测)"
    )
    parser.add_argument(
        "--format", "-f",
        default="srt",
        choices=["srt", "vtt", "ass"],
        help="字幕格式"
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="CPU线程数"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        return 1
    
    print(f"输入视频: {args.input}")
    print(f"输出字幕: {args.output}")
    print(f"使用模型: {args.model}")
    print(f"语言: {args.language or '自动检测'}")
    print(f"格式: {args.format}")
    print("-" * 40)
    
    # 导入并运行生成器
    from lib.subtitle import SubtitleGenerator
    
    generator = SubtitleGenerator(model=args.model)
    
    try:
        # 生成字幕
        track = generator.generate(
            video_path=args.input,
            language=args.language,
            format=args.format
        )
        
        # 保存字幕
        generator.save(track, args.output, args.format)
        
        print(f"成功生成 {len(track.subtitles)} 条字幕")
        print(f"字幕已保存到: {args.output}")
        print(f"检测语言: {track.language}")
        
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
