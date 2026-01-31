# Color Grader

Video color correction and anime-style presets.

## Installation

```bash
cd skills/ai-color-grader
pip install -r requirements.txt
sudo apt install ffmpeg
```

## Quick Start

### Apply Preset Style

```bash
# Anime style (punchy colors)
python scripts/generate.py apply video.mp4 graded.mp4 --style anime

# Cinematic (teal/orange)
python scripts/generate.py apply video.mp4 graded.mp4 --style cinematic

# Vintage film
python scripts/generate.py apply video.mp4 graded.mp4 --style vintage

# Black & white
python scripts/generate.py apply video.mp4 graded.mp4 --style bw

# Cool tones
python scripts/generate.py apply video.mp4 graded.mp4 --style cool
```

### Custom Settings

```bash
# Adjust brightness/contrast/saturation
python scripts/generate.py custom video.mp4 graded.mp4 \
    --brightness 0.1 --contrast 0.2 --saturation 1.3
```

### Auto Correction

```bash
# Auto color correction
python scripts/generate.py auto video.mp4 graded.mp4
```

### Cleanup

```bash
# Denoise
python scripts/generate.py denoise video.mp4 clean.mp4 --strength 5

# Sharpen
python scripts/generate.py sharpen video.mp4 sharp.mp4 --strength 1.5
```

## Available Styles

| Style | Description |
|-------|-------------|
| anime | Punchy anime colors |
| cinematic | Teal/orange cinematic look |
| vintage | Vintage film look |
| bw | Black and white |
| sepia | Sepia tone |
| cool | Cool blue tones |
| warm | Warm orange tones |
| high_contrast | Punchy contrast |
| dreamy | Soft, dreamy look |

## Integration

Use after `ai-anime-pipeline`:

```bash
# Color grade final output
python scripts/generate.py apply output/final.mp4 output/graded.mp4 --style anime

# Denoise low-quality clips
python scripts/generate.py denoise clips/scene_01.mp4 clips/clean_01.mp4
```

## Tips

1. **Preview First**: Test with short clip before full grade
2. **Moderation**: Anime style at 1.0 is strong; try 0.7 for subtle
3. **Upscaling Fix**: Use denoise before upscaling
