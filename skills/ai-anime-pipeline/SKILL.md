# Anime Pipeline

End-to-end anime production workflow. Coordinates script → storyboard → images → video → audio → subtitles → final output.

## Installation

```bash
cd skills/ai-anime-pipeline
pip install -r requirements.txt
```

## Quick Start

### 1. Initialize Project

```bash
# Create a new project with 5 scenes
python scripts/generate.py init my_anime --scenes 5

# Or use a template
python scripts/generate.py init short_anime --template short --scenes 10
```

### 2. Configure Scenes

Edit the generated `project.yaml`:

```yaml
name: my_anime
output_dir: ./output
scenes:
  - scene_id: "01"
    description: "少女在樱花盛开的校园中醒来"
    dialogue: "新しい一日が始まる..."
    duration: 5.0
    style: anime
    characters: [" heroine"]
    mood: happy
  - scene_id: "02"
    description: "主角走进教室，看到新同学"
    duration: 6.0
    mood: curious
```

### 3. Run Pipeline

```bash
# Run full pipeline
python scripts/generate.py run my_anime/project.yaml

# Run specific stages only
python scripts/generate.py run my_anime/project.yaml --stages images,video

# Dry run (show what would happen)
python scripts/generate.py run my_anime/project.yaml --dry-run
```

## Stages

| Stage | Description | Output |
|-------|-------------|--------|
| script | Process scene configurations | project.yaml |
| storyboard | Generate scene breakdowns | storyboards/*.json |
| images | Generate character/background images | images/*.png |
| video | Generate video clips | videos/*.mp4 |
| voice | Generate voiceovers | audio/voice/*.wav |
| music | Generate background music | audio/music/bgm.wav |
| subtitles | Generate SRT subtitles | subtitles/*.srt |
| edit | Combine all elements | output/*_unedited.mp4 |
| color | Apply color grading | output/*_graded.mp4 |
| output | Final export | output/*.mp4 |

## Project Structure

```
my_anime/
├── project.yaml              # Project configuration
├── production_report.json    # After running
├── scenes/                   # Scene scripts
├── storyboards/              # Scene breakdowns
├── images/                   # Generated images
├── videos/                   # Generated video clips
├── audio/
│   ├── voice/               # Voiceover files
│   └── music/               # Background music
├── subtitles/               # Subtitle files
├── output/                  # Final outputs
└── logs/                    # Production logs
```

## Integration with Other Skills

This pipeline coordinates with other AI Anime skills:

```bash
# After images are generated, continue to video
python scripts/generate.py run project.yaml --stages video

# Generate voice for existing dialogue
python scripts/generate.py run project.yaml --stages voice
```

## Parallel Processing

```bash
# Run independent stages in parallel
python scripts/generate.py run project.yaml --parallel
```

Stages that can run in parallel:
- images (per scene)
- video (per scene)
- voice (per scene)

## Environment Variables

```bash
# Optional API keys for downstream skills
export STABILITY_API_KEY="..."
export ELEVENLABS_API_KEY="..."
export MUBERT_API_KEY="..."
```

## Tips

1. **Start Small**: Begin with 3-5 scenes to test your workflow
2. **Check Progress**: Run with `--dry-run` first
3. **Resume Failed**: Re-run to continue from where you left off
4. **Custom Stages**: Use `--stages` to run only what you need
