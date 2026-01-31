#!/usr/bin/env python3
"""
Translator - Script translation for anime productions

Supports multiple translation services.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Provider(Enum):
    """Translation providers"""
    GOOGLE = "google"
    DEEPL = "deepl"
    OPENAI = "openai"
    AZURE = "azure"
    CUSTOM = "custom"


@dataclass
class TranslationConfig:
    """Translation configuration"""
    source_lang: str
    target_lang: str
    provider: Provider = Provider.GOOGLE
    api_key: Optional[str] = None
    formality: str = "default"  # default, formal, informal


@dataclass
class TranslationResult:
    """Translation result"""
    original: str
    translated: str
    source_lang: str
    target_lang: str
    confidence: float = 1.0
    provider: str = "google"


class Translator:
    """Main translator class"""
    
    def __init__(self, config: Optional[TranslationConfig] = None):
        self.config = config or TranslationConfig(
            source_lang="en",
            target_lang="zh",
        )
    
    def translate(self, text: str) -> str:
        """Translate single text"""
        if not text.strip():
            return text
        
        if self.config.provider == Provider.GOOGLE:
            return self._translate_google(text)
        elif self.config.provider == Provider.DEEPL:
            return self._translate_deepl(text)
        elif self.config.provider == Provider.OPENAI:
            return self._translate_openai(text)
        else:
            return self._translate_simple(text)
    
    def _translate_google(self, text: str) -> str:
        """Google Translate (using basic API)"""
        try:
            from googletrans import Translator as GoogleTranslator
            result = GoogleTranslator().translate(
                text, 
                src=self.config.source_lang,
                dest=self.config.target_lang
            )
            return result.text
        except ImportError:
            logger.warning("⚠️  googletrans not installed. Using simple fallback.")
            return self._translate_simple(text)
        except Exception as e:
            logger.error(f"❌ Google Translate error: {e}")
            return self._translate_simple(text)
    
    def _translate_deepl(self, text: str) -> str:
        """DeepL Translate"""
        api_key = self.config.api_key or os.environ.get("DEEPL_API_KEY")
        if not api_key:
            logger.warning("⚠️  DeepL API key not set. Using fallback.")
            return self._translate_simple(text)
        
        try:
            import requests
            response = requests.post(
                "https://api-free.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
                data={
                    "text": text,
                    "source_lang": self.config.source_lang.upper(),
                    "target_lang": self.config.target_lang.upper(),
                }
            )
            result = response.json()
            return result["translations"][0]["text"]
        except Exception as e:
            logger.error(f"❌ DeepL error: {e}")
            return self._translate_simple(text)
    
    def _translate_openai(self, text: str) -> str:
        """OpenAI Translate"""
        api_key = self.config.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("⚠️  OpenAI API key not set. Using fallback.")
            return self._translate_simple(text)
        
        try:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Translate from {self.config.source_lang} to {self.config.target_lang}. Keep the same tone and style."},
                    {"role": "user", "content": text}
                ],
                api_key=api_key,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ OpenAI error: {e}")
            return self._translate_simple(text)
    
    def _translate_simple(self, text: str) -> str:
        """Simple word-by-word fallback (for demo/development)"""
        # This is a placeholder - in production, use real API
        logger.info(f"📝 Would translate: {text[:50]}...")
        
        # Simple mapping for common anime terms
        mappings = {
            "hello": "你好",
            "goodbye": "再见",
            "thank you": "谢谢",
            "yes": "是",
            "no": "不是",
            "I": "我",
            "you": "你",
            "we": "我们",
            "the": "",
            "a": "",
        }
        
        result = text
        for en, zh in mappings.items():
            result = result.replace(en, zh)
        
        return result if result != text else f"[ZH] {text}"
    
    def translate_file(
        self,
        input_file: Path,
        output_file: Path,
        format: str = "srt",
    ) -> bool:
        """Translate subtitle/script file"""
        if not input_file.exists():
            logger.error(f"❌ File not found: {input_file}")
            return False
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format == "srt":
                return self._translate_srt(input_file, output_file)
            elif format == "txt":
                return self._translate_txt(input_file, output_file)
            elif format == "json":
                return self._translate_json(input_file, output_file)
            else:
                return self._translate_txt(input_file, output_file)
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return False
    
    def _translate_srt(self, input_file: Path, output_file: Path) -> bool:
        """Translate SRT subtitle file"""
        content = input_file.read_text()
        lines = content.split("\n")
        
        result_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip timestamps
            if "-->" in line:
                result_lines.append(line)
                i += 1
                continue
            
            # Skip index
            if line.isdigit():
                result_lines.append(line)
                i += 1
                continue
            
            # Translate dialogue
            if line.strip():
                translated = self.translate(line)
                result_lines.append(translated)
            else:
                result_lines.append(line)
            
            i += 1
        
        output_file.write_text("\n".join(result_lines))
        logger.info(f"✅ Translated: {output_file}")
        return True
    
    def _translate_txt(self, input_file: Path, output_file: Path) -> bool:
        """Translate plain text file"""
        content = input_file.read_text()
        paragraphs = content.split("\n\n")
        
        translated = []
        for para in paragraphs:
            if para.strip():
                translated.append(self.translate(para))
            else:
                translated.append("")
        
        output_file.write_text("\n\n".join(translated))
        logger.info(f"✅ Translated: {output_file}")
        return True
    
    def _translate_json(self, input_file: Path, output_file: Path) -> bool:
        """Translate JSON file (for dialogue scripts)"""
        data = json.loads(input_file.read_text())
        
        def translate_item(item):
            if isinstance(item, str):
                return self.translate(item)
            elif isinstance(item, dict):
                return {k: translate_item(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [translate_item(i) for i in item]
            return item
        
        translated_data = translate_item(data)
        output_file.write_text(json.dumps(translated_data, ensure_ascii=False, indent=2))
        logger.info(f"✅ Translated: {output_file}")
        return True
    
    def translate_dialogue(
        self,
        dialogue_file: Path,
        output_file: Path,
    ) -> bool:
        """Translate dialogue JSON file"""
        return self.translate_file(dialogue_file, output_file, format="json")
    
    def batch_translate(
        self,
        input_dir: Path,
        output_dir: Path,
        pattern: str = "*.srt",
        format: str = "srt",
    ) -> Dict[str, bool]:
        """Batch translate files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        for input_file in input_dir.glob(pattern):
            output_file = output_dir / input_file.name
            success = self.translate_file(input_file, output_file, format)
            results[str(input_file)] = success
        
        completed = sum(1 for v in results.values() if v)
        logger.info(f"✅ Batch translate: {completed}/{len(results)} files")
        
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Translator")
    subparsers = parser.add_subparsers(dest="command")
    
    # Single translate
    single_parser = subparsers.add_parser("text", help="Translate single text")
    single_parser.add_argument("text", help="Text to translate")
    single_parser.add_argument("--from", dest="source", default="en")
    single_parser.add_argument("--to", dest="target", default="zh")
    
    # File translate
    file_parser = subparsers.add_parser("file", help="Translate file")
    file_parser.add_argument("input", help="Input file")
    file_parser.add_argument("output", help="Output file")
    file_parser.add_argument("--format", default="srt")
    
    # Batch
    batch_parser = subparsers.add_parser("batch", help="Batch translate")
    batch_parser.add_argument("input_dir", help="Input directory")
    batch_parser.add_argument("output_dir", help="Output directory")
    batch_parser.add_argument("--pattern", default="*.srt")
    
    args = parser.parse_args()
    
    translator = Translator()
    
    if args.command == "text":
        config = TranslationConfig(source_lang=args.source, target_lang=args.target)
        translator = Translator(config)
        result = translator.translate(args.text)
        print(f"📝 {result}")
    
    elif args.command == "file":
        translator.translate_file(Path(args.input), Path(args.output), args.format)
    
    elif args.command == "batch":
        translator.batch_translate(Path(args.input_dir), Path(args.output_dir), args.pattern)
    
    else:
        parser.print_help()
