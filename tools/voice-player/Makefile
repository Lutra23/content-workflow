.PHONY: install play play-latest list help

# Install audio dependencies
install:
	@echo "📦 Installing audio dependencies..."
	@if command -v apt-get &> /dev/null; then \
		sudo apt-get update -qq && \
		sudo apt-get install -y ffmpeg pulseaudio-utils; \
	elif command -v dnf &> /dev/null; then \
		sudo dnf install -y ffmpeg; \
	else \
		echo "Please install ffmpeg manually:"; \
		echo "  - Debian/Ubuntu: sudo apt install ffmpeg"; \
		echo "  - macOS: brew install ffmpeg"; \
	fi
	@echo ""
	@echo "✅ Dependencies installed!"
	@echo ""
	@echo "Available audio players:"
	@which ffplay paplay aplay 2>/dev/null | head -3 || echo "  None found"

# Play a specific file
play:
	@if [ -z "$(file)" ]; then \
		echo "Usage: make play file=/path/to/message.ogg"; \
	else \
		python3 voice_player.py $(file); \
	fi

# Play latest voice message
play-latest:
	@echo "🔊 Playing latest voice message..."
	@python3 voice_player.py --latest

# List all voice files
list:
	@python3 voice_player.py --list

# Show directory and status
status:
	@python3 voice_player.py --dir

# Show help
help:
	@echo "🔊 Voice Player for Clawdbot"
	@echo ""
	@echo "Commands:"
	@echo "  make install       Install audio dependencies"
	@echo "  make play-latest   Play the latest voice message"
	@echo "  make list          List all voice files"
	@echo "  make status        Show directory and audio status"
	@echo "  make help          Show this help"
	@echo ""
	@echo "Direct usage:"
	@echo "  python voice_player.py --latest"
	@echo "  python voice_player.py message.ogg"
	@echo "  python voice_player.py --list"
