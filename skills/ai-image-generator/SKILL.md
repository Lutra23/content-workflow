---
name: ai-image-generator
description: Unified AI image generation interface for anime/cartoon production. Supports Midjourney, Stable Diffusion, DALL-E, Flux, and Kling AI. Provides consistent prompt formatting, multi-provider fallback, batch processing, and style presets optimized for anime content creation.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python3"],"env":["OPENAI_API_KEY","HF_TOKEN","REPLICATE_API_TOKEN"],"optionalEnv":["MIDJOURNEY_DISCORD_TOKEN"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# AI Image Generator

Unified AI image generation interface for anime and cartoon production. Supports multiple providers with consistent APIs and anime-optimized presets.

## Installation

```bash
# Clone or navigate to the skill directory
cd skills/ai-image-generator

# Install dependencies
pip install -r requirements.txt

# Configure API keys (choose your providers)
export OPENAI_API_KEY="your-openai-key"      # For DALL-E
export HF_TOKEN="your-huggingface-token"     # For Stable Diffusion
export REPLICATE_API_TOKEN="your-replicate"  # For Flux
export MIDJOURNEY_DISCORD_TOKEN="your-token" # Optional: for Midjourney
```

## Quick Start

### Basic Image Generation

```bash
# Generate anime character (auto-selects best provider)
python scripts/generate.py character "少女，蓝色长发，粉色眼睛，校园制服" --style anime

# Generate background scene
python scripts/generate.py background "樱花盛开的校园，春天，傍晚" --size 1920x1080

# Direct provider selection
python scripts/generate.py character "cute anime girl" --provider stable-diffusion --style anime
```

### Batch Processing

```bash
# Generate from prompt file
python scripts/batch.py generate prompts.txt --output ./output --provider stable-diffusion

# Generate from image list
python scripts/batch.py from-images images/ --prompt "add effects" --style anime
```

### API Usage

```python
from lib.image_generator import AnimeImageGenerator

generator = AnimeImageGenerator()

# Generate character
character = generator.generate_character(
    prompt="cute anime girl with blue hair",
    style="anime",
    size=(1024, 1024)
)

# Generate background
background = generator.generate_background(
    scene_description="cherry blossom campus in spring",
    style="anime",
    perspective="perspective"
)

# Batch generation
results = generator.batch_generate(
    prompts=["prompt1", "prompt2", "prompt3"],
    style="anime",
    provider="auto"
)
```

## Providers

### Stable Diffusion (Recommended for Anime)

Best for high-volume, customizable anime generation.

```bash
# Local setup (requires GPU)
export SD_API_URL="http://localhost:7860"
export HF_TOKEN="your-huggingface-token"

# Usage
python scripts/generate.py character "anime girl" --provider stable-diffusion
```

**Models supported:**
- anime-full-res
- anything-v5
- Counterfeit
- RevAnimated

### DALL-E 3

Fast, high-quality, good prompt understanding.

```bash
export OPENAI_API_KEY="your-key"

# Usage
python scripts/generate.py character "anime girl with blue eyes" --provider dall-e
```

### Flux

High-quality, excellent for commercial anime.

```bash
export REPLICATE_API_TOKEN="your-key"

# Usage
python scripts/generate.py character "anime style portrait" --provider flux
```

### Midjourney (Discord)

Best artistic quality, requires Discord bot setup.

```bash
export MIDJOURNEY_DISCORD_TOKEN="your-bot-token"

# Usage
python scripts/generate.py character "anime style girl" --provider midjourney
```

### Kling AI

Good for combined image+video generation.

```bash
export KLING_API_KEY="your-key"

# Usage
python scripts/generate.py background "anime landscape" --provider kling
```

## Style Presets

### Anime Styles

```yaml
# configs/styles/anime.yaml
presets:
  standard_anime:
    prompt_template: "masterpiece, best quality, anime style, {prompt}, detailed illustration, beautiful eyes, vibrant colors"
    negative_prompt: "low quality, worst quality, blurry, bad anatomy, bad hands"
    default_size: [1024, 1024]
    
  soft_anime:
    prompt_template: "soft anime style, {prompt}, pastel colors, gentle lighting, romantic atmosphere"
    negative_prompt: "dark, gritty, realistic"
    default_size: [1024, 1024]
    
  action_anime:
    prompt_template: "dynamic anime action scene, {prompt}, dramatic lighting, fast motion blur, intense atmosphere"
    negative_prompt: "static, calm, peaceful"
    default_size: [1280, 720]
```

### Character Presets

```yaml
# configs/styles/character.yaml
presets:
  anime_girl:
    hair_colors: ["blue", "pink", "silver", "purple"]
    eye_colors: ["pink", "blue", "green", "red"]
    school_uniform: true
    
  anime_boy:
    hair_colors: ["black", "brown", "blonde", "silver"]
    eye_colors: ["brown", "blue", "green"]
    school_uniform: true
```

## Configuration

### Provider Priority

```yaml
# configs/providers.yaml
providers:
  primary: stable-diffusion
  fallback_order:
    - stable-diffusion
    - flux
    - dall-e
    - midjourney
    - kling
  
  stable-diffusion:
    api_url: http://localhost:7860
    model: anime-full-res
    quality: high
    
  flux:
    model: flux-anime
    guidance: 7.5
```

### Rate Limiting

```yaml
# configs/rate_limits.yaml
providers:
  openai:
    requests_per_minute: 50
    images_per_request: 1
    
  replicate:
    requests_per_minute: 30
    images_per_request: 1
    
  local_sd:
    requests_per_minute: 100
    images_per_request: 4
```

## Advanced Usage

### Consistent Character Generation

```python
from lib.image_generator import AnimeImageGenerator

generator = AnimeImageGenerator()

# Create character reference
character_ref = generator.create_character_reference(
    prompt="anime girl, long blue hair, pink eyes, school uniform",
    seed=42
)

# Generate variations with same character
poses = ["walking", "running", "sitting", "standing"]
for pose in poses:
    generator.generate_character_variant(
        reference=character_ref,
        pose=pose,
        output=f"character_{pose}.png"
    )
```

### Style Transfer

```python
# Apply anime style to any image
result = generator.apply_anime_style(
    input_image="real_photo.jpg",
    style_strength=0.7,
    output="anime_version.png"
)
```

### Quality Optimization

```python
# Optimize for different use cases
generator.set_quality_mode("high")  # Best for final output
generator.set_quality_mode("fast")  # Quick previews
generator.set_quality_mode("draft") # Low cost testing
```

## Workflow Integration

### With Storyboarding

```bash
# Generate storyboard frames from script
python scripts/storyboard.py generate script.txt --style anime --output frames/
```

### With Video Pipeline

```bash
# Generate keyframes for video
python scripts/video_pipeline.py generate-keyframes video_script.yaml --output keyframes/
```

## Output Formats

| Format | Use Case | Quality |
|--------|----------|---------|
| PNG | Final output, transparency | Lossless |
| JPG | Web, sharing | High |
| WEBP | Web optimization | High |
| PSD | Further editing | Layered |

## Cost Estimation

| Provider | Cost per Image | Quality |
|----------|---------------|---------|
| Stable Diffusion (local) | $0.00 | High |
| DALL-E 3 | $0.04-0.12 | Very High |
| Flux | $0.05-0.10 | Very High |
| Midjourney | $0.03-0.08 | Highest |
| Kling AI | $0.02-0.05 | High |

## Troubleshooting

### Common Issues

**Low quality output:**
- Increase quality settings
- Use more detailed prompts
- Try different provider

**Character inconsistency:**
- Use reference image mode
- Lower guidance scale
- Try InstantID for identity preservation

**Rate limit errors:**
- Enable fallback providers
- Reduce batch size
- Add delays between requests

### Performance Tips

1. Use local SD for high-volume generation
2. Enable caching for similar prompts
3. Use seed values for reproducibility
4. Batch similar requests together

## Scripts Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/generate.py` | Single image generation | `generate.py character "anime girl"` |
| `scripts/batch.py` | Batch processing | `batch.py generate prompts.txt` |
| `scripts/optimize.py` | Quality optimization | `optimize.py input.png --quality high` |
| `scripts/storyboard.py` | Storyboard generation | `storyboard.py script.txt` |
| `scripts/video_pipeline.py` | Keyframe generation | `video_pipeline.py script.yaml` |

## References

- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [OpenAI DALL-E API](https://platform.openai.com/docs/guides/images)
- [Replicate Flux](https://replicate.com/flux)
- [Midjourney Documentation](https://docs.midjourney.com)

## Limitations

### Current Limitations
- No real-time generation monitoring
- Limited controlNet integration (in development)
- No LoRA training interface (coming soon)

### Planned Features
- [ ] ControlNet support for pose control
- [ ] LoRA training pipeline
- [ ] Inpainting/outpainting
- [ ] Video keyframe interpolation
- [ ] Collaborative generation
