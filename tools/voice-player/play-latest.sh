#!/bin/bash
# 🔊 Play latest Feishu voice message
# Usage: ./play-latest.sh

cd "$(dirname "$0")"

echo "🎧 Finding latest voice message..."
python3 voice_player.py --latest
