# Color Grader

Video color correction.

## Usage

```bash
# Apply style
python scripts/generate.py apply video.mp4 graded.mp4 --style anime

# Custom
python scripts/generate.py custom video.mp4 graded.mp4 --brightness 0.1

# Auto
python scripts/generate.py auto video.mp4 graded.mp4

# Denoise
python scripts/generate.py denoise video.mp4 clean.mp4
```

See [SKILL.md](SKILL.md) for full documentation.
