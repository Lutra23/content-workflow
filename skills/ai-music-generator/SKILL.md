---
name: ai-music-generator
description: AI-powered music and sound generation for anime productions. Supports Mubert, Google MusicGen, Soundful, and Udio. Generates background music, character themes, fight music, and ambient sounds optimized for anime storytelling.
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["python3"],"env":["MUBERT_API_KEY","REPLICATE_API_TOKEN"]},"primaryEnv":"MUBERT_API_KEY"}}
---

# AI Music Generator

AI-powered music and sound generation for anime productions. Creates background music, character themes, and ambient audio.

## Installation

```bash
cd skills/ai-music-generator
pip install -r requirements.txt

# Configure API keys
export MUBERT_API_KEY="your-mubert-key"     # Primary for music
export REPLICATE_API_TOKEN="your-replicate" # For MusicGen
export SOUNDFUL_API_KEY="your-soundful-key" # For stock music
```

## Quick Start

### Generate Background Music

```bash
# Generate anime BGM
python scripts/generate.py bgm "anime opening, upbeat, energetic" --duration 180 --bpm 128

# Generate calm background music
python scripts/generate.py bgm "peaceful forest, gentle, ambient" --style calm --duration 120

# Generate fight scene music
python scripts/generate.py bgm "action, intense, orchestral" --style action --duration 60
```

### Generate Character Theme

```bash
# Character theme
python scripts/generate.py theme "gentle piano, emotional, main character theme"

# Character theme with lyrics
python scripts/generate.py theme "upbeat pop, main character" --lyrics "夢を追いかけて"
```

### Generate Ambient Sound

```bash
# Ambient soundscape
python scripts/generate.py ambient "school hallway, quiet, morning" --duration 30

# Nature ambient
python scripts/generate.py ambient "forest, birds, gentle wind" --duration 60
```

### Generate Sound Effects

```bash
# Sound effects
python scripts/generate.py sfx "sword swing, anime style" --intensity high

# UI sounds
python scripts/generate.py sfx "notification, cute" --style chibi
```

## API Usage

```python
from lib.music_generator import AnimeMusicGenerator

generator = AnimeMusicGenerator()

# Generate background music
bgm = generator.generate_bgm(
    prompt="anime school life, gentle, warm",
    style="calm",
    duration=120,
    bpm=80
)

# Generate character theme
theme = generator.generate_theme(
    prompt="hero theme, epic, orchestral",
    character=" protagonist",
    duration=60
)

# Generate audio for scene
scene_audio = generator.generate_for_scene(
    scene_description="epic battle scene",
    scene_type="fight",
    duration=90
)
```

## Providers

### Mubert (Recommended)

Best for anime-style music generation.

```bash
export MUBERT_API_KEY="your-key"

# Usage
python scripts/generate.py bgm "anime opening" --provider mubert
```

**Features:**
- High quality music
- Anime-optimized tags
- Long duration support
- Loop capability

### Google MusicGen (Replicate)

Open-source music generation.

```bash
export REPLICATE_API_TOKEN="your-token"

# Usage
python scripts/generate.py bgm "piano solo, emotional" --provider musicgen
```

**Features:**
- Customizable generation
- Local-like control
- Multiple model sizes

### Udio

High quality music with lyrics support.

```bash
# Via API
python scripts/generate.py theme "pop song, anime" --provider udio --lyrics "日本語の歌詞"
```

### Soundful

Royalty-free stock music.

```bash
export SOUNDFUL_API_KEY="your-key"

# Usage
python scripts/generate.py bgm "upbeat, positive" --provider soundful --style corporate
```

## Music Styles

### Anime Background Music

| Style | Description | BPM | Mood |
|-------|-------------|-----|------|
| calm | Peaceful, gentle | 60-80 | Relaxed |
| upbeat | Energetic, happy | 110-130 | Cheerful |
| dramatic | Emotional, tense | 70-90 | Serious |
| action | Intense, fast | 140-160 | Exciting |
| mysterious | Dark, suspenseful | 60-80 | Ominous |
| romantic | Soft, warm | 70-90 | Loving |

### Character Themes

```yaml
# configs/styles/themes.yaml
presets:
  protagonist:
    prompt_template: "heroic theme, {prompt}, orchestral, epic"
    instruments: ["strings", "brass", "percussion"]
    mood: heroic
    
  antagonist:
    prompt_template: "dark theme, {prompt}, minor key, ominous"
    instruments: ["synth", "bass", "drums"]
    mood: dark
    
  love_interest:
    prompt_template: "romantic theme, {prompt}, soft, gentle"
    instruments: ["piano", "strings", "harp"]
    mood: romantic
    
  comic_relief:
    prompt_template: "funny theme, {prompt}, playful, quirky"
    instruments: ["brass", "woodwind", "percussion"]
    mood: comedic
```

### Scene-Specific Music

```yaml
# configs/styles/scenes.yaml
presets:
  school_day:
    prompt_template: "slice of life, {prompt}, cheerful, school setting"
    bpm: 100-120
    
  battle:
    prompt_template: "action music, {prompt}, intense, fast tempo"
    bpm: 150-180
    
  emotional:
    prompt_template: "emotional, {prompt}, piano, strings"
    bpm: 60-80
    
  romance:
    prompt_template: "romantic, {prompt}, soft, warm"
    bpm: 70-90
    
  suspense:
    prompt_template: "suspense, {prompt}, dark, minimal"
    bpm: 50-70
```

## Sound Effects

### Categories

| Category | Tags | Use Case |
|----------|------|----------|
| combat | sword, punch, kick, magic | Fight scenes |
| ambient | wind, birds, water | Background |
| ui | notification, select, cancel | Menus |
| voice | breathing, sigh, laugh | Character |
| environmental | rain, thunder, fire | Weather |

### Generation

```python
# Generate specific sound effect
sfx = generator.generate_sfx(
    prompt="anime sword swing sound effect",
    category="combat",
    duration=2.0
)

# Generate sound pack
pack = generator.generate_sound_pack(
    scene="school",
    includes=["bell", "locker", " footsteps"]
)
```

## Configuration

```yaml
# configs/providers.yaml
providers:
  primary: mubert
  fallback_order:
    - mubert
    - musicgen
    - soundful
  
  mubert:
    mode: track
    loop: true
    bpm: 120
    format: mp3
    bitrate: 320
  
  musicgen:
    model: musicgen-small
    duration: 30
    format: wav
  
  soundful:
    quality: high
    format: wav
```

## Output Formats

| Format | Use Case | Quality |
|--------|----------|---------|
| MP3 | General use | High (320kbps) |
| WAV | Editing | Lossless |
| FLAC | Archival | Lossless |
| OGG | Web | High |

## Cost Estimation

| Provider | Cost per Minute | Quality |
|----------|-----------------|---------|
| MusicGen (local) | $0.00 | Good |
| Mubert | $0.25 | Very High |
| Udio | $0.30 | Highest |
| Soundful | $0.10 | High |

## Scripts Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `scripts/generate.py` | Main generation CLI | `generate.py bgm "anime music"` |
| `scripts/batch.py` | Batch processing | `batch.py bgm prompts.txt` |
| `scripts/mix.py` | Audio mixing | `mix.py track1.wav track2.wav` |
| `scripts/adapt.py` | Adapt to scenes | `adapt.py bgm.mp4 --scene battle` |

## Workflow Integration

### With Video Generator

```python
# Generate music for scene, then combine with video
from lib.music_generator import AnimeMusicGenerator
from lib.video_generator import AnimeVideoGenerator

music_gen = AnimeMusicGenerator()
video_gen = AnimeVideoGenerator()

# Generate BGM for scene
bgm = music_gen.generate_bgm("battle scene, intense", duration=90)

# Generate video
video = video_gen.text_to_video("epic battle")

# Combine
video_gen.combine_video_audio(video.video_path, bgm.audio_path, "final.mp4")
```

### With Voice Generator

```python
# Mix background music with dialogue
bgm = music_gen.generate_bgm("calm school", duration=60)
voice = voice_gen.generate("dialogue", voice="hinata")

# Mix audio tracks
mixed = music_gen.mix_tracks(
    [bgm.audio_path, voice.audio_path],
    volumes=[0.3, 1.0],
    output="scene_audio.mp3"
)
```

## Troubleshooting

### Common Issues

**Music doesn't match scene:**
- Use scene-specific prompts
- Adjust BPM to match video pace
- Try different mood settings

**Quality issues:**
- Use higher bitrate settings
- Try different providers
- Post-process with audio tools

**Loop issues:**
- Enable loop mode in settings
- Use seamless loop tags
- Check crossfade options

### Performance Tips

1. Use local MusicGen for testing
2. Generate shorter clips, then extend
3. Use prompts with clear mood indicators
4. Cache generated tracks

## Limitations

### Current Limitations
- No real-time generation preview
- Limited stem separation
- No vocal removal

### Planned Features
- [ ] Stem separation (vocals/instruments)
- [ ] Tempo/speed adjustment
- [ ] Loop point detection
- [ ] Audio to MIDI conversion

## References

- [Mubert API](https://mubert.com/docs/api)
- [Google MusicGen](https://github.com/facebookresearch/MusicGen)
- [Udio API](https://udio.com/api-docs)
- [Soundful](https://soundful.com/api-docs)
