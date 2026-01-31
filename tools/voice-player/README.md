# 🔊 Voice Message Player for Clawdbot

Plays Feishu voice messages (OGG/opus format) from Clawdbot.

## Quick Start

```bash
# Install audio dependencies (once)
make install

# Play the latest voice message
make play-latest

# List all voice files
make list
```

## Installation

```bash
cd /home/zous/clawd/tools/voice-player

# Install system audio dependencies
make install
# Or manually:
# sudo apt install ffmpeg pulseaudio-utils
```

## Usage

```bash
# Play a specific file
python voice_player.py /path/to/message.ogg

# Play latest voice file
python voice_player.py --latest
python voice_player.py -l

# List all voice files
python voice_player.py --list
python voice_player.py -ls

# Show voice directory and available players
python voice_player.py --dir
```

## Requirements

- **ffmpeg** (for ffplay) - Recommended
- **pulseaudio** (for paplay) - Alternative for Linux
- **alsa** (for aplay) - Fallback for Linux

Install all with: `sudo apt install ffmpeg pulseaudio-utils`

## Add to Crontab (Optional)

Play latest voice every 5 minutes:

```bash
crontab -e

# Add this line:
*/5 * * * * cd /home/zous/clawd/tools/voice-player && python voice_player.py --latest >> /tmp/voice.log 2>&1
```

## WSL Notes

For WSL to play audio through Windows:

```bash
# Option 1: Install PulseAudio server on Windows
# Download: https://www.portaudio.com/ (or use WSLg)

# Option 2: Use Windows FFmpeg with network audio
# Install FFmpeg on Windows, then:
ffplay -nodisp -autoexit /mnt/c/Users/YourName/Downloads/message.ogg
```

## File Locations

- **Voice files**: `/home/zous/.clawdbot/media/inbound/`
- **Log file**: `/tmp/voice.log` (when using crontab)

## Supported Formats

OGG, MP3, WAV, M4A, AAC

---

Made with 🦦 by lutra
