# 🔍 Emoji Search (es)

Quick CLI tool to search and copy emojis.

## Install

```bash
# Make it globally available
cd /home/zous/clawd/nightly-projects/emoji-search
python main.py --install  # Add to PATH (optional)
# Or just run directly
python main.py fire
```

## Usage

```bash
# Search for emojis
python main.py fire

# Search with multiple words
python main.py "happy cat"

# Output:
# 🔍 Found 10 emojis for 'fire':
#
#  1. 🔥  (fire, flame, burning)
#  2. 𖡨  (fire, flame, burning)
#  3. 𖤐  (fire, flame)
# ...
```

## Features

- 🔍 Keyword search
- 📋 Copy support (coming soon)
- 🏷️ Show emoji aliases

## Future

- `--copy <num>` to copy emoji to clipboard
- `--random` for random emoji
- `--category` filter
