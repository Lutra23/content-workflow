# AI Voice Generator

Unified AI voice/TTS generation interface for anime and cartoon production.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
export ELEVENLABS_API_KEY="your-key"
export AZURE_SPEECH_KEY="your-azure-key"

# Generate dialogue
python scripts/generate.py dialogue "你好，我叫小明" --voice "young_female" --emotion happy

# Clone a voice
python scripts/clone.py sample.wav --name "my_voice"
```

## Features

- **Multi-provider support**: ElevenLabs, Azure, OpenAI, Google, Coqui
- **Voice cloning**: Create consistent character voices
- **Emotion control**: Happy, sad, angry, surprised, neutral
- **Multi-language**: 29+ languages supported
- **Batch processing**: Generate entire dialogue scripts
- **Audio effects**: Reverb, normalize, fade

## Documentation

See [SKILL.md](./SKILL.md) for complete documentation.
