"""
AI Video Generator - Core Module

Unified interface for multiple AI video generation providers:
- Runway Gen-3
- Pika Labs
- Kling AI
- Luma Dream Machine
"""

import os
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import yaml
import base64


class Provider(Enum):
    """Supported video generation providers."""
    RUNWAY = "runway"
    PIKA = "pika"
    KLING = "kling"
    LUMA = "luma"
    AUTO = "auto"


# Alias for backward compatibility
VideoProvider = Provider


class MotionPreset(Enum):
    """Motion presets for anime video generation."""
    GENTLE = "gentle"
    DYNAMIC = "dynamic"
    CINEMATIC = "cinematic"
    DREAMY = "dreamy"


class CameraMotion(Enum):
    """Camera motion types."""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY = "dolly"
    SHAKE = "shake"


@dataclass
class VideoParams:
    """Parameters for video generation."""
    # Common
    prompt: str = ""
    image_path: Optional[str] = None
    duration: int = 5  # seconds
    style: str = "anime"
    motion_scale: float = 1.0
    motion_prompt: str = ""
    
    # Advanced
    camera_movement: str = "static"
    fps: int = 24
    aspect_ratio: str = "16:9"
    seed: Optional[int] = None
    
    # Provider selection
    provider: Provider = Provider.AUTO
    
    # Quality
    quality: str = "high"
    upscale: Optional[float] = None  # e.g., 2.0 for 2x upscale


@dataclass
class GeneratedVideo:
    """Result of video generation."""
    video_data: bytes
    format: str  # mp4, webm, etc.
    duration: float  # seconds
    fps: int
    resolution: Tuple[int, int]
    provider: Provider
    seed: Optional[int]
    metadata: Dict[str, Any]
    local_path: Optional[str] = None


class VideoGeneratorError(Exception):
    """Base exception for video generation errors."""
    pass


class ProviderNotAvailableError(VideoGeneratorError):
    """Raised when a provider is not available."""
    pass


class RateLimitError(VideoGeneratorError):
    """Raised when rate limit is exceeded."""
    pass


class GenerationTimeoutError(VideoGeneratorError):
    """Raised when generation times out."""
    pass


class AnimeVideoGenerator:
    """
    Unified AI video generator for anime/cartoon production.
    
    Usage:
        generator = AnimeVideoGenerator()
        video = await generator.generate_from_text("anime girl walking", duration=5)
        video = await generator.generate_from_image("pose.png", "walking motion", duration=4)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the video generator."""
        self.config = self._load_config(config_path)
        self.session = None
        self._active_generations = {}
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration."""
        if config_path is None:
            config_path = os.environ.get(
                "AI_VIDEO_GEN_CONFIG",
                Path(__file__).parent / "configs" / "providers.yaml"
            )
        
        default_config = {
            "primary_provider": "runway",
            "fallback_order": ["runway", "pika", "kling", "luma"],
            "providers": {
                "runway": {
                    "api_url": "https://api.runwayml.com/v1",
                    "max_duration": 10,
                    "enabled": bool(os.environ.get("RUNWAY_API_KEY"))
                },
                "pika": {
                    "api_url": "https://api.pika.art/v1",
                    "max_duration": 4,
                    "enabled": bool(os.environ.get("PIKA_API_KEY"))
                },
                "kling": {
                    "api_url": "https://api.klingai.com/v1",
                    "max_duration": 10,
                    "enabled": bool(os.environ.get("KLING_API_KEY"))
                },
                "luma": {
                    "api_url": "https://api.lumalabs.ai/v1",
                    "max_duration": 5,
                    "enabled": bool(os.environ.get("LUMA_API_KEY"))
                }
            },
            "rate_limits": {
                "runway": {"vpm": 2, "max_concurrent": 1},
                "pika": {"vpm": 5, "max_concurrent": 2},
                "kling": {"vpm": 3, "max_concurrent": 1},
                "luma": {"vpm": 10, "max_concurrent": 3}
            },
            "motion_presets": self._default_motion_presets()
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
            default_config.update(user_config)
        
        return default_config
    
    def _default_motion_presets(self) -> Dict:
        """Default motion presets."""
        return {
            "gentle": {
                "motion_template": "gentle, smooth motion, {motion}",
                "camera_movement": "static",
                "motion_scale": 0.5
            },
            "dynamic": {
                "motion_template": "dynamic action, {motion}, fast paced",
                "camera_movement": "shake",
                "motion_scale": 1.2
            },
            "cinematic": {
                "motion_template": "cinematic motion, {motion}",
                "camera_movement": "pan_left",
                "motion_scale": 0.8
            },
            "dreamy": {
                "motion_template": "dreamy atmosphere, {motion}, floating",
                "camera_movement": "static",
                "motion_scale": 0.3
            }
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=300)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def _format_motion_prompt(self, motion: str, style: str = "anime") -> str:
        """Format motion prompt with style preset."""
        presets = self.config.get("motion_presets", {})
        if style in presets:
            template = presets[style]["motion_template"]
            return template.format(motion=motion)
        return f"{style} style, {motion}"
    
    async def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,
        style: str = "anime",
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> GeneratedVideo:
        """
        Generate video from text prompt.
        
        Args:
            prompt: Text description of the video
            duration: Video duration in seconds
            style: Motion style preset
            provider: Specific provider or AUTO
            
        Returns:
            GeneratedVideo object
        """
        params = VideoParams(
            prompt=prompt,
            duration=duration,
            style=style,
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def generate_from_image(
        self,
        image_path: str,
        motion_prompt: str = "",
        duration: int = 4,
        style: str = "anime",
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> GeneratedVideo:
        """
        Generate video from static image.
        
        Args:
            image_path: Path to source image
            motion_prompt: Description of desired motion
            duration: Video duration in seconds
            style: Motion style preset
            provider: Specific provider or AUTO
            
        Returns:
            GeneratedVideo object
        """
        params = VideoParams(
            image_path=image_path,
            motion_prompt=motion_prompt,
            duration=duration,
            style=style,
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def _generate(self, params: VideoParams) -> GeneratedVideo:
        """Internal generation with provider fallback."""
        providers = self._get_provider_order(params.provider)
        
        last_error = None
        for provider in providers:
            try:
                if provider == Provider.RUNWAY:
                    return await self._generate_runway(params)
                elif provider == Provider.PIKA:
                    return await self._generate_pika(params)
                elif provider == Provider.KLING:
                    return await self._generate_kling(params)
                elif provider == Provider.LUMA:
                    return await self._generate_luma(params)
            except ProviderNotAvailableError as e:
                last_error = e
                continue
            except Exception as e:
                last_error = e
                continue
        
        raise VideoGeneratorError(f"All providers failed: {last_error}")
    
    def _get_provider_order(self, provider: Provider) -> List[Provider]:
        """Get ordered list of providers."""
        if provider != Provider.AUTO:
            return [provider]
        
        fallbacks = self.config.get("fallback_order", [])
        return [Provider(p) for p in fallbacks]
    
    async def _generate_runway(self, params: VideoParams) -> GeneratedVideo:
        """Generate video using Runway Gen-3."""
        config = self.config["providers"]["runway"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Runway not enabled")
        
        api_key = os.environ.get("RUNWAY_API_KEY")
        session = await self._get_session()
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Build payload
        payload = {
            "model": "gen3",
            "prompt": params.prompt,
            "duration": min(params.duration, config["max_duration"]),
            "aspect_ratio": params.aspect_ratio,
            "motion_bucket_id": int(params.motion_scale * 127)
        }
        
        # Add camera movement if specified
        if params.camera_movement != "static":
            payload["camera_motion"] = params.camera_movement
        
        # Start generation
        async with session.post(
            f"{config['api_url']}/generations/text-to-video",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 429:
                raise RateLimitError("Runway rate limit exceeded")
            if response.status != 201:
                error = await response.text()
                raise VideoGeneratorError(f"Runway error: {error}")
            
            generation = await response.json()
            gen_id = generation["id"]
        
        # Poll for completion
        result = await self._poll_runway(config, headers, gen_id)
        
        return result
    
    async def _poll_runway(self, config: Dict, headers: Dict, gen_id: str, timeout: int = 300) -> GeneratedVideo:
        """Poll Runway for generation completion."""
        session = await self._get_session()
        start_time = asyncio.get_event_loop().time()
        
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise GenerationTimeoutError("Video generation timed out")
            
            async with session.get(
                f"{config['api_url']}/generations/{gen_id}",
                headers=headers
            ) as response:
                if response.status != 200:
                    await asyncio.sleep(2)
                    continue
                
                generation = await response.json()
                
                if generation["status"] == "succeeded":
                    # Download video
                    video_url = generation["output"]["video_url"]
                    async with session.get(video_url) as r:
                        video_data = await r.read()
                    
                    resolution = (generation.get("width", 1280), generation.get("height", 768))
                    
                    return GeneratedVideo(
                        video_data=video_data,
                        format="mp4",
                        duration=generation.get("duration", 5),
                        fps=24,
                        resolution=resolution,
                        provider=Provider.RUNWAY,
                        seed=generation.get("seed"),
                        metadata={"model": "gen3"}
                    )
                
                elif generation["status"] == "failed":
                    raise VideoGeneratorError(f"Runway generation failed: {generation.get('error')}")
            
            await asyncio.sleep(3)
    
    async def _generate_pika(self, params: VideoParams) -> GeneratedVideo:
        """Generate video using Pika Labs."""
        config = self.config["providers"]["pika"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Pika not enabled")
        
        # Placeholder - Pika API integration
        raise ProviderNotAvailableError("Pika Labs integration - not yet implemented")
    
    async def _generate_kling(self, params: VideoParams) -> GeneratedVideo:
        """Generate video using Kling AI."""
        config = self.config["providers"]["kling"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Kling not enabled")
        
        api_key = os.environ.get("KLING_API_KEY")
        session = await self._get_session()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": params.prompt,
            "duration": params.duration,
            "aspect_ratio": params.aspect_ratio
        }
        
        # Placeholder - Kling API integration
        raise ProviderNotAvailableError("Kling integration - not yet fully implemented")
    
    async def _generate_luma(self, params: VideoParams) -> GeneratedVideo:
        """Generate video using Luma Dream Machine."""
        config = self.config["providers"]["luma"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Luma not enabled")
        
        # Placeholder - Luma API integration
        raise ProviderNotAvailableError("Luma Dream Machine integration - not yet implemented")
    
    async def extend_video(
        self,
        video_path: str,
        additional_seconds: float = 3,
        provider: Provider = Provider.AUTO
    ) -> GeneratedVideo:
        """Extend an existing video."""
        # Placeholder for video extension
        raise ProviderNotAvailableError("Video extension - not yet implemented")
    
    async def batch_generate(
        self,
        prompts: List[str],
        duration: int = 5,
        style: str = "anime",
        provider: Provider = Provider.AUTO,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> List[GeneratedVideo]:
        """Generate multiple videos from prompts."""
        results = []
        output_path = Path(output_dir) if output_dir else Path.cwd() / "videos"
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, prompt in enumerate(prompts):
            try:
                result = await self.generate_from_text(
                    prompt=prompt,
                    duration=duration,
                    style=style,
                    provider=provider,
                    **kwargs
                )
                
                # Save to disk
                filename = f"video_{i+1:04d}.{result.format}"
                local_path = output_path / filename
                with open(local_path, "wb") as f:
                    f.write(result.video_data)
                result.local_path = str(local_path)
                
                results.append(result)
                
            except Exception as e:
                print(f"Failed to generate video {i+1}: {e}")
                continue
        
        return results
    
    async def stream_progress(self, generation_id: str, provider: Provider) -> AsyncGenerator[Dict, None]:
        """Stream generation progress."""
        # Placeholder for progress streaming
        yield {"status": "starting", "progress": 0}
        await asyncio.sleep(2)
        yield {"status": "generating", "progress": 50}
        await asyncio.sleep(2)
        yield {"status": "complete", "progress": 100}
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function
async def generate_anime_video(
    prompt: str,
    duration: int = 5,
    provider: str = "auto",
    style: str = "anime",
    **kwargs
) -> GeneratedVideo:
    """Quick video generation function."""
    async with AnimeVideoGenerator() as generator:
        return await generator.generate_from_text(
            prompt=prompt,
            duration=duration,
            provider=Provider(provider),
            style=style,
            **kwargs
        )


if __name__ == "__main__":
    import sys
    
    async def main():
        if len(sys.argv) < 2:
            print("Usage: python video_generator.py <prompt>")
            return
        
        prompt = sys.argv[1]
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        provider = sys.argv[3] if len(sys.argv) > 3 else "auto"
        
        print(f"Generating video: {prompt}")
        print(f"Duration: {duration}s, Provider: {provider}")
        
        try:
            result = await generate_anime_video(
                prompt=prompt,
                duration=duration,
                provider=provider
            )
            
            print(f"Generated {result.format} video from {result.provider.value}")
            print(f"Duration: {result.duration}s, Resolution: {result.resolution}")
            
            output_path = Path("output.mp4")
            with open(output_path, "wb") as f:
                f.write(result.video_data)
            print(f"Saved to {output_path}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    asyncio.run(main())
