---
name: ai-voice-generator
description: Unified AI voice/TTS generation interface for anime/cartoon production. Supports ElevenLabs, Azure TTS, OpenAI TTS, Google TTS, and Coqui TTS. Provides voice cloning, emotion control, multi-language support, and batch processing for character dialogues.
metadata: {"clawdbot":{"emoji":"🎤","requires":{"bins":["python3"],"env":["ELEVENLABS_API_KEY","AZURE_SPEECH_KEY","OPENAI_API_KEY"],"optionalEnv":["GOOGLE_TTS_KEY","COQUI_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# AI Voice Generator

Unified AI voice/TTS generation interface for anime and cartoon production. Supports multiple providers with consistent APIs and anime-optimized voice presets.

## Installation

```bash
# Clone or navigate to the skill directory
cd skills/ai-voice-generator

# Install dependencies
pip install -r requirements.txt

# Configure API keys (choose your providers)
export ELEVENLABS_API_KEY="your-elevenlabs-key"     # For high-quality voices
export AZURE_SPEECH_KEY="your-azure-key"           # For multi-language
export OPENAI_API_KEY="your-openai-key"            # For fast generation
export GOOGLE_TTS_KEY="your-google-key"            # Optional
export COQUI_API_KEY="your-coqui-key"              # Optional: for local TTS
```

## Quick Start

### Generate Voice

```bash
# Generate character dialogue (auto-selects best provider)
python scripts/generate.py dialogue "你好，我叫小明，很高兴认识你" --voice "young female" --emotion happy --style anime

# Generate with specific provider
python scripts/generate.py dialogue "Hello, my name is Alice" --provider elevenlabs --voice "young_female_1"

# Direct text-to-speech
python scripts/generate.py tts "这是一段测试语音" --provider azure --language zh-CN
```

### Voice Cloning

```bash
# Clone a voice from audio sample
python scripts/clone.py reference.wav --name "main_character"

# List available voices
python scripts/list_voices.py

# Generate with cloned voice
python scripts/generate.py dialogue "新的对话内容" --voice "main_character" --emotion neutral
```

### Batch Processing

```bash
# Generate from dialogue script
python scripts/batch.py generate dialogue.txt --voice "young female" --output ./audio/

# Generate multiple languages
python scripts/batch.py translate dialogue_en.txt --languages zh,ja,ko --provider azure
```

### API Usage

```python
from lib.voice_generator import AnimeVoiceGenerator

generator = AnimeVoiceGenerator()

# Generate character dialogue
audio = await generator.generate_dialogue(
    text="你好，我叫小明！",
    voice="young_female",
    emotion="happy",
    provider="elevenlabs"
)

# Clone a voice
voice_id = await generator.clone_voice(
    audio_sample="reference.wav",
    name="protagonist_voice"
)

# Generate with cloned voice
audio = await generator.generate_dialogue(
    text="今天天气真好呢！",
    voice_id=voice_id,
    emotion="cheerful"
)

# Batch generation
results = await generator.batch_generate(
    script="dialogue.txt",
    voice="young_male",
    emotions={"happy", "sad", "angry"}
)
```

## Providers

### ElevenLabs (Recommended for Anime)

Highest quality voices with emotion expression.

```bash
export ELEVENLABS_API_KEY="your-key"

# Usage
python scripts/generate.py dialogue "Hello!" --provider elevenlabs --voice "young_female_1"
```

**Features:**
- 29+ languages
- Emotion control
- Voice cloning
- Stability adjustment
- Similarity boost

### Azure TTS (Recommended for Multi-language)

Best for multi-language projects.

```bash
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"

# Usage
python scripts/generate.py tts "你好世界" --provider azure --language zh-CN --voice "zh-CN-XiaoxiaoNeural"
```

**Features:**
- 400+ voices
- Neural voices
- SSML support
- Prosody control
- Multiple styles

### OpenAI TTS

Fast generation, good quality.

```bash
export OPENAI_API_KEY="your-key"

# Usage
python scripts/generate.py tts "Hello world" --provider openai --voice "alloy"
```

**Voices:**
- alloy, echo, fable, onyx, nova, shimmer

### Google TTS

Large language coverage.

```bash
export GOOGLE_TTS_KEY="your-key"

# Usage
python scripts/generate.py tts "こんにちは" --provider google --language ja --voice "ja-JP-Wavenet-A"
```

### Coqui TTS (Local)

Open source, runs locally.

```bash
# No API key needed
python scripts/generate.py tts "Test" --provider coqui --model "tacotron2"
```

## Voice Presets

### Anime Character Voices

```yaml
# configs/voice_presets.yaml
presets:
  young_female:
    voices:
      elevenlabs: "young_female_1"
      azure: "zh-CN-XiaoxiaoNeural"
      openai: "nova"
      google: "ja-JP-Wavenet-A"
    emotion_range: ["happy", "sad", "angry", "surprised", "neutral"]
    pitch: "+2st"
    speed: 1.0
    
  young_male:
    voices:
      elevenlabs: "young_male_1"
      azure: "zh-CN-YunxiNeural"
      openai: "alloy"
      google: "ja-JP-Wavenet-B"
    emotion_range: ["happy", "serious", "sad", "angry", "neutral"]
    pitch: "-1st"
    speed: 1.0
    
  older_female:
    voices:
      elevenlabs: "older_female_1"
      azure: "zh-CN-XiaoyouNeural"
      openai: "shimmer"
    emotion_range: ["gentle", "strict", "kind", "neutral"]
    pitch: "-1st"
    speed: 0.95
    
  robot:
    voices:
      elevenlabs: "robot_voice"
      azure: "zh-CN-XiaoshuangNeural"
    emotion_range: ["neutral", "serious"]
    pitch: "+3st"
    speed: 1.1
```

### Emotion Presets

```yaml
# configs/emotions.yaml
emotions:
  happy:
    stability: 0.5
    similarity: 0.75
    style: 0.5
    description: "Cheerful, upbeat tone"
    
  sad:
    stability: 0.7
    similarity: 0.8
    style: 0.2
    description: "Melancholic, gentle tone"
    
  angry:
    stability: 0.3
    similarity: 0.7
    style: 0.8
    description: "Intense, forceful tone"
    
  surprised:
    stability: 0.4
    similarity: 0.7
    style: 0.6
    description: "Excited, shocked tone"
    
  neutral:
    stability: 0.7
    similarity: 0.8
    style: 0.0
    description: "Calm, natural tone"
```

## Configuration

### Provider Priority

```yaml
# configs/providers.yaml
providers:
  primary: elevenlabs
  fallback_order:
    - elevenlabs
    - azure
    - openai
    - google
    - coqui
    
  elevenlabs:
    api_url: https://api.elevenlabs.io/v1
    enabled: true
    voices_per_minute: 100
    
  azure:
    api_url: https://eastus.tts.speech.microsoft.com
    enabled: true
    voices_per_minute: 200
    
  openai:
    api_url: https://api.openai.com/v1
    enabled: true
    voices_per_minute: 50
    
  google:
    api_url: https://texttospeech.googleapis.com/v1
    enabled: true
    voices_per_minute: 300
    
  coqui:
    api_url: http://localhost:5002
    enabled: true
    voices_per_minute: 1000
```

### Audio Settings

```yaml
# configs/audio_settings.yaml
output:
  format: mp3        # mp3, wav, ogg
  sample_rate: 44100 # 16000, 22050, 44100, 48000
  bitrate: 192k      # 128k, 192k, 256k, 320k
  channels: 1        # 1 (mono), 2 (stereo)
  
normalization:
  target_lufs: -16
  max_peak_dbfs: -3
```

## Advanced Usage

### SSML Generation

```python
from lib.voice_generator import AnimeVoiceGenerator

generator = AnimeVoiceGenerator()

# Generate with SSML for advanced control
audio = await generator.generate_ssml("""
<speak>
  <prosody rate="fast" pitch="+2st">
    大家好，我是小明！
  </prosody>
  <break time="500ms"/>
  <amazon:effect name="whispered">
    这是一个秘密...
  </amazon:effect>
</speak>
""")
```

### Character Voice Profile

```python
# Create and use character voice profiles
profile = generator.create_voice_profile(
    name="protagonist",
    base_voice="young_female",
    pitch_offset=1.5,
    speed=0.95,
    custom_replacements={
        "小明": {"pronunciation": "xiǎo míng", "emphasis": True}
    }
)

# Generate with profile
audio = await generator.generate_with_profile(
    text="大家好！",
    profile=profile
)
```

### Audio Post-processing

```python
# Apply effects to generated audio
from lib.voice_generator import AudioProcessor

processor = AudioProcessor()

# Add reverb
processed = processor.add_reverb(
    audio,
    room_size=0.5,
    wetness=0.3
)

# Normalize audio
normalized = processor.normalize(audio, target_lufs=-16)

# Apply fade in/out
faded = processor.apply_fade(audio, in_ms=500, out_ms=1000)
```

## Batch Processing

### Dialogue Script Format

```text
# dialogue.txt
Scene 1: 学校门口
[happy] 小明: 早上好！今天天气真好啊！
[neutral] 小红: 是啊，阳光明媚呢。
[surprised] 小明: 哇，你看那只小猫！
[cute] 小猫: 喵～

Scene 2: 教室
[serious] 老师: 同学们，上课了！
```

### Generate Batch

```bash
# Generate all dialogue
python scripts/batch.py generate dialogue.txt --output ./audio/ --format mp3

# Generate with specific voice
python scripts/batch.py generate dialogue.txt --voice "young_female" --emotion auto

# Generate with timestamps
python scripts/batch.py generate dialogue.txt --timestamps --output dialogue.srt
```

## Output Formats

| Format | Use Case | Quality |
|--------|----------|---------|
| MP3 | General use | High |
| WAV | Further editing | Lossless |
| OGG | Web streaming | High |
| FLAC | Archive | Lossless |

## Cost Estimation

| Provider | Cost per 1000 chars | Quality |
|----------|---------------------|---------|
| ElevenLabs | $0.30-1.00 | Highest |
| Azure TTS | ¥0.4/万字符 | High |
| OpenAI TTS | $0.015-0.030/min | High |
| Google TTS | $0.004/万字符 | Medium |
| Coqui TTS | Free | Medium |

## Troubleshooting

### Common Issues

**Robotic voice:**
- Increase stability parameter
- Use emotion presets
- Try different voice

**Incorrect pronunciation:**
- Use SSML for phoneme control
- Add custom pronunciation dictionary
- Try voice cloning

**Emotion not matching:**
- Use explicit emotion tags
- Adjust style parameter
- Try different voice

### Performance Tips

1. Cache generated audio files
2. Use voice cloning for consistent characters
3. Batch similar lines together
4. Use Azure for long text (>5000 chars)

## Scripts Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/generate.py` | Single audio generation | `generate.py tts "Hello"` |
| `scripts/clone.py` | Voice cloning | `clone.py sample.wav --name voice1` |
| `scripts/list_voices.py` | List available voices | `list_voices.py` |
| `scripts/batch.py` | Batch processing | `batch.py generate script.txt` |
| `scripts/post_process.py` | Audio effects | `post_process.py audio.mp3 --reverb` |

## Integration

### With Video Pipeline

```python
# Generate voice and sync with video
from lib.voice_generator import AnimeVoiceGenerator
from lib.video_generator import AnimeVideoGenerator

voice_gen = AnimeVoiceGenerator()
video_gen = AnimeVideoGenerator()

# Generate voice first
voice = await voice_gen.generate_dialogue(
    text="你好！我是小明。",
    voice="young_female",
    emotion="happy"
)

# Generate video
video = await video_gen.generate_from_text(
    prompt="anime girl saying hello",
    duration=voice.duration
)

# Sync in post-processing
# (Use video editor for precise lip-sync)
```

### With Subtitle Generator

```bash
# Generate audio and subtitles together
python scripts/generate.py with_subs dialogue.txt --output ./project/
```

## References

- [ElevenLabs API](https://docs.elevenlabs.io/)
- [Azure TTS](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)
- [Google TTS](https://cloud.google.com/text-to-speech/docs)

## Limitations

### Current Limitations
- No real-time streaming synthesis
- Limited voice cloning quality
- No lip-sync generation
- SSML support varies by provider

### Planned Features
- [ ] Real-time streaming
- [ ] Improved voice cloning
- [ ] Lip-sync generation
- [ ] Voice conversion
- [ ] Multi-speaker support
