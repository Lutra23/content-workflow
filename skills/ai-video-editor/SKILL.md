# Video Editor

Simple video editing operations with ffmpeg: concatenate, trim, speed, audio, resize, subtitles.

## Installation

```bash
cd skills/ai-video-editor
pip install -r requirements.txt

# Install ffmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
```

## Quick Start

### Concatenate Videos

```bash
# Simple concat
python scripts/generate.py concat clip1.mp4 clip2.mp4 clip3.mp4 -o combined.mp4
```

### Trim Video

```bash
# Trim by start/end time
python scripts/generate.py trim video.mp4 clip.mp4 --start 10 --end 30

# Trim by duration
python scripts/generate.py trim video.mp4 clip.mp4 --start 5 --duration 10
```

### Change Speed

```bash
# 1.5x speed
python scripts/generate.py speed video.mp4 fast.mp4 --speed 1.5

# 0.5x slow motion
python scripts/generate.py speed video.mp4 slow.mp4 --speed 0.5
```

### Add Audio

```bash
# Replace audio
python scripts/generate.py audio video.mp4 bgm.mp4 output.mp4

# Mix with original
python scripts/generate.py audio video.mp4 bgm.mp4 output.mp4 --mix
```

### Resize

```bash
# Resize to 720x480
python scripts/generate.py resize video.mp4 small.mp4 --width 720 --height 480
```

### Add Subtitles

```bash
python scripts/generate.py subtitle video.mp4 subs.srt output.mp4
```

### Show Info

```bash
python scripts/generate.py info video.mp4
```

## Features

| Command | Description |
|---------|-------------|
| `concat` | Join multiple videos |
| `trim` | Cut video segment |
| `speed` | Change playback speed |
| `audio` | Add/replace audio track |
| `resize` | Change resolution |
| `subtitle` | Burn in subtitles |
| `info` | Show video metadata |

## Integration

Use with `ai-anime-pipeline`:

```bash
# Combine scene clips
python scripts/generate.py concat scenes/*.mp4 -o episode.mp4

# Add background music
python scripts/generate.py audio episode.mp4 bgm.mp4 final.mp4
```

## Tips

1. **Order Matters**: concat uses file order
2. **Lossless Trim**: Use `-c copy` for fast trimming
3. **Audio Sync**: When mixing, original audio volume may need adjustment
