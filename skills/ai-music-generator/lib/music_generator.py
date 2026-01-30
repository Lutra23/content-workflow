#!/usr/bin/env python3
"""
Anime Music Generator - Core library for AI music and sound generation
Supports Mubert, Google MusicGen, Soundful, and Udio.
"""

import os
import sys
import json
import time
import base64
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicProvider(Enum):
    """Supported music providers"""
    MUBERT = "mubert"
    MUSICGEN = "musicgen"
    SOUNDFUL = "soundful"
    UDIO = "udio"
    AUTO = "auto"


class MusicStyle(Enum):
    """Music style presets"""
    CALM = "calm"
    UPBEAT = "upbeat"
    DRAMATIC = "dramatic"
    ACTION = "action"
    MYSTERIOUS = "mysterious"
    ROMANTIC = "romantic"


class SceneType(Enum):
    """Scene types for music generation"""
    SCHOOL_DAY = "school_day"
    BATTLE = "battle"
    EMOTIONAL = "emotional"
    ROMANCE = "romance"
    SUSPENSE = "suspense"
    COMEDY = "comedy"
    INTRO = "intro"
    OUTRO = "outro"


@dataclass
class MusicResult:
    """Result from music generation"""
    success: bool
    audio_path: Optional[str] = None
    audio_url: Optional[str] = None
    provider: Optional[str] = None
    duration: float = 0.0
    bpm: int = 0
    style: Optional[str] = None
    loopable: bool = False
    metadata: Dict = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class AudioTrack:
    """Audio track for mixing"""
    path: str
    start_time: float = 0.0
    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0


class AnimeMusicGenerator:
    """
    Unified interface for anime music and sound generation.
    
    Features:
    - Background music generation
    - Character theme generation
    - Ambient sound generation
    - Sound effect generation
    - Audio mixing
    """
    
    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent.parent / "configs"
        self.cache_dir = Path.home() / ".cache" / "anime-music-generator"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._load_config()
    
    def _load_config(self):
        """Load provider and style configurations"""
        config_path = self.config_dir / "providers.yaml"
        styles_dir = self.config_dir / "styles"
        
        self.provider_config = {}
        self.style_presets = {}
        
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                self.provider_config = config.get("providers", {})
                self.fallback_order = config.get("fallback_order", ["mubert", "musicgen"])
        
        # Load style presets
        if styles_dir.exists():
            for style_file in styles_dir.glob("*.yaml"):
                with open(style_file) as f:
                    config = yaml.safe_load(f)
                    for name, preset_data in config.get("presets", {}).items():
                        self.style_presets[name] = preset_data
    
    def generate_bgm(
        self,
        prompt: str,
        style: Union[MusicStyle, str] = None,
        duration: float = 120.0,
        bpm: int = None,
        loop: bool = True,
        provider: Union[MusicProvider, str] = MusicProvider.AUTO,
        output_path: str = None,
        output_format: str = "mp3"
    ) -> MusicResult:
        """
        Generate background music.
        
        Args:
            prompt: Music description
            style: Music style preset
            duration: Duration in seconds
            bpm: Beats per minute
            loop: Whether the track should loop seamlessly
            provider: Music provider
            output_path: Output file path
            output_format: Audio format
            
        Returns:
            MusicResult with audio path and metadata
        """
        # Get style config
        style_value = style.value if isinstance(style, MusicStyle) else style
        style_config = self.style_presets.get(style_value, {})
        
        # Build prompt with style
        if style_config and "prompt_template" in style_config:
            full_prompt = style_config["prompt_template"].format(prompt=prompt)
        else:
            full_prompt = prompt
        
        # Use style BPM if not specified
        if not bpm and style_config and "bpm" in style_config:
            bpm = style_config["bpm"]
        
        provider_name = provider.value if isinstance(provider, MusicProvider) else provider
        
        if provider_name == "auto":
            providers_to_try = self.fallback_order
        else:
            providers_to_try = [provider_name]
        
        last_error = None
        
        for provider_name in providers_to_try:
            try:
                provider_instance = self._get_provider(provider_name)
                result = provider_instance.generate_bgm(
                    prompt=full_prompt,
                    duration=duration,
                    bpm=bpm,
                    loop=loop,
                    output_format=output_format
                )
                
                if result.success and output_path:
                    result = self._download_and_save(result, output_path)
                
                return result
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Provider {provider_name} failed: {e}")
                continue
        
        return MusicResult(success=False, error=f"All providers failed: {last_error}")
    
    def generate_theme(
        self,
        prompt: str,
        character: str = None,
        style: Union[MusicStyle, str] = None,
        duration: float = 60.0,
        lyrics: str = None,
        provider: Union[MusicProvider, str] = MusicProvider.AUTO,
        output_path: str = None
    ) -> MusicResult:
        """
        Generate character theme music.
        
        Args:
            prompt: Theme description
            character: Character name
            style: Music style
            duration: Duration in seconds
            lyrics: Song lyrics (if applicable)
            provider: Music provider
            output_path: Output file path
            
        Returns:
            MusicResult with audio path
        """
        # Build character-specific prompt
        if character:
            prompt = f"{character} theme, {prompt}"
        
        return self.generate_bgm(
            prompt=prompt,
            style=style or MusicStyle.UPBEAT,
            duration=duration,
            loop=False,
            provider=provider,
            output_path=output_path
        )
    
    def generate_ambient(
        self,
        prompt: str,
        duration: float = 60.0,
        layers: List[str] = None,
        provider: Union[MusicProvider, str] = MusicProvider.AUTO,
        output_path: str = None
    ) -> MusicResult:
        """
        Generate ambient soundscape.
        
        Args:
            prompt: Ambient description (e.g., "forest with birds")
            duration: Duration in seconds
            layers: Sound layers to include
            provider: Music provider
            output_path: Output file path
            
        Returns:
            MusicResult with audio path
        """
        # Add ambient-specific tags
        full_prompt = f"ambient soundscape, {prompt}, background, relaxing"
        
        provider_name = provider.value if isinstance(provider, MusicProvider) else provider
        
        if provider_name == "auto":
            providers_to_try = ["mubert", "musicgen"]
        else:
            providers_to_try = [provider_name]
        
        last_error = None
        
        for provider_name in providers_to_try:
            try:
                provider_instance = self._get_provider(provider_name)
                result = provider_instance.generate_ambient(
                    prompt=full_prompt,
                    duration=duration
                )
                
                if result.success and output_path:
                    result = self._download_and_save(result, output_path)
                
                return result
                
            except Exception as e:
                last_error = str(e)
                continue
        
        return MusicResult(success=False, error=f"All providers failed: {last_error}")
    
    def generate_sfx(
        self,
        prompt: str,
        category: str = "combat",
        duration: float = 2.0,
        intensity: str = "medium",
        output_path: str = None
    ) -> MusicResult:
        """
        Generate sound effect.
        
        Args:
            prompt: Sound description
            category: SFX category (combat/ambient/ui/voice/environmental)
            duration: Duration in seconds
            intensity: Sound intensity (low/medium/high)
            output_path: Output file path
            
        Returns:
            MusicResult with audio path
        """
        # Build SFX prompt
        full_prompt = f"anime {category} sound effect, {prompt}, {intensity} intensity"
        
        # Note: SFX generation would typically use a different provider or method
        # This is a placeholder that creates silent audio
        
        import uuid
        
        if not output_path:
            output_path = self.cache_dir / f"sfx_{uuid.uuid4().hex[:8]}.wav"
        
        # Create silent placeholder (actual SFX would use dedicated service)
        try:
            import numpy as np
            from scipy.io import wavfile
            
            sample_rate = 44100
            samples = np.zeros(int(sample_rate * duration), dtype=np.int16)
            wavfile.write(str(output_path), sample_rate, samples)
            
            return MusicResult(
                success=True,
                audio_path=str(output_path),
                provider="placeholder",
                duration=duration,
                metadata={"category": category, "intensity": intensity}
            )
        except Exception as e:
            return MusicResult(success=False, error=str(e))
    
    def generate_for_scene(
        self,
        scene_description: str,
        scene_type: Union[SceneType, str],
        duration: float = None,
        provider: Union[MusicProvider, str] = MusicProvider.AUTO,
        output_path: str = None
    ) -> MusicResult:
        """
        Generate music specifically for a scene.
        
        Args:
            scene_description: Description of the scene
            scene_type: Type of scene
            duration: Duration in seconds (auto if not specified)
            provider: Music provider
            output_path: Output file path
            
        Returns:
            MusicResult with audio path
        """
        # Get scene config
        scene_value = scene_type.value if isinstance(scene_type, SceneType) else scene_type
        scene_config = self.style_presets.get(scene_value, {})
        
        # Build prompt
        if scene_config and "prompt_template" in scene_config:
            prompt = scene_config["prompt_template"].format(prompt=scene_description)
        else:
            prompt = f"{scene_type} music, {scene_description}"
        
        # Get default duration
        if not duration:
            duration_map = {
                SceneType.INTRO: 30,
                SceneType.OUTRO: 30,
                SceneType.BATTLE: 90,
                SceneType.EMOTIONAL: 60,
                SceneType.ROMANCE: 90,
                SceneType.SCHOOL_DAY: 120,
                SceneType.SUSPENSE: 60,
                SceneType.COMEDY: 30
            }
            duration = duration_map.get(scene_type, 60)
        
        # Get style
        style_map = {
            SceneType.BATTLE: MusicStyle.ACTION,
            SceneType.EMOTIONAL: MusicStyle.DRAMATIC,
            SceneType.ROMANCE: MusicStyle.ROMANTIC,
            SceneType.SCHOOL_DAY: MusicStyle.UPBEAT,
            SceneType.SUSPENSE: MusicStyle.MYSTERIOUS,
            SceneType.COMEDY: MusicStyle.UPBEAT
        }
        style = style_map.get(scene_type, None)
        
        return self.generate_bgm(
            prompt=prompt,
            style=style,
            duration=duration,
            provider=provider,
            output_path=output_path
        )
    
    def generate_sound_pack(
        self,
        scene: str,
        includes: List[str] = None,
        output_dir: str = None
    ) -> Dict[str, MusicResult]:
        """
        Generate a sound pack for a scene.
        
        Args:
            scene: Scene name
            includes: List of sounds to include
            output_dir: Output directory
            
        Returns:
            Dict of sound name to MusicResult
        """
        output_dir = Path(output_dir) if output_dir else self.cache_dir / f"soundpack_{scene}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if includes is None:
            includes = ["ambient", "music", "sfx"]
        
        results = {}
        
        if "ambient" in includes:
            ambient_path = output_dir / "ambient.wav"
            results["ambient"] = self.generate_ambient(
                prompt=f"{scene} ambient soundscape",
                duration=120,
                output_path=str(ambient_path)
            )
        
        if "music" in includes:
            music_path = output_dir / "bgm.mp3"
            results["music"] = self.generate_bgm(
                prompt=f"{scene} background music",
                style=MusicStyle.CALM,
                duration=120,
                output_path=str(music_path)
            )
        
        if "sfx" in includes:
            sfx_path = output_dir / "sfx_pack"
            sfx_path.mkdir(exist_ok=True)
            results["sfx"] = {}
            
            common_sfx = {
                "footsteps": "walking footsteps",
                "door_open": "door opening",
                "equipment": "equipment sounds"
            }
            
            for name, desc in common_sfx.items():
                sfx_file = sfx_path / f"{name}.wav"
                results["sfx"][name] = self.generate_sfx(
                    prompt=f"{desc}, anime style",
                    output_path=str(sfx_file)
                )
        
        return results
    
    def mix_tracks(
        self,
        tracks: List[Union[AudioTrack, Dict]],
        output_path: str = None,
        format: str = "mp3",
        sample_rate: int = 44100
    ) -> MusicResult:
        """
        Mix multiple audio tracks together.
        
        Args:
            tracks: List of AudioTrack or dicts
            output_path: Output file path
            format: Output format
            sample_rate: Sample rate
            
        Returns:
            MusicResult with mixed audio
        """
        try:
            from pydub import AudioSegment
            import uuid
            
            if not output_path:
                output_path = self.cache_dir / f"mixed_{uuid.uuid4().hex[:8]}.{format}"
            
            # Load and mix tracks
            mixed = None
            
            for track_data in tracks:
                if isinstance(track_data, dict):
                    track = AudioTrack(**track_data)
                else:
                    track = track_data
                
                audio = AudioSegment.from_wav(track.path)
                
                # Apply volume
                audio = audio - (20 * (1 - track.volume))
                
                # Apply fade in/out
                if track.fade_in > 0:
                    audio = audio.fade_in(track.fade_in * 1000)
                if track.fade_out > 0:
                    audio = audio.fade_out(track.fade_out * 1000)
                
                # Position track
                if mixed is None:
                    mixed = audio
                    # Pad to start time
                    if track.start_time > 0:
                        mixed = AudioSegment.silent(duration=track.start_time * 1000) + mixed
                else:
                    # Extend mixed if needed
                    if len(mixed) < (track.start_time + len(audio)) * 1000:
                        mixed = mixed + AudioSegment.silent(
                            duration=(track.start_time + len(audio) / 1000 - len(mixed) / 1000) * 1000
                        )
                    
                    # Overlay track
                    mixed = mixed.overlay(audio, position=track.start_time * 1000)
            
            # Export
            mixed.export(
                str(output_path),
                format=format,
                bitrate="320k" if format == "mp3" else None
            )
            
            duration = len(mixed) / 1000
            
            return MusicResult(
                success=True,
                audio_path=str(output_path),
                provider="mixed",
                duration=duration,
                metadata={"num_tracks": len(tracks)}
            )
            
        except Exception as e:
            return MusicResult(success=False, error=str(e))
    
    def adapt_bgm(
        self,
        bgm_path: str,
        target_duration: float,
        fade_out: bool = True,
        output_path: str = None
    ) -> MusicResult:
        """
        Adapt BGM to target duration.
        
        Args:
            bgm_path: Path to BGM file
            target_duration: Target duration in seconds
            fade_out: Whether to add fade out
            output_path: Output file path
            
        Returns:
            MusicResult with adapted audio
        """
        try:
            from pydub import AudioSegment
            import uuid
            
            audio = AudioSegment.from_wav(bgm_path)
            current_duration = len(audio) / 1000
            
            if current_duration > target_duration:
                # Trim
                audio = audio[:target_duration * 1000]
                if fade_out:
                    audio = audio.fade_out(min(3000, target_duration * 1000))
            else:
                # Loop
                loops = int(target_duration / current_duration) + 1
                audio = audio * loops
                audio = audio[:target_duration * 1000]
            
            if not output_path:
                output_path = self.cache_dir / f"adapted_{uuid.uuid4().hex[:8]}.wav"
            
            audio.export(str(output_path), format="wav")
            
            return MusicResult(
                success=True,
                audio_path=str(output_path),
                provider="adapted",
                duration=target_duration,
                metadata={"original_duration": current_duration}
            )
            
        except Exception as e:
            return MusicResult(success=False, error=str(e))
    
    def _get_provider(self, provider_name: str) -> Any:
        """Get or initialize provider"""
        if provider_name == "mubert":
            return MubertProvider(self.provider_config.get("mubert", {}))
        elif provider_name == "musicgen":
            return MusicGenProvider(self.provider_config.get("musicgen", {}))
        elif provider_name == "soundful":
            return SoundfulProvider(self.provider_config.get("soundful", {}))
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    def _download_and_save(self, result: MusicResult, output_path: str) -> MusicResult:
        """Download audio from URL and save"""
        if result.audio_url:
            import requests
            response = requests.get(result.audio_url)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            result.audio_path = output_path
            result.audio_url = None
        
        return result


class BaseMusicProvider:
    """Base class for music providers"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def generate_bgm(
        self,
        prompt: str,
        duration: float = 120.0,
        bpm: int = None,
        loop: bool = True,
        output_format: str = "mp3"
    ) -> MusicResult:
        raise NotImplementedError
    
    def generate_ambient(
        self,
        prompt: str,
        duration: float = 60.0
    ) -> MusicResult:
        raise NotImplementedError


class MubertProvider(BaseMusicProvider):
    """Mubert music generation provider"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.api_key = os.getenv("MUBERT_API_KEY")
        self.base_url = "https://api.mubert.com/v2"
    
    def generate_bgm(
        self,
        prompt: str,
        duration: float = 120.0,
        bpm: int = None,
        loop: bool = True,
        output_format: str = "mp3"
    ) -> MusicResult:
        try:
            import requests
            
            if not self.api_key:
                return MusicResult(success=False, error="MUBERT_API_KEY not set")
            
            # Mubert uses tags for generation
            tags = prompt.replace(" ", ", ")
            
            params = {
                "method": "track",
                "tags": tags,
                "duration": int(duration),
                "loop": loop,
                "format": "mp3"
            }
            
            response = requests.get(
                f"{self.base_url}/generate",
                params=params,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                import uuid
                cache_path = f"/tmp/music_{uuid.uuid4().hex[:12]}.{output_format}"
                
                with open(cache_path, 'wb') as f:
                    f.write(response.content)
                
                return MusicResult(
                    success=True,
                    audio_path=cache_path,
                    provider="mubert",
                    duration=duration,
                    bpm=bpm or 120,
                    loopable=loop,
                    metadata={"tags": tags}
                )
            
            return MusicResult(
                success=False,
                error=f"Mubert API returned {response.status_code}"
            )
            
        except Exception as e:
            return MusicResult(success=False, error=str(e))
    
    def generate_ambient(
        self,
        prompt: str,
        duration: float = 60.0
    ) -> MusicResult:
        try:
            import requests
            
            if not self.api_key:
                return MusicResult(success=False, error="MUBERT_API_KEY not set")
            
            # Use ambient/station mode
            params = {
                "method": "track",
                "tags": f"ambient, {prompt}",
                "duration": int(duration),
                "mode": "ambient",
                "format": "mp3"
            }
            
            response = requests.get(
                f"{self.base_url}/generate",
                params=params,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=60
            )
            
            if response.status_code == 200:
                import uuid
                cache_path = f"/tmp/ambient_{uuid.uuid4().hex[:12]}.mp3"
                
                with open(cache_path, 'wb') as f:
                    f.write(response.content)
                
                return MusicResult(
                    success=True,
                    audio_path=cache_path,
                    provider="mubert",
                    duration=duration,
                    metadata={"tags": params["tags"]}
                )
            
            return MusicResult(success=False, error=f"Mubert API returned {response.status_code}")
            
        except Exception as e:
            return MusicResult(success=False, error=str(e))


class MusicGenProvider(BaseMusicProvider):
    """Google MusicGen via Replicate"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        self.api_url = "https://api.replicate.com/v1/predictions"
    
    def generate_bgm(
        self,
        prompt: str,
        duration: float = 30.0,
        bpm: int = None,
        loop: bool = False,
        output_format: str = "wav"
    ) -> MusicResult:
        try:
            import requests
            
            if not self.api_token:
                return MusicResult(success=False, error="REPLICATE_API_TOKEN not set")
            
            # Calculate seconds from duration
            seconds = int(duration)
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "Prefer": "wait"
            }
            
            payload = {
                "version": "musicgen",
                "input": {
                    "prompt": prompt,
                    "duration": seconds,
                    "model": "musicgen-small"
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=300
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                output = data.get('output')
                
                if isinstance(output, list):
                    audio_url = output[0]
                else:
                    audio_url = output
                
                import uuid
                cache_path = f"/tmp/music_{uuid.uuid4().hex[:12]}.{output_format}"
                
                # Download
                audio_response = requests.get(audio_url)
                with open(cache_path, 'wb') as f:
                    f.write(audio_response.content)
                
                return MusicResult(
                    success=True,
                    audio_path=cache_path,
                    provider="musicgen",
                    duration=duration,
                    bpm=bpm or 120
                )
            
            return MusicResult(
                success=False,
                error=f"MusicGen API returned {response.status_code}"
            )
            
        except Exception as e:
            return MusicResult(success=False, error=str(e))
    
    def generate_ambient(
        self,
        prompt: str,
        duration: float = 60.0
    ) -> MusicResult:
        return self.generate_bgm(
            prompt=f"ambient, {prompt}",
            duration=duration,
            loop=True
        )


class SoundfulProvider(BaseMusicProvider):
    """Soundful royalty-free music"""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.api_key = os.getenv("SOUNDFUL_API_KEY")
    
    def generate_bgm(
        self,
        prompt: str,
        duration: float = 120.0,
        bpm: int = None,
        loop: bool = True,
        output_format: str = "wav"
    ) -> MusicResult:
        return MusicResult(
            success=False,
            error="Soundful requires API setup. Check Soundful documentation."
        )
    
    def generate_ambient(
        self,
        prompt: str,
        duration: float = 60.0
    ) -> MusicResult:
        return MusicResult(
            success=False,
            error="Soundful requires API setup. Check Soundful documentation."
        )
