#!/usr/bin/env python3
"""
🔊 Voice Message Player for Clawdbot
Plays Feishu/Feishu voice messages (OGG/opus format)

Usage:
    python voice_player.py <file_path>
    python voice_player.py --latest     # Play latest voice file
    python voice_player.py --list       # List all voice files
    python voice_player.py --dir        # Show voice directory
    python voice_player.py --install    # Install audio dependencies

Author: lutra 🦦
"""

import os
import sys
import glob
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
VOICE_DIR = Path("/home/zous/.clawdbot/media/inbound")
SUPPORTED_FORMATS = ('.ogg', '.mp3', '.wav', '.m4a', '.aac')


def check_audio_player():
    """Check available audio players."""
    players = []

    # Check for common audio players
    for player in ['paplay', 'aplay', 'ffplay', 'mplayer', 'cvlc']:
        try:
            subprocess.run(['which', player], capture_output=True, check=True)
            players.append(player)
        except subprocess.CalledProcessError:
            continue

    return players


def play_with_ffplay(file_path):
    """Play using ffplay (FFmpeg)."""
    try:
        # -nodisp: no display window
        # -autoexit: exit when playback finishes
        subprocess.run(['ffplay', '-nodisp', '-autoexit', str(file_path)],
                      check=True)
        return True
    except Exception as e:
        print(f"ffplay failed: {e}")
        return False


def play_with_paplay(file_path):
    """Play using paplay (PulseAudio)."""
    try:
        subprocess.run(['paplay', str(file_path)], check=True)
        return True
    except Exception as e:
        print(f"paplay failed: {e}")
        return False


def play_with_aplay(file_path):
    """Play using aplay (ALSA)."""
    try:
        subprocess.run(['aplay', str(file_path)], check=True)
        return True
    except Exception as e:
        print(f"aplay failed: {e}")
        return False


def play_voice(file_path):
    """Play a voice file using available player."""
    if not file_path or not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return False

    file_path = Path(file_path)
    print(f"🔊 Playing: {file_path.name} ...")

    # Try players in order of preference
    players = check_audio_player()

    if not players:
        print("❌ No audio player found!")
        print("   Install one of: ffmpeg (ffplay), pulseaudio (paplay), alsa (aplay)")
        print("   Run: sudo apt install ffmpeg")
        return False

    print(f"   Available players: {', '.join(players)}")

    # Try each player
    for player in ['ffplay', 'paplay', 'aplay']:
        if player in players:
            print(f"   Trying {player}...")
            if player == 'ffplay':
                if play_with_ffplay(file_path):
                    print("✅ Playback complete!")
                    return True
            elif player == 'paplay':
                if play_with_paplay(file_path):
                    print("✅ Playback complete!")
                    return True
            elif player == 'aplay':
                if play_with_aplay(file_path):
                    print("✅ Playback complete!")
                    return True

    print("❌ Playback failed with all available players")
    return False


def get_latest_voice():
    """Get the most recent voice file."""
    if not VOICE_DIR.exists():
        print(f"❌ Voice directory not found: {VOICE_DIR}")
        return None

    voice_files = []
    for ext in SUPPORTED_FORMATS:
        voice_files.extend(VOICE_DIR.glob(f"*{ext}"))

    if not voice_files:
        print("📭 No voice files found")
        return None

    latest = max(voice_files, key=lambda f: f.stat().st_mtime)
    return latest


def list_voice_files():
    """List all voice files sorted by time."""
    if not VOICE_DIR.exists():
        print(f"❌ Voice directory not found: {VOICE_DIR}")
        return []

    voice_files = []
    for ext in SUPPORTED_FORMATS:
        voice_files.extend(VOICE_DIR.glob(f"*{ext}"))

    voice_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    print(f"\n📁 Voice Files in {VOICE_DIR}:\n")
    for i, f in enumerate(voice_files, 1):
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size_kb = f.stat().st_size / 1024
        print(f"  {i:2}. [{mtime}] {f.name} ({size_kb:.1f} KB)")

    return voice_files


def install_deps():
    """Install audio dependencies."""
    print("📦 Installing audio dependencies...")

    # Detect OS and install appropriate packages
    if os.path.exists('/etc/debian_version'):  # Debian/Ubuntu
        print("   Installing ffmpeg and pulseaudio...")
        os.system('sudo apt-get update -qq')
        os.system('sudo apt-get install -y ffmpeg pulseaudio-utils')
    elif os.path.exists('/etc/redhat-release'):  # RHEL/CentOS
        print("   Installing ffmpeg...")
        os.system('sudo dnf install -y ffmpeg')
    else:
        print("   Please install ffmpeg manually:")
        print("   - Debian/Ubuntu: sudo apt install ffmpeg")
        print("   - macOS: brew install ffmpeg")
        print("   - Windows: download from https://ffmpeg.org/download.html")

    print("✅ Dependencies installed!")
    print("\nNow check audio players:")
    players = check_audio_player()
    print(f"   Available: {players or 'None'}")


def main():
    parser = argparse.ArgumentParser(
        description="🔊 Play Feishu voice messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python voice_player.py message.ogg              # Play specific file
  python voice_player.py --latest                 # Play latest voice
  python voice_player.py --list                   # List all voices
  python voice_player.py --dir                    # Show directory path
  python voice_player.py --install                # Install audio deps
        """
    )

    parser.add_argument('file', nargs='?', help='Voice file to play')
    parser.add_argument('--latest', '-l', action='store_true',
                        help='Play the most recent voice file')
    parser.add_argument('--list', '-ls', action='store_true',
                        help='List all voice files')
    parser.add_argument('--dir', '-d', action='store_true',
                        help='Show voice directory')
    parser.add_argument('--install', action='store_true',
                        help='Install required dependency (ffmpeg)')

    args = parser.parse_args()

    if args.install:
        install_deps()
        return

    if args.dir:
        print(f"📁 Voice directory: {VOICE_DIR}")
        print(f"   Exists: {VOICE_DIR.exists()}")
        if VOICE_DIR.exists():
            count = len([f for ext in SUPPORTED_FORMATS for f in VOICE_DIR.glob(f"*{ext}")])
            print(f"   Files: {count}")
        players = check_audio_player()
        if players:
            print(f"   Audio players: {', '.join(players)}")
        else:
            print("   Audio players: None (run --install)")
        return

    if args.list:
        list_voice_files()
        return

    if args.latest:
        file_path = get_latest_voice()
        if file_path:
            print(f"🎯 Latest file: {file_path.name}")
        play_voice(file_path)
        return

    if args.file:
        play_voice(args.file)
        return

    # No arguments: show help
    parser.print_help()


if __name__ == "__main__":
    main()
