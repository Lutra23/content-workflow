#!/usr/bin/env python3
"""
字幕同步脚本

调整字幕时间轴、合并/拆分字幕行。
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="字幕同步工具")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入字幕文件路径"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出字幕文件路径"
    )
    parser.add_argument(
        "--offset", "-t",
        type=float,
        default=0,
        help="时间偏移 (秒, 正数=延后, 负数=提前)"
    )
    parser.add_argument(
        "--factor", "-s",
        type=float,
        default=1.0,
        help="时间缩放因子 (1.0=不变, 0.5=加速, 2.0=减速)"
    )
    parser.add_argument(
        "--merge", "-m",
        type=int,
        default=None,
        help="合并短行 (最大字符数, 0=禁用)"
    )
    parser.add_argument(
        "--split", "-p",
        type=int,
        default=None,
        help="拆分长行 (最大字符数, 0=禁用)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        return 1
    
    print(f"输入字幕: {args.input}")
    print(f"输出字幕: {args.output}")
    print(f"时间偏移: {args.offset}秒")
    print(f"缩放因子: {args.factor}")
    print(f"合并短行: {args.merge if args.merge else '禁用'}")
    print(f"拆分长行: {args.split if args.split else '禁用'}")
    print("-" * 40)
    
    # 导入并运行编辑器
    from lib.subtitle import SubtitleEditor
    
    editor = SubtitleEditor(args.input)
    
    # 调整时间轴
    if args.offset != 0 or args.factor != 1.0:
        editor.adjust_timing(offset=args.offset, factor=args.factor)
        print(f"时间轴已调整: offset={args.offset}, factor={args.factor}")
    
    # 合并短行
    if args.merge is not None and args.merge > 0:
        editor.merge_lines(max_chars=args.merge)
        print(f"短行已合并: max_chars={args.merge}")
    
    # 拆分长行
    if args.split is not None and args.split > 0:
        editor.split_lines(max_chars=args.split)
        print(f"长行已拆分: max_chars={args.split}")
    
    # 保存结果
    editor.save(args.output)
    
    print(f"字幕已保存到: {args.output}")
    print(f"共 {len(editor.track.subtitles)} 条字幕")
    
    return 0


if __name__ == "__main__":
    exit(main())
