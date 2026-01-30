#!/usr/bin/env python3
"""
创建角色参考脚本

从参考图像创建角色一致性配置文件。
"""

import argparse
import os
import yaml
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="创建角色参考")
    parser.add_argument(
        "--reference", "-r",
        required=True,
        help="参考图像路径或包含图像的文件夹"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出配置文件路径"
    )
    parser.add_argument(
        "--num-images", "-n",
        type=int,
        default=5,
        help="生成参考图数量"
    )
    parser.add_argument(
        "--style", "-s",
        default="anime",
        choices=["anime", "realistic", "cartoon"],
        help="风格预设"
    )
    parser.add_argument(
        "--resolution",
        default="512x512",
        help="输出分辨率 (WxH)"
    )
    
    args = parser.parse_args()
    
    # 收集参考图像
    reference_images = []
    if os.path.isdir(args.reference):
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
            reference_images.extend(Path(args.reference).glob(ext))
    else:
        reference_images = [args.reference]
    
    if not reference_images:
        print(f"错误: 未找到参考图像")
        return 1
    
    reference_images = [str(p) for p in reference_images[:10]]  # 最多10张
    
    # 创建配置
    resolution = tuple(map(int, args.resolution.split("x")))
    
    config = {
        "name": "character",
        "reference_images": reference_images,
        "style": args.style,
        "resolution": {
            "width": resolution[0],
            "height": resolution[1]
        },
        "num_samples": args.num_images,
        "created_at": str(Path(__file__).stat().st_mtime) if os.path.exists(args.reference) else None
    }
    
    # 保存配置
    with open(args.output, 'w') as f:
        yaml.safe_dump(config, f)
    
    print(f"角色参考已保存到: {args.output}")
    print(f"参考图像数量: {len(reference_images)}")
    
    return 0


if __name__ == "__main__":
    exit(main())
