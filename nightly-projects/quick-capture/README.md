# Quick Note Capture (qn) ✨ Enhanced

A lightweight CLI tool to quickly capture notes to your daily memory file. Now with **tags** and **search**!

## Installation

```bash
# One-line install
mkdir -p ~/bin
cp /home/zous/clawd/nightly-projects/quick-capture/qn ~/bin/qn
chmod +x ~/bin/qn

# Add to PATH
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Update

```bash
cp /home/zous/clawd/nightly-projects/quick-capture/qn ~/bin/qn
```

## Usage

### Capture a quick note
```bash
qn "Buy milk and eggs"
```

### Capture with tags
```bash
qn "Review PR #github #coding"
qn "Finish design #design #urgent"
```

### Capture multiline notes
```bash
qn -m "Meeting notes
- Discuss project timeline
- Review budget
- Action items"
```

### View today's notes
```bash
qn --today
```

### Search all notes
```bash
qn --search "python"
qn --search "AI"
```

### Show recent notes (last 3 days)
```bash
qn --recent
```

### List all tags
```bash
qn --tags
```

## Examples

```bash
qn "学习 Claude Code CLI #learning #ai"
qn "买咖啡 #life"
qn "修复 bug #coding #urgent"
qn --search "AI"
qn --tags
```

## Features

- 📝 Quick capture with timestamp
- 🏷️ Tag support (`#tag`)
- 🔍 Full-text search
- 📊 Tag statistics
- 📅 Multi-day history

## Notes

- Saved to `~/clawd/memory/YYYY-MM-DD.md`
- Works anywhere from command line
- Integrates with Clawdbot memory system
