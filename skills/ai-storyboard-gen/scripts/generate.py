#!/usr/bin/env python3
"""
分镜生成脚本

从剧本生成专业的动漫分镜。
"""

import argparse
import os
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="AI分镜生成")
    parser.add_argument(
        "--script", "-s",
        required=True,
        help="剧本路径或剧本文本内容"
    )
    parser.add_argument(
        "--output", "-o",
        default="output",
        help="输出目录"
    )
    parser.add_argument(
        "--style", "-t",
        default="anime",
        choices=["anime", "realistic", "cartoon"],
        help="风格"
    )
    parser.add_argument(
        "--format", "-f",
        default="pdf",
        choices=["pdf", "png", "json"],
        help="输出格式"
    )
    parser.add_argument(
        "--num-panels", "-n",
        type=int,
        default=None,
        help="分镜格数量 (默认: 自动)"
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["16:9", "4:3", "1:1", "9:16"],
        help="宽高比"
    )
    parser.add_argument(
        "--resolution",
        default="1920x1080",
        help="分辨率 (WxH)"
    )
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 读取剧本
    if os.path.exists(args.script):
        with open(args.script, 'r', encoding='utf-8') as f:
            script_content = f.read()
        print(f"从文件加载剧本: {args.script}")
    else:
        script_content = args.script
        print("使用命令行传入的剧本")
    
    # 导入并运行生成器
    from lib.storyboard import StoryboardGenerator
    
    generator = StoryboardGenerator()
    
    # 生成分镜
    resolution = tuple(map(int, args.resolution.split('x')))
    storyboard = generator.generate(
        script=script_content,
        num_panels=args.num_panels,
        style=args.style,
        aspect_ratio=args.aspect_ratio
    )
    storyboard.resolution = resolution
    
    # 导出结果
    if args.format == "json":
        output_file = os.path.join(args.output, "storyboard.json")
        storyboard.export(output_file, format="json")
        print(f"分镜已导出到: {output_file}")
    elif args.format == "pdf":
        output_file = os.path.join(args.output, "storyboard.pdf")
        storyboard.export(output_file, format="pdf")
        print(f"分镜已导出到: {output_file}")
    elif args.format == "png":
        output_dir = os.path.join(args.output, "panels")
        storyboard.export_frames(output_dir, format="png")
        print(f"分镜帧已导出到: {output_dir}")
    
    print(f"共生成 {len(storyboard.panels)} 个分镜格")
    
    return 0


if __name__ == "__main__":
    exit(main())
