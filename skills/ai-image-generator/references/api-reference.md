# Anime Image Generator API Reference

## AnimeImageGenerator Class

Main class for anime image generation across multiple providers.

### Constructor

```python
from lib.image_generator import AnimeImageGenerator

generator = AnimeImageGenerator(config_dir: str = None)
```

**Parameters:**
- `config_dir`: Directory containing `providers.yaml` and `styles/` folder. Defaults to skill's `configs` directory.

### Methods

#### generate_character

Generate an anime character image.

```python
result = generator.generate_character(
    prompt: str,
    style: str = "anime",
    size: Tuple[int, int] = None,
    provider: Union[Provider, str] = Provider.AUTO,
    quality: QualityMode = QualityMode.HIGH,
    seed: int = None,
    output_path: str = None
) -> GenerationResult
```

**Parameters:**
- `prompt`: Character description (e.g., "blue-haired girl with pink eyes")
- `style`: Style preset name from `configs/styles/`
- `size`: Output dimensions (width, height)
- `provider`: AI provider to use
- `quality`: Quality setting (draft/fast/high)
- `seed`: Random seed for reproducibility
- `output_path`: Local path to save image

**Returns:** `GenerationResult` object with `success`, `image_path`, `image_url`, `provider`, `seed`, `metadata`, `error`

#### generate_background

Generate an anime background/scene.

```python
result = generator.generate_background(
    prompt: str,
    style: str = "anime",
    size: Tuple[int, int] = None,
    perspective: str = "normal",
    provider: Union[Provider, str] = Provider.AUTO,
    quality: QualityMode = QualityMode.HIGH,
    output_path: str = None
) -> GenerationResult
```

**Parameters:**
- `prompt`: Scene description
- `style`: Style preset name
- `size`: Output dimensions
- `perspective`: View type (normal/wide/aerial/low/close-up)
- `provider`: AI provider
- `quality`: Quality setting
- `output_path`: Local path to save image

#### batch_generate

Generate multiple images.

```python
results = generator.batch_generate(
    prompts: List[str],
    style: str = "anime",
    image_type: ImageType = ImageType.CHARACTER,
    provider: Union[Provider, str] = Provider.AUTO,
    quality: QualityMode = QualityMode.HIGH,
    output_dir: str = "./output",
    parallel: int = 1
) -> List[GenerationResult]
```

#### create_character_reference

Create reference data for consistent character generation.

```python
reference = generator.create_character_reference(
    prompt: str,
    seed: int = None
) -> Dict[str, Any]
```

**Returns:**
```python
{
    "reference_id": "abc12345",
    "prompt": "anime girl with blue hair",
    "prompt_hash": "a1b2c3d4",
    "seed": 1234567890,
    "created_at": 1706745600.0
}
```

#### generate_character_variant

Generate variation of character from reference.

```python
result = generator.generate_character_variant(
    reference: Dict[str, Any],
    variation: str,
    output_path: str = None,
    style: str = "anime",
    provider: Union[Provider, str] = Provider.AUTO
) -> GenerationResult
```

#### set_quality_mode

Set quality mode for subsequent generations.

```python
generator.set_quality_mode(mode: Union[QualityMode, str])
```

---

## Enums

### Provider

```python
from lib.image_generator import Provider

Provider.STABLE_DIFFUSION  # Local/stable diffusion
Provider.DALL_E           # OpenAI DALL-E
Provider.FLUX             # Replicate Flux
Provider.MIDJOURNEY       # Discord Midjourney
Provider.KLING            # Kling AI
Provider.AUTO             # Auto-select based on fallback order
```

### QualityMode

```python
from lib.image_generator import QualityMode

QualityMode.DRAFT  # Fast, low cost (testing)
QualityMode.FAST   # Balanced speed/quality
QualityMode.HIGH   # Best quality (production)
```

### ImageType

```python
from lib.image_generator import ImageType

ImageType.CHARACTER   # Character images
ImageType.BACKGROUND  # Background/scene images
ImageType.PROP        # Props/objects
ImageType.EFFECT      # Visual effects
ImageType.UI          # UI elements
```

---

## GenerationResult

Response object from generation methods.

```python
@dataclass
class GenerationResult:
    success: bool                    # Whether generation succeeded
    image_path: Optional[str] = None  # Local file path
    image_url: Optional[str] = None   # Remote URL (if applicable)
    provider: Optional[str] = None    # Provider used
    prompt_used: Optional[str] = None # Actual prompt sent to API
    seed: Optional[int] = None        # Generation seed
    metadata: Dict = field(default_factory=dict)  # Additional data
    error: Optional[str] = None       # Error message if failed
```

---

## StylePreset

Configuration for style presets.

```python
@dataclass
class StylePreset:
    name: str                       # Preset name
    prompt_template: str            # Prompt with {prompt} placeholder
    negative_prompt: str = ""       # Negative prompt
    default_size: Tuple[int, int]   # Default dimensions
    guidance_scale: float = 7.5     # CFG scale
    steps: int = 30                 # Inference steps
    model: Optional[str] = None     # Preferred model
```

---

## CLI Usage

### Single Image Generation

```bash
# Character generation
python scripts/generate.py character "少女，蓝色长发，粉色眼睛" --style anime

# Background generation
python scripts/generate.py background "樱花校园，春天" --size 1920x1080

# Direct generation
python scripts/generate.py generate "anime girl" --provider stable-diffusion
```

### Batch Processing

```bash
# From prompt file
python scripts/batch.py generate prompts.txt --output ./output

# Generate variations
python scripts/batch.py variations ref.png "angry,sad,happy"

# Character variants
python scripts/batch.py character-variants "blue hair girl" --poses "standing,sitting"
```

---

## Environment Variables

| Variable | Provider | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | DALL-E | OpenAI API key |
| `HF_TOKEN` | Stable Diffusion (HF) | HuggingFace token |
| `REPLICATE_API_TOKEN` | Flux | Replicate API token |
| `MIDJOURNEY_DISCORD_TOKEN` | Midjourney | Discord bot token |
| `KLING_API_KEY` | Kling | Kling AI API key |
| `SD_API_URL` | Stable Diffusion | Local SD WebUI URL |

---

## Error Handling

```python
from lib.image_generator import AnimeImageGenerator

generator = AnimeImageGenerator()

result = generator.generate_character("anime girl")

if not result.success:
    print(f"Error: {result.error}")
    # Handle specific errors
    if "rate limit" in result.error.lower():
        # Implement backoff
        pass
else:
    print(f"Image saved to: {result.image_path}")
```

---

## Caching

Generated images are cached in `~/.cache/anime-image-generator/`. Cache includes:
- Generated images
- Prompt embeddings (for similar prompt detection)

```python
# Check if prompt is cached
generator.cache_dir  # Cache directory path
```

---

## Provider Configuration

### Stable Diffusion (Local)

```python
# Requires Stable Diffusion WebUI running with --api flag
# URL: http://localhost:7860

# Automatic1111 WebUI
# python webui-user.py --api --listen
```

### DALL-E

```python
# Requires OPENAI_API_KEY
export OPENAI_API_KEY="sk-..."
```

### Flux

```python
# Requires REPLICATE_API_TOKEN
export REPLICATE_API_TOKEN="r8_..."
```

### Midjourney

```python
# Requires Discord bot setup or proxy service
# Direct API access not available
export MIDJOURNEY_DISCORD_TOKEN="..."
```

---

## Thread Safety

`AnimeImageGenerator` is thread-safe for concurrent use within the same process.

```python
import concurrent.futures

generator = AnimeImageGenerator()

def generate(prompt):
    return generator.generate_character(prompt)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(generate, prompts))
```

---

## Best Practices

1. **Use local SD for high-volume**: Set up local Stable Diffusion for cost-effective batch generation
2. **Enable caching**: Reduces redundant API calls
3. **Use quality modes**: Use `draft` for testing, `high` for final output
4. **Seed reproducibility**: Set explicit seeds for consistent results
5. **Fallback providers**: Configure fallback order for reliability
