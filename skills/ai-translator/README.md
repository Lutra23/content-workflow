# Translator

Script translation for anime.

## Usage

```bash
# Translate text
python scripts/generate.py text "Hello" --to zh

# Translate file
python scripts/generate.py file input.srt output.srt --from en --to zh

# Batch
python scripts/generate.py batch ./in ./out --pattern "*.srt"
```

See [SKILL.md](SKILL.md) for full documentation.
