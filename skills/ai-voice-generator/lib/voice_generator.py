"""
AI Voice Generator - Core Module

Unified interface for multiple AI TTS/voice generation providers:
- ElevenLabs
- Azure TTS
- OpenAI TTS
- Google TTS
- Coqui TTS (local)
"""

import os
import io
import base64
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum
import yaml
import wave
import struct

import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize


class Provider(Enum):
    """Supported voice generation providers."""
    ELEVENLABS = "elevenlabs"
    AZURE = "azure"
    OPENAI = "openai"
    GOOGLE = "google"
    COQUI = "coqui"
    AUTO = "auto"


class Emotion(Enum):
    """Emotion presets for voice generation."""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    NEUTRAL = "neutral"
    GENTLE = "gentle"
    SERIOUS = "serious"
    CUTE = "cute"


@dataclass
class VoiceParams:
    """Parameters for voice generation."""
    # Text
    text: str = ""
    
    # Voice
    voice: str = ""
    voice_id: Optional[str] = None
    provider: Provider = Provider.AUTO
    
    # Style
    emotion: Emotion = Emotion.NEUTRAL
    stability: float = 0.5  # 0-1
    similarity: float = 0.75  # 0-1
    style: float = 0.0  # 0-1
    
    # Audio
    speed: float = 1.0
    pitch: float = 0.0  # semitones
    volume: float = 0.0  # dB
    
    # Output
    format: str = "mp3"
    sample_rate: int = 44100
    output_path: Optional[str] = None


@dataclass
class GeneratedAudio:
    """Result of voice generation."""
    audio_data: bytes
    format: str  # mp3, wav, etc.
    duration: float  # seconds
    sample_rate: int
    channels: int
    provider: Provider
    voice_id: Optional[str]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    local_path: Optional[str] = None


@dataclass
class VoiceProfile:
    """Voice profile for character consistency."""
    name: str
    voice: str
    voice_id: Optional[str] = None
    provider: Provider = Provider.AUTO
    base_params: Dict[str, Any] = field(default_factory=dict)
    custom_pronunciations: Dict[str, Dict] = field(default_factory=dict)


class VoiceGeneratorError(Exception):
    """Base exception for voice generation."""
    pass


class ProviderNotAvailableError(VoiceGeneratorError):
    """Raised when provider is not available."""
    pass


class RateLimitError(VoiceGeneratorError):
    """Raised when rate limit is exceeded."""
    pass


class AnimeVoiceGenerator:
    """
    Unified AI voice generator for anime/cartoon production.
    
    Usage:
        generator = AnimeVoiceGenerator()
        audio = await generator.generate_dialogue("你好，我叫小明！", voice="young_female", emotion="happy")
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the voice generator."""
        self.config = self._load_config(config_path)
        self.session = None
        self._voice_cache = {}
        self._cloned_voices = {}
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration."""
        if config_path is None:
            config_path = os.environ.get(
                "AI_VOICE_GEN_CONFIG",
                Path(__file__).parent / "configs" / "providers.yaml"
            )
        
        default_config = {
            "primary_provider": "elevenlabs",
            "fallback_order": ["elevenlabs", "azure", "openai", "google", "coqui"],
            "providers": {
                "elevenlabs": {
                    "api_url": "https://api.elevenlabs.io/v1",
                    "enabled": bool(os.environ.get("ELEVENLABS_API_KEY")),
                    "voices_per_minute": 100
                },
                "azure": {
                    "api_url": "https://eastus.tts.speech.microsoft.com",
                    "enabled": bool(os.environ.get("AZURE_SPEECH_KEY")),
                    "region": os.environ.get("AZURE_SPEECH_REGION", "eastus"),
                    "voices_per_minute": 200
                },
                "openai": {
                    "api_url": "https://api.openai.com/v1",
                    "enabled": bool(os.environ.get("OPENAI_API_KEY")),
                    "voices_per_minute": 50,
                    "model": "tts-1"
                },
                "google": {
                    "api_url": "https://texttospeech.googleapis.com/v1",
                    "enabled": bool(os.environ.get("GOOGLE_TTS_KEY")),
                    "voices_per_minute": 300
                },
                "coqui": {
                    "api_url": "http://localhost:5002",
                    "enabled": True,  # Local, no API key needed
                    "voices_per_minute": 1000
                }
            },
            "voice_presets": self._default_voice_presets(),
            "emotion_presets": self._default_emotion_presets(),
            "output": {
                "format": "mp3",
                "sample_rate": 44100,
                "bitrate": "192k",
                "channels": 1
            }
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
            default_config.update(user_config)
        
        return default_config
    
    def _default_voice_presets(self) -> Dict:
        """Default voice presets for anime characters."""
        return {
            "young_female": {
                "elevenlabs": "young_female_1",
                "azure": "zh-CN-XiaoxiaoNeural",
                "openai": "nova",
                "google": "ja-JP-Wavenet-A",
                "coqui": "pittsburgh"
            },
            "young_male": {
                "elevenlabs": "young_male_1",
                "azure": "zh-CN-YunxiNeural",
                "openai": "alloy",
                "google": "ja-JP-Wavenet-B",
                "coqui": "LJ"
            },
            "older_female": {
                "elevenlabs": "older_female_1",
                "azure": "zh-CN-XiaoyouNeural",
                "openai": "shimmer",
                "google": "en-US-Wavenet-J"
            },
            "robot": {
                "elevenlabs": "robot_voice",
                "azure": "zh-CN-XiaoshuangNeural",
                "openai": "echo"
            }
        }
    
    def _default_emotion_presets(self) -> Dict:
        """Default emotion presets."""
        return {
            "happy": {"stability": 0.5, "similarity": 0.75, "style": 0.5},
            "sad": {"stability": 0.7, "similarity": 0.8, "style": 0.2},
            "angry": {"stability": 0.3, "similarity": 0.7, "style": 0.8},
            "surprised": {"stability": 0.4, "similarity": 0.7, "style": 0.6},
            "neutral": {"stability": 0.7, "similarity": 0.8, "style": 0.0},
            "gentle": {"stability": 0.6, "similarity": 0.8, "style": 0.3},
            "serious": {"stability": 0.6, "similarity": 0.8, "style": 0.1},
            "cute": {"stability": 0.4, "similarity": 0.8, "style": 0.7}
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def _get_emotion_params(self, emotion: Emotion) -> Dict[str, float]:
        """Get generation parameters for emotion."""
        emotion_str = emotion.value if isinstance(emotion, Emotion) else emotion
        presets = self.config.get("emotion_presets", {})
        return presets.get(emotion_str, presets.get("neutral", {"stability": 0.7, "similarity": 0.8, "style": 0.0}))
    
    async def generate_dialogue(
        self,
        text: str,
        voice: str = "young_female",
        emotion: Emotion = Emotion.NEUTRAL,
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> GeneratedAudio:
        """
        Generate character dialogue audio.
        
        Args:
            text: Dialogue text
            voice: Voice preset name
            emotion: Emotion preset
            provider: Provider selection
            
        Returns:
            GeneratedAudio object
        """
        params = VoiceParams(
            text=text,
            voice=voice,
            emotion=emotion,
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def generate_tts(
        self,
        text: str,
        language: str = "zh-CN",
        provider: Provider = Provider.AUTO,
        voice: Optional[str] = None,
        **kwargs
    ) -> GeneratedAudio:
        """
        Generate TTS audio for narration.
        
        Args:
            text: Text to speak
            language: Language code (zh-CN, en-US, ja-JP, etc.)
            provider: Provider selection
            voice: Specific voice name
            
        Returns:
            GeneratedAudio object
        """
        params = VoiceParams(
            text=text,
            voice=voice or f"{language}_default",
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def _generate(self, params: VoiceParams) -> GeneratedAudio:
        """Internal generation with provider fallback."""
        providers = self._get_provider_order(params.provider)
        
        last_error = None
        for provider in providers:
            try:
                if provider == Provider.ELEVENLABS:
                    return await self._generate_elevenlabs(params)
                elif provider == Provider.AZURE:
                    return await self._generate_azure(params)
                elif provider == Provider.OPENAI:
                    return await self._generate_openai(params)
                elif provider == Provider.GOOGLE:
                    return await self._generate_google(params)
                elif provider == Provider.COQUI:
                    return await self._generate_coqui(params)
            except ProviderNotAvailableError as e:
                last_error = e
                continue
            except Exception as e:
                last_error = e
                continue
        
        raise VoiceGeneratorError(f"All providers failed: {last_error}")
    
    def _get_provider_order(self, provider: Provider) -> List[Provider]:
        """Get ordered list of providers."""
        if provider != Provider.AUTO:
            return [provider]
        
        fallbacks = self.config.get("fallback_order", [])
        return [Provider(p) for p in fallbacks]
    
    async def _generate_elevenlabs(self, params: VoiceParams) -> GeneratedAudio:
        """Generate using ElevenLabs."""
        config = self.config["providers"]["elevenlabs"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("ElevenLabs not enabled")
        
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        
        # Get voice ID
        voice_id = params.voice_id
        if not voice_id:
            voice_presets = self.config.get("voice_presets", {})
            voice_id = voice_presets.get(params.voice, {}).get("elevenlabs", params.voice)
        
        # Get emotion parameters
        emotion_params = self._get_emotion_params(params.emotion)
        
        session = await self._get_session()
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": params.text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": emotion_params.get("stability", 0.5),
                "similarity_boost": emotion_params.get("similarity", 0.75),
                "style": emotion_params.get("style", 0.0),
                "use_speaker_boost": True
            }
        }
        
        async with session.post(
            f"{config['api_url']}/voices/{voice_id}/text-to-speech",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 429:
                raise RateLimitError("ElevenLabs rate limit exceeded")
            if response.status != 200:
                error = await response.text()
                raise VoiceGeneratorError(f"ElevenLabs error: {error}")
            
            audio_data = await response.read()
            
            # Get duration
            audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
            duration = len(audio) / 1000.0
            
            return GeneratedAudio(
                audio_data=audio_data,
                format="mp3",
                duration=duration,
                sample_rate=44100,
                channels=1,
                provider=Provider.ELEVENLABS,
                voice_id=voice_id,
                text=params.text,
                metadata={"model": "eleven_multilingual_v2"}
            )
    
    async def _generate_azure(self, params: VoiceParams) -> GeneratedAudio:
        """Generate using Azure TTS."""
        config = self.config["providers"]["azure"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Azure not enabled")
        
        api_key = os.environ.get("AZURE_SPEECH_KEY")
        region = config.get("region", "eastus")
        
        # Build SSML
        voice_name = params.voice
        voice_presets = self.config.get("voice_presets", {})
        voice_name = voice_presets.get(params.voice, {}).get("azure", params.voice)
        
        emotion_params = self._get_emotion_params(params.emotion)
        
        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
            <voice name="{voice_name}">
                <mstts:express-as style="{params.emotion.value}">
                    <prosody rate="{params.speed}" pitch="{params.pitch}st">
                        {params.text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>"""
        
        # For now, raise not implemented - Azure requires specific SDK
        raise ProviderNotAvailableError("Azure TTS - requires Azure SDK setup")
    
    async def _generate_openai(self, params: VoiceParams) -> GeneratedAudio:
        """Generate using OpenAI TTS."""
        config = self.config["providers"]["openai"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("OpenAI not enabled")
        
        api_key = os.environ.get("OPENAI_API_KEY")
        
        # Map voice preset to OpenAI voice
        voice_presets = self.config.get("voice_presets", {})
        voice_name = voice_presets.get(params.voice, {}).get("openai", "alloy")
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.get("model", "tts-1"),
            "input": params.text,
            "voice": voice_name,
            "response_format": "mp3",
            "speed": params.speed
        }
        
        async with session.post(
            f"{config['api_url']}/audio/speech",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                error = await response.text()
                raise VoiceGeneratorError(f"OpenAI error: {error}")
            
            audio_data = await response.read()
            
            # Get duration
            audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
            duration = len(audio) / 1000.0
            
            return GeneratedAudio(
                audio_data=audio_data,
                format="mp3",
                duration=duration,
                sample_rate=44100,
                channels=1,
                provider=Provider.OPENAI,
                voice_id=voice_name,
                text=params.text,
                metadata={"model": payload["model"]}
            )
    
    async def _generate_google(self, params: VoiceParams) -> GeneratedAudio:
        """Generate using Google TTS."""
        config = self.config["providers"]["google"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Google not enabled")
        
        api_key = os.environ.get("GOOGLE_TTS_KEY")
        
        # Placeholder - requires google-cloud-texttospeech SDK
        raise ProviderNotAvailableError("Google TTS - not yet implemented")
    
    async def _generate_coqui(self, params: VoiceParams) -> GeneratedAudio:
        """Generate using Coqui TTS (local)."""
        config = self.config["providers"]["coqui"]
        
        # Placeholder - local TTS requires server setup
        raise ProviderNotAvailableError("Coqui TTS - requires local server setup")
    
    async def clone_voice(
        self,
        audio_sample: str,
        name: str,
        provider: Provider = Provider.ELEVENLABS
    ) -> str:
        """
        Clone a voice from audio sample.
        
        Args:
            audio_sample: Path to audio file
            name: Name for cloned voice
            provider: Provider for cloning
            
        Returns:
            voice_id of cloned voice
        """
        if provider == Provider.ELEVENLABS:
            return await self._clone_elevenlabs(audio_sample, name)
        else:
            raise ProviderNotAvailableError(f"Voice cloning not supported for {provider}")
    
    async def _clone_elevenlabs(self, audio_sample: str, name: str) -> str:
        """Clone voice using ElevenLabs."""
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise ProviderNotAvailableError("ELEVENLABS_API_KEY not set")
        
        session = await self._get_session()
        headers = {
            "Accept": "application/json",
            "xi-api-key": api_key
        }
        
        # Upload audio sample
        with open(audio_sample, "rb") as f:
            files = {"files": (audio_sample, f, "audio/mpeg")}
            data = {"name": name, "description": "Cloned voice for anime character"}
            
            async with session.post(
                "https://api.elevenlabs.io/v1/voices/add",
                headers=headers,
                data=data
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise VoiceGeneratorError(f"Voice cloning failed: {error}")
                
                result = await response.json()
                voice_id = result["voice_id"]
                
                # Cache the cloned voice
                self._cloned_voices[name] = voice_id
                
                return voice_id
    
    def create_voice_profile(
        self,
        name: str,
        voice: str,
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> VoiceProfile:
        """Create a voice profile for character consistency."""
        return VoiceProfile(
            name=name,
            voice=voice,
            provider=provider,
            base_params=kwargs
        )
    
    async def generate_with_profile(
        self,
        text: str,
        profile: VoiceProfile,
        emotion: Emotion = Emotion.NEUTRAL,
        **kwargs
    ) -> GeneratedAudio:
        """Generate audio using a voice profile."""
        params = VoiceParams(
            text=text,
            voice=profile.voice,
            voice_id=profile.voice_id,
            provider=profile.provider,
            emotion=emotion,
            **kwargs
        )
        params.base_params.update(profile.base_params)
        return await self._generate(params)
    
    async def batch_generate(
        self,
        script: str,
        voice: str = "young_female",
        emotions: Optional[List[Emotion]] = None,
        provider: Provider = Provider.AUTO,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> List[GeneratedAudio]:
        """Generate audio from a dialogue script."""
        # Parse script
        lines = self._parse_script(script)
        
        results = []
        output_path = Path(output_dir) if output_dir else Path.cwd() / "audio"
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, line in enumerate(lines):
            try:
                emotion = emotions[0] if emotions else self._detect_emotion(line)
                
                audio = await self.generate_dialogue(
                    text=line["text"],
                    voice=voice,
                    emotion=emotion,
                    provider=provider,
                    **kwargs
                )
                
                # Save to disk
                filename = f"line_{i+1:04d}.{audio.format}"
                local_path = output_path / filename
                with open(local_path, "wb") as f:
                    f.write(audio.audio_data)
                audio.local_path = str(local_path)
                
                results.append(audio)
                
            except Exception as e:
                print(f"Failed to generate line {i+1}: {e}")
                continue
        
        return results
    
    def _parse_script(self, script: str) -> List[Dict]:
        """Parse dialogue script."""
        lines = []
        for line in script.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            
            # Parse emotion tag and dialogue
            if line.startswith("[") and "]":
                end_tag = line.index("]")
                emotion = line[1:end_tag]
                dialogue = line[end_tag+1:].strip()
                lines.append({"emotion": emotion, "text": dialogue})
            else:
                lines.append({"emotion": "neutral", "text": line})
        
        return lines
    
    def _detect_emotion(self, text: str) -> Emotion:
        """Detect emotion from text."""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["！", "!", "开心", "高兴", "太好了"]):
            return Emotion.HAPPY
        elif any(w in text_lower for w in ["哭", "悲伤", "难过", "唉"]):
            return Emotion.SAD
        elif any(w in text_lower for w in ["生气", "怒", "可恶"]):
            return Emotion.ANGRY
        elif any(w in text_lower for w in ["哇", "啊", "什么", "惊讶"]):
            return Emotion.SURPRISED
        else:
            return Emotion.NEUTRAL
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function
async def generate_voice(
    text: str,
    voice: str = "young_female",
    emotion: str = "neutral",
    provider: str = "auto",
    **kwargs
) -> GeneratedAudio:
    """Quick voice generation function."""
    async with AnimeVoiceGenerator() as generator:
        return await generator.generate_dialogue(
            text=text,
            voice=voice,
            emotion=Emotion(emotion),
            provider=Provider(provider),
            **kwargs
        )


if __name__ == "__main__":
    import sys
    
    async def main():
        if len(sys.argv) < 2:
            print("Usage: python voice_generator.py <text>")
            return
        
        text = sys.argv[1]
        voice = sys.argv[2] if len(sys.argv) > 2 else "young_female"
        emotion = sys.argv[3] if len(sys.argv) > 3 else "neutral"
        
        print(f"Generating: {text}")
        print(f"Voice: {voice}, Emotion: {emotion}")
        
        try:
            result = await generate_voice(
                text=text,
                voice=voice,
                emotion=emotion
            )
            
            print(f"Generated {result.format} audio from {result.provider.value}")
            print(f"Duration: {result.duration:.2f}s")
            
            output_path = Path("output.mp3")
            with open(output_path, "wb") as f:
                f.write(result.audio_data)
            print(f"Saved to {output_path}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    asyncio.run(main())
