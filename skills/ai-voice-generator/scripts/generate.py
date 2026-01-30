#!/usr/bin/env python3
"""
Anime Voice Generator CLI - Voice synthesis script
"""

import os
import sys
import argparse
from pathlib import Path
from lib.voice_generator import AnimeVoiceGenerator, VoiceProvider, Emotion


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime character voices using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic voice synthesis
  %(prog)s speak "こんにちは、元気ですか？" --voice hinata --emotion happy
  
  # Generate narration
  %(prog)s narrate "長い旅が始まる..." --style dramatic
  
  # Generate with specific provider
  %(prog)s speak "Hello!" --provider elevenlabs --voice my_voice
  
  # Generate with lip sync data
  %(prog)s speak "こんにちは" --voice asuka --lipsync --output visemes.json
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Generation mode")
    
    # Speak mode
    speak_parser = subparsers.add_parser("speak", help="Generate voice from text")
    speak_parser.add_argument("text", help="Text to synthesize")
    speak_parser.add_argument("--voice", default="hinata", help="Voice preset or ID")
    speak_parser.add_argument("--emotion", default="neutral",
                             choices=["neutral", "happy", "sad", "angry", "surprised", "fearful", "calm"],
                             help="Emotion to convey")
    speak_parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5-2.0)")
    speak_parser.add_argument("--pitch", type=float, default=0.0, help="Pitch adjustment")
    speak_parser.add_argument("--provider", default="auto", help="Voice provider")
    speak_parser.add_argument("--output", "-o", help="Output file path")
    speak_parser.add_argument("--format", default="mp3", help="Output format (mp3/wav)")
    speak_parser.add_argument("--lipsync", action="store_true", help="Generate lip sync data")
    
    # Narrate mode
    narrate_parser = subparsers.add_parser("narrate", help="Generate narration")
    narrate_parser.add_argument("text", help="Narration text")
    narrate_parser.add_argument("--style", default="gentle",
                               choices=["dramatic", "gentle", "action", "mysterious"],
                               help="Narration style")
    narrate_parser.add_argument("--voice", default="narrator", help="Voice preset")
    narrate_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Initialize generator
    generator = AnimeVoiceGenerator()
    
    # Parse provider
    provider_map = {
        "auto": VoiceProvider.AUTO,
        "elevenlabs": VoiceProvider.ELEVENLABS,
        "openai": VoiceProvider.OPENAI,
        "azure": VoiceProvider.AZURE,
        "coqui": VoiceProvider.COQUI
    }
    provider = provider_map.get(args.provider.lower(), VoiceProvider.AUTO)
    
    if args.mode == "speak":
        if args.lipsync:
            result = generator.generate_with_lipsync(
                text=args.text,
                voice=args.voice,
                emotion=args.emotion,
                provider=provider
            )
            
            # Output viseme data
            if result.success:
                output = {
                    "audio_path": result.audio_path,
                    "visemes": result.visemes,
                    "duration": result.duration
                }
                print(json.dumps(output, indent=2, ensure_ascii=False))
            else:
                print(f"❌ Failed: {result.error}")
                return 1
        else:
            result = generator.generate(
                text=args.text,
                voice=args.voice,
                emotion=args.emotion,
                speed=args.speed,
                pitch=args.pitch,
                provider=provider,
                output_path=args.output,
                output_format=args.format
            )
    
    elif args.mode == "narrate":
        # Apply style presets
        style_configs = {
            "dramatic": {"speed": 0.9, "pitch": -2},
            "gentle": {"speed": 1.0, "pitch": 0},
            "action": {"speed": 1.1, "pitch": 2},
            "mysterious": {"speed": 0.95, "pitch": -1}
        }
        style = style_configs.get(args.style, {})
        
        result = generator.generate(
            text=args.text,
            voice=args.voice,
            emotion="neutral",
            speed=style.get("speed", 1.0),
            pitch=style.get("pitch", 0.0),
            provider=provider,
            output_path=args.output,
            output_format=args.format
        )
    
    # Output results
    if result.success:
        print(f"✅ Success! Audio saved to: {result.audio_path}")
        print(f"   Provider: {result.provider}")
        print(f"   Duration: {result.duration:.2f}s")
        print(f"   Text: {result.text[:50]}..." if len(result.text or "") > 50 else f"   Text: {result.text}")
        return 0
    else:
        print(f"❌ Failed: {result.error}")
        return 1


if __name__ == "__main__":
    import json
    sys.exit(main())
