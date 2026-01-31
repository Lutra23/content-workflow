# Translator

Script translation for anime productions. Supports SRT, TXT, JSON formats with multiple providers.

## Installation

```bash
cd skills/ai-translator
pip install -r requirements.txt

# Optional: Install API libraries
pip install googletrans      # Google Translate
pip install openai           # OpenAI Translate
pip install requests        # HTTP client
```

## Quick Start

### Translate Single Text

```bash
# English to Chinese
python scripts/generate.py text "Hello, world!" --to zh

# Japanese to English
python scripts/generate.py text "こんにちは" --from ja --to en
```

### Translate SRT Subtitles

```bash
# English to Chinese
python scripts/generate.py file english.srt chinese.srt --from en --to zh

# Japanese to English
python scripts/generate.py file japanese.srt english.srt --from ja --to en
```

### Batch Translate

```bash
# Translate all SRT files in directory
python scripts/generate.py batch ./en_subs ./zh_subs --from en --to zh

# Custom file pattern
python scripts/generate.py batch ./dialogues ./translations --pattern "*.txt"
```

## Supported Formats

| Format | Description | Example |
|--------|-------------|---------|
| SRT | SubRip subtitles | `dialogue.srt` |
| TXT | Plain text | `script.txt` |
| JSON | Dialogue scripts | `dialogue.json` |

## Providers

| Provider | Quality | API Key Required |
|----------|---------|------------------|
| Google | Good | No (rate limited) |
| DeepL | Excellent | Yes (`DEEPL_API_KEY`) |
| OpenAI | Best | Yes (`OPENAI_API_KEY`) |
| Fallback | Basic | No |

### Configure API Keys

```bash
# DeepL
export DEEPL_API_KEY="your-key"

# OpenAI
export OPENAI_API_KEY="your-key"
```

## Integration with Pipeline

```bash
# Translate subtitles after generation
python scripts/generate.py file subtitles/en.srt subtitles/zh.srt --from en --to zh

# Add to final video
ffmpeg -i video.mp4 -vf subtitles=subs.srt final.mp4
```

## Tips

1. **Quality**: OpenAI > DeepL > Google > Fallback
2. **Context**: Translate full scene, not just single lines
3. **Review**: Always review machine translations
4. **Formal vs Informal**: Use `--formality formal` for business content
