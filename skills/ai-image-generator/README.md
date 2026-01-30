# AI Image Generator

Unified AI image generation interface for anime and cartoon production.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
export OPENAI_API_KEY="your-openai-key"
export HF_TOKEN="your-huggingface-token"

# Generate anime character
python scripts/generate.py character "anime girl with blue hair" --style anime
```

## Features

- **Multi-provider support**: Stable Diffusion, DALL-E, Flux, Midjourney, Kling
- **Anime-optimized presets**: Pre-configured styles for anime content
- **Batch processing**: Generate multiple images efficiently
- **Character consistency**: Reference-based generation
- **Style transfer**: Apply anime styles to any image

## Documentation

See [SKILL.md](./SKILL.md) for complete documentation.

## Support

- Create issues on GitHub
- Check troubleshooting section in SKILL.md
