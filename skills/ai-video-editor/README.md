# Video Editor

Simple video editing with ffmpeg.

## Usage

```bash
# Concatenate
python scripts/generate.py concat a.mp4 b.mp4 -o combined.mp4

# Trim
python scripts/generate.py trim video.mp4 clip.mp4 --start 10 --end 30

# Change speed
python scripts/generate.py speed video.mp4 fast.mp4 --speed 1.5

# Add audio
python scripts/generate.py audio video.mp4 bgm.mp4 out.mp4
```

See [SKILL.md](SKILL.md) for full documentation.
