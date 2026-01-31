#!/usr/bin/env python3
"""
Translator CLI - Script translation for anime productions
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from translator import Translator, TranslationConfig, Provider


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Translator - Script translation for anime",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate single text
  %(prog)s text "Hello world" --to zh
  
  # Translate SRT file
  %(prog)s file dialogue.srt translated.srt --from en --to zh
  
  # Batch translate
  %(prog)s batch ./en_subs ./zh_subs --pattern "*.srt"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Text
    text_parser = subparsers.add_parser("text", help="Translate single text")
    text_parser.add_argument("text", help="Text to translate")
    text_parser.add_argument("--from", dest="source", default="en")
    text_parser.add_argument("--to", dest="target", default="zh")
    text_parser.add_argument("--provider", default="google")
    
    # File
    file_parser = subparsers.add_parser("file", help="Translate file")
    file_parser.add_argument("input", help="Input file")
    file_parser.add_argument("output", help="Output file")
    file_parser.add_argument("--from", dest="source", default="en")
    file_parser.add_argument("--to", dest="target", default="zh")
    file_parser.add_argument("--format", default="srt")
    
    # Batch
    batch_parser = subparsers.add_parser("batch", help="Batch translate")
    batch_parser.add_argument("input_dir", help="Input directory")
    batch_parser.add_argument("output_dir", help="Output directory")
    batch_parser.add_argument("--from", dest="source", default="en")
    batch_parser.add_argument("--to", dest="target", default="zh")
    batch_parser.add_argument("--pattern", default="*.srt")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    provider_map = {
        "google": Provider.GOOGLE,
        "deepl": Provider.DEEPL,
        "openai": Provider.OPENAI,
    }
    
    config = TranslationConfig(
        source_lang=args.source if 'source' in args else "en",
        target_lang=args.target if 'target' in args else "zh",
        provider=provider_map.get(args.provider, Provider.GOOGLE) if 'provider' in args else Provider.GOOGLE,
    )
    
    translator = Translator(config)
    
    if args.command == "text":
        result = translator.translate(args.text)
        print(f"\n📝 {result}\n")
    
    elif args.command == "file":
        success = translator.translate_file(
            Path(args.input),
            Path(args.output),
            getattr(args, 'format', 'srt')
        )
        if success:
            print(f"✅ Translated: {args.output}")
    
    elif args.command == "batch":
        results = translator.batch_translate(
            Path(args.input_dir),
            Path(args.output_dir),
            getattr(args, 'pattern', '*.srt')
        )
        completed = sum(1 for v in results.values() if v)
        print(f"✅ Completed: {completed}/{len(results)} files")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
