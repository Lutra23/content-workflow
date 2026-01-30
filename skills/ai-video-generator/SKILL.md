---
name: ai-video-generator
description: Unified AI video generation interface for anime/cartoon production. Supports Runway Gen-3, Pika Labs, Kling AI, and Luma Dream Machine. Provides text-to-video, image-to-video, and video extension capabilities with consistent APIs and motion control presets.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python3"],"env":["RUNWAY_API_KEY","KLING_API_KEY","LUMA_API_KEY"],"optionalEnv":["PIKA_API_KEY"]},"primaryEnv":"RUNWAY_API_KEY"}}
---

# AI Video Generator

Unified AI video generation interface for anime and cartoon production. Supports multiple providers with consistent APIs and motion control presets.

## Installation

```bash
# Clone or navigate to the skill directory
cd skills/ai-video-generator

# Install dependencies
pip install -r requirements.txt

# Configure API keys (choose your providers)
export RUNWAY_API_KEY="your-runway-key"      # For Runway Gen-3
export KLING_API_KEY="your-kling-key"        # For Kling AI
export LUMA_API_KEY="your-luma-key"          # For Luma Dream Machine
export PIKA_API_KEY="your-pika-key"          # Optional: for Pika Labs
```

## Quick Start

### Text to Video

```bash
# Generate anime video from text
python scripts/generate.py text "动画风格，城市夜景，霓虹灯效果" --duration 5 --style anime

# Direct provider selection
python scripts/generate.py text "cute anime cat walking" --provider runway --duration 4
```

### Image to Video

```bash
# Animate a static image
python scripts/generate.py image character_pose.png --motion "walking" --duration 4 --provider pika

# With style control
python scripts/generate.py image scene.png --motion "gentle floating" --style anime --provider luma
```

### Video Extension

```bash
# Extend an existing video
python scripts/generate.py extend scene.mp4 --additional 3 --provider runway
```

### API Usage

```python
from lib.video_generator import AnimeVideoGenerator

generator = AnimeVideoGenerator()

# Text to video
video = await generator.generate_from_text(
    prompt="anime girl walking in cherry blossom garden",
    duration=5,
    style="anime"
)

# Image to video
video = await generator.generate_from_image(
    image="character_pose.png",
    motion_prompt="walking naturally",
    duration=4
)

# Batch generation
results = await generator.batch_generate(
    prompts=["scene1", "scene2", "scene3"],
    duration=5,
    provider="auto"
)
```

## Providers

### Runway Gen-3 (Recommended)

Best quality for anime content.

```bash
export RUNWAY_API_KEY="your-key"

# Usage
python scripts/generate.py text "anime cityscape at night" --provider runway --duration 5
```

**Capabilities:**
- Text to video
- Image to video
- Video extension (up to 10s)
- Motion brush
- Camera controls

### Pika Labs

Fast iteration, good for prototyping.

```bash
export PIKA_API_KEY="your-key"

# Usage
python scripts/generate.py image pose.png --motion "dance" --provider pika --duration 3
```

### Kling AI

Chinese support, good value.

```bash
export KLING_API_KEY="your-key"

# Usage
python scripts/generate.py text "中国古风建筑，樱花盛开" --provider kling --duration 5
```

### Luma Dream Machine

Free tier available, quick generation.

```bash
export LUMA_API_KEY="your-key"

# Usage
python scripts/generate.py text "anime landscape" --provider luma --duration 5
```

## Motion Presets

### Anime Motion Styles

```yaml
# configs/motion_presets.yaml
presets:
  gentle:
    prompt_template: "gentle, smooth motion, {motion}, subtle movement, peaceful atmosphere"
    camera_movement: "static"
    motion_scale: 0.5
    
  dynamic:
    prompt_template: "dynamic action, {motion}, fast paced, energetic, impactful movements"
    camera_movement: "shake"
    motion_scale: 1.2
    
  cinematic:
    prompt_template: "cinematic motion, {motion}, dramatic camera, professional film look"
    camera_movement: "pan_left"
    motion_scale: 0.8
    
  dreamy:
    prompt_template: "dreamy atmosphere, {motion}, floating, ethereal, soft transitions"
    camera_movement: "static"
    motion_scale: 0.3
```

### Camera Movements

| Movement | Description | Use Case |
|----------|-------------|----------|
| static | No camera movement | Close-ups, talking heads |
| pan_left | Camera moves left | Establishing shots |
| pan_right | Camera moves right | Following action |
| tilt_up | Camera looks up | Revealing shots |
| tilt_down | Camera looks down | Focus on subject |
| zoom_in | Camera moves closer | Building tension |
| zoom_out | Camera moves away | Revealing context |
| dolly | Smooth tracking | Dynamic action |
| shake | Camera shake | Impact, explosions |

## Configuration

### Provider Priority

```yaml
# configs/providers.yaml
providers:
  primary: runway
  fallback_order:
    - runway
    - pika
    - kling
    - luma
    
  runway:
    api_url: https://api.runwayml.com/v1
    max_duration: 10
    enabled: true
    
  pika:
    api_url: https://api.pika.art/v1
    max_duration: 4
    enabled: true
    
  kling:
    api_url: https://api.klingai.com/v1
    max_duration: 10
    enabled: true
    
  luma:
    api_url: https://api.lumalabs.ai/v1
    max_duration: 5
    enabled: true
```

### Rate Limits

```yaml
# configs/rate_limits.yaml
providers:
  runway:
    videos_per_minute: 2
    max_concurrent: 1
    
  pika:
    videos_per_minute: 5
    max_concurrent: 2
    
  kling:
    videos_per_minute: 3
    max_concurrent: 1
    
  luma:
    videos_per_minute: 10
    max_concurrent: 3
```

## Advanced Usage

### Consistent Character Video

```python
from lib.video_generator import AnimeVideoGenerator

generator = AnimeVideoGenerator()

# Create character reference
character_ref = generator.create_character_reference(
    image="character.png",
    name="main_character"
)

# Generate video with consistent character
video = generator.generate_with_character(
    character_ref=character_ref,
    prompt="character walking and waving",
    duration=5
)
```

### Storyboard to Video

```bash
# Convert storyboard frames to video
python scripts/storyboard_to_video.py storyboard/ --fps 24 --output animation.mp4

# With audio track
python scripts/storyboard_to_video.py storyboard/ --audio background_music.mp3 --output final.mp4
```

### Batch Scene Generation

```python
# Generate multiple scenes for a story
scenes = [
    {"prompt": "opening scene - school entrance", "duration": 5},
    {"prompt": " classroom introduction", "duration": 5},
    {"prompt": "lunch break scene", "duration": 5},
    {"prompt": "after school activities", "duration": 5}
]

results = await generator.batch_generate_scenes(
    scenes=scenes,
    style="anime",
    provider="runway"
)
```

## Output Formats

| Format | Use Case | Quality |
|--------|----------|---------|
| MP4 (H.264) | General use | High |
| MP4 (H.265) | Web, high efficiency | High |
| WebM | Web streaming | Medium |
| ProRes | Post-production | Lossless |
| GIF | Social media | Low |

## Cost Estimation

| Provider | Cost per Second | Quality |
|----------|-----------------|---------|
| Runway Gen-3 | $0.50-1.00 | Highest |
| Pika Labs | Free/$0.02 | High |
| Kling AI | ¥0.2/秒 | High |
| Luma Dream Machine | Free/$0.01 | Medium |

## Troubleshooting

### Common Issues

**Low quality output:**
- Use higher motion_scale values
- Add more detailed prompts
- Try different provider

**Character inconsistency:**
- Use character reference images
- Keep prompts similar across generations
- Use image-to-video instead of text-to-video

**Generation failures:**
- Check API rate limits
- Reduce video length
- Try fallback providers

### Performance Tips

1. Use shorter clips for faster iteration
2. Enable auto-retry for failed generations
3. Use webm for quick previews
4. Batch similar requests together

## Scripts Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/generate.py` | Single video generation | `generate.py text "anime girl" --duration 5` |
| `scripts/batch.py` | Batch processing | `batch.py generate scenes.txt --output ./videos` |
| `scripts/extend.py` | Video extension | `extend.py video.mp4 --additional 5` |
| `scripts/storyboard_to_video.py` | Storyboard conversion | `storyboard_to_video.py frames/` |
| `scripts/enhance.py` | Quality enhancement | `enhance.py video.mp4 --upscale 2x` |

## Integration

### With AI Image Generator

```python
# Generate keyframe first, then animate
from lib.image_generator import AnimeImageGenerator
from lib.video_generator import AnimeVideoGenerator

image_gen = AnimeImageGenerator()
video_gen = AnimeVideoGenerator()

# Generate keyframe
keyframe = await image_gen.generate_character(
    prompt="anime girl, walking pose, front view",
    size=(768, 768)
)

# Animate the keyframe
video = await video_gen.generate_from_image(
    image=keyframe,
    motion_prompt="walking naturally in park",
    duration=5
)
```

### With Video Editor

```bash
# Export for video editing software
python scripts/export.py video.mp4 --format prores --color-space rec709
```

## References

- [Runway ML API](https://docs.runwayml.com/)
- [Pika Labs API](https://docs.pika.art/)
- [Kling AI Documentation](https://docs.klingai.com/)
- [Luma Dream Machine](https://dreammachine.lumalabs.ai/)

## Limitations

### Current Limitations
- No real-time generation preview
- Limited camera control options
- No inpainting within videos
- Maximum video length varies by provider

### Planned Features
- [ ] Real-time preview generation
- [ ] Advanced camera controls
- [ ] Video inpainting
- [ ] Voice sync integration
- [ ] Multi-shot sequences
