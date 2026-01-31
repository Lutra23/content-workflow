"""
AI Image Generator - Core Module

Unified interface for multiple AI image generation providers:
- Stable Diffusion (local/API)
- DALL-E 3 (OpenAI)
- Flux (Replicate)
- Midjourney (Discord)
"""

import os
import json
import base64
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import yaml


class Provider(Enum):
    """Supported image generation providers."""
    STABLE_DIFFUSION = "stable-diffusion"
    DALL_E = "dall-e"
    FLUX = "flux"
    MIDJOURNEY = "midjourney"
    KLING = "kling"
    AUTO = "auto"


class QualityMode(Enum):
    """Quality modes for image generation."""
    DRAFT = "draft"
    FAST = "fast"
    HIGH = "high"


class ImageType(Enum):
    """Types of images for anime production."""
    CHARACTER = "character"
    BACKGROUND = "background"
    PROP = "prop"
    EFFECT = "effect"
    SCENE = "scene"


@dataclass
class GenerationParams:
    """Parameters for image generation."""
    prompt: str
    negative_prompt: str = ""
    size: Tuple[int, int] = (1024, 1024)
    num_images: int = 1
    style: str = "anime"
    quality: str = "high"
    seed: Optional[int] = None
    guidance_scale: float = 7.5
    steps: int = 30
    provider: Provider = Provider.AUTO


@dataclass
class GeneratedImage:
    """Result of image generation."""
    image_data: bytes  # Base64 encoded or raw bytes
    format: str  # png, jpg, etc.
    provider: Provider
    seed: Optional[int]
    metadata: Dict[str, Any]
    local_path: Optional[str] = None


class ImageGeneratorError(Exception):
    """Base exception for image generation errors."""
    pass


class ProviderNotAvailableError(ImageGeneratorError):
    """Raised when a provider is not available or not configured."""
    pass


class RateLimitError(ImageGeneratorError):
    """Raised when rate limit is exceeded."""
    pass


class AnimeImageGenerator:
    """
    Unified AI image generator for anime/cartoon production.
    
    Usage:
        generator = AnimeImageGenerator()
        result = generator.generate_character("cute anime girl with blue hair")
        result = generator.generate_background("cherry blossom park")
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the image generator with configuration."""
        self.config = self._load_config(config_path)
        self.session = None
        self._provider_cache = {}
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration from file or use defaults."""
        if config_path is None:
            config_path = os.environ.get(
                "AI_IMAGE_GEN_CONFIG",
                Path(__file__).parent / "configs" / "providers.yaml"
            )
        
        default_config = {
            "primary_provider": "stable-diffusion",
            "fallback_order": ["stable-diffusion", "flux", "dall-e", "midjourney", "kling"],
            "providers": {
                "stable-diffusion": {
                    "api_url": os.environ.get("SD_API_URL", "http://localhost:7860"),
                    "model": "anime-full-res",
                    "enabled": True
                },
                "dall-e": {
                    "api_url": "https://api.openai.com/v1",
                    "model": "dall-e-3",
                    "enabled": bool(os.environ.get("OPENAI_API_KEY"))
                },
                "flux": {
                    "api_url": "https://api.replicate.com/v1",
                    "model": "flux-anime",
                    "enabled": bool(os.environ.get("REPLICATE_API_TOKEN"))
                },
                "midjourney": {
                    "api_url": "https://discord.com/api/v10",
                    "enabled": bool(os.environ.get("MIDJOURNEY_DISCORD_TOKEN"))
                },
                "kling": {
                    "api_url": "https://api.klingai.com/v1",
                    "enabled": bool(os.environ.get("KLING_API_KEY"))
                }
            },
            "rate_limits": {
                "dall-e": {"rpm": 50, "images_per_request": 1},
                "flux": {"rpm": 30, "images_per_request": 1},
                "stable-diffusion": {"rpm": 100, "images_per_request": 4}
            },
            "style_presets": self._default_style_presets()
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
            # Merge configs
            default_config.update(user_config)
            
        return default_config
    
    def _default_style_presets(self) -> Dict:
        """Default anime style presets."""
        return {
            "standard_anime": {
                "prompt_template": "masterpiece, best quality, anime style, {prompt}, detailed illustration, beautiful eyes, vibrant colors",
                "negative_prompt": "low quality, worst quality, blurry, bad anatomy, bad hands, extra limbs",
                "default_size": [1024, 1024]
            },
            "soft_anime": {
                "prompt_template": "soft anime style, {prompt}, pastel colors, gentle lighting, romantic atmosphere, soft shadows",
                "negative_prompt": "dark, gritty, realistic, harsh lighting, high contrast",
                "default_size": [1024, 1024]
            },
            "action_anime": {
                "prompt_template": "dynamic anime action scene, {prompt}, dramatic lighting, fast motion blur, intense atmosphere, impact effects",
                "negative_prompt": "static, calm, peaceful, slow, gentle",
                "default_size": [1280, 720]
            },
            "cinematic": {
                "prompt_template": "cinematic anime, {prompt}, dramatic composition, film grain, movie poster style, professional lighting",
                "negative_prompt": "amateur, low quality, static pose, bad composition",
                "default_size": [1920, 1080]
            }
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=120)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def _format_prompt(self, prompt: str, style: str = "anime") -> str:
        """Format prompt with style preset."""
        presets = self.config.get("style_presets", {})
        if style in presets:
            template = presets[style]["prompt_template"]
            return template.format(prompt=prompt)
        return prompt
    
    def _format_negative_prompt(self, style: str = "anime") -> str:
        """Get negative prompt for style."""
        presets = self.config.get("style_presets", {})
        if style in presets:
            return presets[style].get("negative_prompt", "")
        return ""
    
    async def generate_character(
        self,
        prompt: str,
        style: str = "standard_anime",
        size: Tuple[int, int] = (1024, 1024),
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> GeneratedImage:
        """
        Generate anime character image.
        
        Args:
            prompt: Character description
            style: Style preset name
            size: Output image size (width, height)
            provider: Specific provider or AUTO for auto-selection
            
        Returns:
            GeneratedImage object
        """
        params = GenerationParams(
            prompt=prompt,
            size=size,
            style=style,
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def generate_background(
        self,
        scene_description: str,
        style: str = "standard_anime",
        perspective: str = "perspective",
        size: Tuple[int, int] = (1920, 1080),
        provider: Provider = Provider.AUTO,
        **kwargs
    ) -> GeneratedImage:
        """
        Generate background scene image.
        
        Args:
            scene_description: Scene description
            style: Style preset
            perspective: Perspective type (perspective, top-down, side)
            size: Output size
            provider: Provider selection
            
        Returns:
            GeneratedImage object
        """
        # Enhance background prompt
        enhanced_prompt = f"{scene_description}, {perspective} view, detailed environment, proper perspective"
        
        params = GenerationParams(
            prompt=enhanced_prompt,
            size=size,
            style=style,
            provider=provider,
            **kwargs
        )
        return await self._generate(params)
    
    async def _generate(self, params: GenerationParams) -> GeneratedImage:
        """Internal generation method with provider fallback."""
        providers = self._get_provider_order(params.provider)
        
        last_error = None
        for provider in providers:
            try:
                if provider == Provider.STABLE_DIFFUSION:
                    return await self._generate_stable_diffusion(params)
                elif provider == Provider.DALL_E:
                    return await self._generate_dalle(params)
                elif provider == Provider.FLUX:
                    return await self._generate_flux(params)
                elif provider == Provider.MIDJOURNEY:
                    return await self._generate_midjourney(params)
                elif provider == Provider.KLING:
                    return await self._generate_kling(params)
            except ProviderNotAvailableError as e:
                last_error = e
                continue
            except Exception as e:
                last_error = e
                continue
        
        raise ImageGeneratorError(f"All providers failed: {last_error}")
    
    def _get_provider_order(self, provider: Provider) -> List[Provider]:
        """Get ordered list of providers to try."""
        if provider != Provider.AUTO:
            return [provider]
        
        fallbacks = self.config.get("fallback_order", [])
        return [Provider(p) for p in fallbacks]
    
    async def _generate_stable_diffusion(self, params: GenerationParams) -> GeneratedImage:
        """Generate image using Stable Diffusion."""
        config = self.config["providers"]["stable-diffusion"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Stable Diffusion not enabled")
        
        api_url = config["api_url"]
        
        payload = {
            "prompt": self._format_prompt(params.prompt, params.style),
            "negative_prompt": params.negative_prompt or self._format_negative_prompt(params.style),
            "width": params.size[0],
            "height": params.size[1],
            "steps": params.steps,
            "cfg_scale": params.guidance_scale,
            "sampler_name": "Euler a",
            "seed": params.seed or -1,
            "batch_size": params.num_images
        }
        
        session = await self._get_session()
        async with session.post(f"{api_url}/sdapi/v1/txt2img", json=payload) as response:
            if response.status == 429:
                raise RateLimitError("Stable Diffusion rate limit exceeded")
            if response.status != 200:
                raise ImageGeneratorError(f"Stable Diffusion error: {await response.text()}")
            
            result = await response.json()
            images = result.get("images", [])
            
            if not images:
                raise ImageGeneratorError("No images generated")
            
            image_data = base64.b64decode(images[0])
            
            return GeneratedImage(
                image_data=image_data,
                format="png",
                provider=Provider.STABLE_DIFFUSION,
                seed=result.get("seed"),
                metadata={"model": config.get("model", "unknown")}
            )
    
    async def _generate_dalle(self, params: GenerationParams) -> GeneratedImage:
        """Generate image using DALL-E 3."""
        config = self.config["providers"]["dall-e"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("DALL-E not enabled")
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ProviderNotAvailableError("OPENAI_API_KEY not set")
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.get("model", "dall-e-3"),
            "prompt": self._format_prompt(params.prompt, params.style),
            "size": f"{params.size[0]}x{params.size[1]}",
            "quality": params.quality,
            "n": params.num_images
        }
        
        async with session.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload
        ) as response:
            if response.status == 429:
                raise RateLimitError("DALL-E rate limit exceeded")
            if response.status != 200:
                raise ImageGeneratorError(f"DALL-E error: {await response.text()}")
            
            result = await response.json()
            image_url = result["data"][0]["url"]
            
            # Download the image
            async with session.get(image_url) as img_response:
                image_data = await img_response.read()
            
            return GeneratedImage(
                image_data=image_data,
                format="png",
                provider=Provider.DALL_E,
                seed=None,
                metadata={"model": payload["model"]}
            )
    
    async def _generate_flux(self, params: GenerationParams) -> GeneratedImage:
        """Generate image using Flux."""
        config = self.config["providers"]["flux"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Flux not enabled")
        
        api_key = os.environ.get("REPLICATE_API_TOKEN")
        if not api_key:
            raise ProviderNotAvailableError("REPLICATE_API_TOKEN not set")
        
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": self._format_prompt(params.prompt, params.style),
            "width": params.size[0],
            "height": params.size[1],
            "guidance": params.guidance_scale,
            "steps": params.steps
        }
        
        # Create prediction
        async with session.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json={"version": config.get("model", "flux-anime"), "input": payload}
        ) as response:
            if response.status != 201:
                raise ImageGeneratorError(f"Flux error: {await response.text()}")
            
            prediction = await response.json()
            
            # Poll for completion
            while prediction["status"] not in ["succeeded", "failed", "canceled"]:
                await asyncio.sleep(1)
                async with session.get(prediction["urls"]["get"], headers=headers) as poll_response:
                    prediction = await poll_response.json()
            
            if prediction["status"] != "succeeded":
                raise ImageGeneratorError(f"Flux generation failed: {prediction.get('error')}")
            
            output_url = prediction["output"]
            async with session.get(output_url) as img_response:
                image_data = await img_response.read()
            
            return GeneratedImage(
                image_data=image_data,
                format="png",
                provider=Provider.FLUX,
                seed=None,
                metadata={"model": config.get("model")}
            )
    
    async def _generate_midjourney(self, params: GenerationParams) -> GeneratedImage:
        """Generate image using Midjourney (via Discord)."""
        # Midjourney requires Discord bot interaction
        # This is a placeholder - actual implementation would need Discord bot setup
        raise ProviderNotAvailableError("Midjourney requires Discord bot setup - not yet implemented")
    
    async def _generate_kling(self, params: GenerationParams) -> GeneratedImage:
        """Generate image using Kling AI."""
        config = self.config["providers"]["kling"]
        if not config.get("enabled"):
            raise ProviderNotAvailableError("Kling not enabled")
        
        api_key = os.environ.get("KLING_API_KEY")
        if not api_key:
            raise ProviderNotAvailableError("KLING_API_KEY not set")
        
        # Placeholder for Kling API integration
        raise ProviderNotAvailableError("Kling integration - not yet implemented")
    
    async def batch_generate(
        self,
        prompts: List[str],
        style: str = "standard_anime",
        provider: Provider = Provider.AUTO,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> List[GeneratedImage]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts: List of prompts
            style: Style preset
            provider: Provider selection
            output_dir: Directory to save images
            
        Returns:
            List of GeneratedImage objects
        """
        results = []
        output_path = Path(output_dir) if output_dir else Path.cwd() / "generated"
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, prompt in enumerate(prompts):
            try:
                result = await self.generate_character(
                    prompt=prompt,
                    style=style,
                    provider=provider,
                    **kwargs
                )
                
                # Save to disk
                filename = f"image_{i+1:04d}.{result.format}"
                local_path = output_path / filename
                with open(local_path, "wb") as f:
                    f.write(result.image_data)
                result.local_path = str(local_path)
                
                results.append(result)
                
            except Exception as e:
                print(f"Failed to generate image {i+1}: {e}")
                continue
        
        return results
    
    async def close(self):
        """Close HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function
async def generate_anime_image(
    prompt: str,
    provider: str = "auto",
    style: str = "standard_anime",
    **kwargs
) -> GeneratedImage:
    """
    Quick image generation function.
    
    Usage:
        result = await generate_anime_image(
            prompt="cute anime girl with blue hair",
            provider="stable-diffusion",
            style="soft_anime"
        )
    """
    async with AnimeImageGenerator() as generator:
        return await generator.generate_character(
            prompt=prompt,
            provider=Provider(provider),
            style=style,
            **kwargs
        )


if __name__ == "__main__":
    import sys
    
    async def main():
        if len(sys.argv) < 2:
            print("Usage: python image_generator.py <prompt>")
            return
        
        prompt = sys.argv[1]
        provider = sys.argv[2] if len(sys.argv) > 2 else "auto"
        style = sys.argv[3] if len(sys.argv) > 3 else "standard_anime"
        
        print(f"Generating: {prompt}")
        print(f"Provider: {provider}, Style: {style}")
        
        try:
            result = await generate_anime_image(
                prompt=prompt,
                provider=provider,
                style=style
            )
            
            print(f"Generated {result.format} image from {result.provider.value}")
            print(f"Size: {len(result.image_data)} bytes")
            
            # Save to file
            output_path = Path("output.png")
            with open(output_path, "wb") as f:
                f.write(result.image_data)
            print(f"Saved to {output_path}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    asyncio.run(main())
