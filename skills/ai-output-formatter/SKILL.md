# Output Formatter

Multi-format video export and optimization for anime productions.

## Features

- **Platform Presets**: YouTube, Bilibili, Twitter, Instagram, Web, Discord
- **Quality Levels**: Low (480p), Medium (720p), High (1080p), Ultra (4K)
- **Compression**: Smart compression with quality trade-offs
- **GIF Generation**: Create animated GIFs from video
- **Batch Export**: Export multiple files at once

## Installation

```bash
cd skills/ai-output-formatter
pip install -r requirements.txt

# Install ffmpeg (required)
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
```

## Quick Start

### Export for Platform

```bash
# YouTube 1080p
python scripts/generate.py export video.mp4 youtube.mp4 --platform youtube --quality high

# Bilibili
python scripts/generate.py export video.mp4 bilibili.mp4 --platform bilibili --quality high

# Twitter (smaller file)
python scripts/generate.py export video.mp4 twitter.mp4 --platform twitter --quality medium

# Instagram (square)
python scripts/generate.py export video.mp4 instagram.mp4 --platform instagram --quality medium
```

### Compress Video

```bash
# High quality compression
python scripts/generate.py compress large.mp4 small.mp4 --quality high

# Medium compression
python scripts/generate.py compress large.mp4 small.mp4 --quality medium

# Maximum compression
python scripts/generate.py compress large.mp4 small.mp4 --quality low
```

### Generate GIF

```bash
# Simple GIF
python scripts/generate.py gif video.mp4 preview.gif

# Custom width
python scripts/generate.py gif video.mp4 preview.gif --width 320
```

### Show Info

```bash
python scripts/generate.py info video.mp4
```

### Batch Export

```bash
python scripts/generate.py batch ./clips ./export --platform youtube --quality high
```

## Presets

| Platform | Quality | Resolution | Bitrate |
|----------|---------|------------|---------|
| YouTube | High | 1920x1080 | 12M |
| YouTube | Ultra | 3840x2160 | 35M |
| Bilibili | High | 1920x1080 | 10M |
| Twitter | Medium | 1280x720 | 5M |
| Instagram | Medium | 1080x1080 | 6M |
| Web | Medium | 1280x720 | 3M |
| Discord | Low | 854x480 | 2M |

## Integration with Pipeline

Use after `ai-anime-pipeline`:

```bash
# Export pipeline output for YouTube
python scripts/generate.py export output/final.mp4 youtube_upload.mp4 \
    --platform youtube --quality high
```

## Tips

1. **WebM for Web**: Use `--platform web` for browser-optimized videos
2. **Smaller GIFs**: Reduce `--width` for smaller GIF files
3. **Fast Upload**: Use Twitter preset for quick social sharing
4. **Original Quality**: Use YouTube Ultra for max quality
