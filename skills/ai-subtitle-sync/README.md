# AI Subtitle Sync

AI字幕同步工具，使用Whisper进行语音识别。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 从视频提取字幕
python scripts/extract.py \
    --input "video.mp4" \
    --output "subtitles.srt" \
    --model medium \
    --language zh
```

## 主要功能

- 语音识别 (ASR) - 使用 Whisper
- 字幕生成 (SRT/VTT)
- 时间轴对齐
- 多语言字幕支持
- 视频内嵌字幕

## 文档

见 [SKILL.md](SKILL.md)
