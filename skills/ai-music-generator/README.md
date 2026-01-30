# AI Music Generator

AI-powered music and sound generation for anime productions.

## Quick Start

```bash
cd skills/ai-music-generator
pip install -r requirements.txt

# Configure API key
export MUBERT_API_KEY="your-key"

# Generate background music
python scripts/generate.py bgm "anime school, gentle, warm" --duration 120

# Generate character theme
python scripts/generate.py theme "hero theme, epic, orchestral"

# Generate ambient sound
python scripts/generate.py ambient "forest, birds, wind" --duration 60
```

## Python API

```python
from lib.music_generator import AnimeMusicGenerator

generator = AnimeMusicGenerator()

# Generate BGM
bgm = generator.generate_bgm(
    prompt="anime opening, upbeat",
    style="upbeat",
    duration=180,
    bpm=128
)

# Generate theme
theme = generator.generate_theme(
    prompt="main character theme",
    character="hero"
)

# Generate for scene
scene_audio = generator.generate_for_scene(
    scene_description="epic battle",
    scene_type="fight"
)
```

See [SKILL.md](SKILL.md) for full documentation.
