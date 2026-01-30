#!/usr/bin/env python3
"""
Anime Image Generator - Batch processing script
"""

import os
import sys
import argparse
from pathlib import Path
from lib.image_generator import AnimeImageGenerator, Provider, QualityMode, ImageType


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate anime images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from prompt file (one prompt per line)
  %(prog)s generate prompts.txt --output ./output --provider stable-diffusion
  
  # Generate character variations
  %(prog)s variations reference.png "angry,sad,happy" --style anime
  
  # Generate variations from character reference
  %(prog)s character-variants character_ref.json --poses "walking,running,sitting"
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Batch mode")
    
    # Generate mode
    gen_parser = subparsers.add_parser("generate", help="Generate from prompt file")
    gen_parser.add_argument("prompt_file", help="File with prompts (one per line)")
    gen_parser.add_argument("--output", "-o", default="./output", help="Output directory")
    gen_parser.add_argument("--style", default="anime", help="Style preset")
    gen_parser.add_argument("--type", default="character", choices=["character", "background", "prop", "effect"],
                          help="Image type")
    gen_parser.add_argument("--provider", default="auto", help="AI provider")
    gen_parser.add_argument("--quality", default="high", choices=["draft", "fast", "high"], help="Quality mode")
    gen_parser.add_argument("--parallel", type=int, default=1, help="Parallel generations")
    
    # Variations mode
    var_parser = subparsers.add_parser("variations", help="Generate variations of an image")
    var_parser.add_argument("reference_image", help="Reference image path")
    var_parser.add_argument("variations", help="Comma-separated variation descriptions")
    var_parser.add_argument("--style", default="anime", help="Style preset")
    var_parser.add_argument("--output", "-o", default="./variations", help="Output directory")
    var_parser.add_argument("--provider", default="auto", help="AI provider")
    
    # Character variants mode
    char_var_parser = subparsers.add_parser("character-variants", help="Generate character pose variations")
    char_var_parser.add_argument("reference", help="Reference file or character description")
    char_var_parser.add_argument("--poses", default="standing", help="Comma-separated poses")
    var_parser.add_argument("--expressions", help="Comma-separated expressions")
    var_parser.add_argument("--style", default="anime", help="Style preset")
    var_parser.add_argument("--output", "-o", default="./character_variants", help="Output directory")
    var_parser.add_argument("--provider", default="auto", help="AI provider")
    
    # From images mode
    img_parser = subparsers.add_parser("from-images", help="Process existing images (style transfer, etc.)")
    img_parser.add_argument("image_dir", help="Directory containing images")
    img_parser.add_argument("--prompt", help="Prompt for processing")
    img_parser.add_argument("--style", default="anime", help="Target style")
    img_parser.add_argument("--output", "-o", default="./processed", help="Output directory")
    img_parser.add_argument("--provider", default="stable-diffusion", help="AI provider")
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Parse provider
    provider_map = {
        "auto": Provider.AUTO,
        "stable-diffusion": Provider.STABLE_DIFFUSION,
        "dall-e": Provider.DALL_E,
        "flux": Provider.FLUX
    }
    provider = provider_map.get(args.provider.lower(), Provider.AUTO)
    quality = QualityMode(args.quality)
    
    # Initialize generator
    generator = AnimeImageGenerator()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.mode == "generate":
        # Load prompts from file
        prompt_file = Path(args.prompt_file)
        if not prompt_file.exists():
            print(f"❌ Prompt file not found: {prompt_file}")
            sys.exit(1)
        
        with open(prompt_file) as f:
            prompts = [line.strip() for line in f if line.strip()]
        
        print(f"📝 Loaded {len(prompts)} prompts from {prompt_file}")
        
        # Determine image type
        image_type_map = {
            "character": ImageType.CHARACTER,
            "background": ImageType.BACKGROUND,
            "prop": ImageType.PROP,
            "effect": ImageType.EFFECT
        }
        image_type = image_type_map.get(args.type, ImageType.CHARACTER)
        
        # Generate batch
        results = generator.batch_generate(
            prompts=prompts,
            style=args.style,
            image_type=image_type,
            provider=provider,
            quality=quality,
            output_dir=str(output_dir),
            parallel=args.parallel
        )
        
        # Summary
        success_count = sum(1 for r in results if r.success)
        print(f"\n✅ Generated {success_count}/{len(results)} images successfully")
        
        # Save detailed results
        results_file = output_dir / "results.json"
        with open(results_file, 'w') as f:
            json.dump([
                {
                    "success": r.success,
                    "prompt": r.prompt_used,
                    "path": r.image_path,
                    "provider": r.provider,
                    "error": r.error
                }
                for r in results
            ], f, indent=2, ensure_ascii=False)
        print(f"📄 Results saved to: {results_file}")
    
    elif args.mode == "variations":
        # Generate variations of reference image
        ref_image = Path(args.reference_image)
        if not ref_image.exists():
            print(f"❌ Reference image not found: {ref_image}")
            sys.exit(1)
        
        variations = [v.strip() for v in args.variations.split(',')]
        print(f"🎨 Generating {len(variations)} variations of {ref_image.name}")
        
        results = []
        for i, variation in enumerate(variations):
            output_file = output_dir / f"variation_{i:03d}_{variation}.png"
            
            # Note: Actual implementation would use img2img
            result = generator._generate(
                prompt=f"{variation}, anime style",
                image_type=ImageType.CHARACTER,
                provider=provider,
                output_path=str(output_file)
            )
            results.append(result)
            
            if result.success:
                print(f"  ✅ {variation}: {result.image_path}")
            else:
                print(f"  ❌ {variation}: {result.error}")
        
        success_count = sum(1 for r in results if r.success)
        print(f"\n✅ Generated {success_count}/{len(results)} variations successfully")
    
    elif args.mode == "character-variants":
        # Generate character pose variations
        if Path(args.reference).exists():
            # Load reference from file
            with open(args.reference) as f:
                reference = json.load(f)
        else:
            # Create new reference from description
            reference = generator.create_character_reference(
                prompt=args.reference
            )
        
        poses = [p.strip() for p in args.poses.split(',')]
        expressions = [e.strip() for e in args.expressions.split(',')] if args.expressions else ["neutral"]
        
        print(f"🎭 Generating {len(poses) * len(expressions)} character variants")
        print(f"   Base prompt: {reference['prompt']}")
        
        results = []
        for i, pose in enumerate(poses):
            for j, expr in enumerate(expressions):
                variant_desc = f"{pose}, {expr} expression"
                output_file = output_dir / f"pose_{i:03d}_{expr}.png"
                
                result = generator.generate_character_variant(
                    reference=reference,
                    variation=variant_desc,
                    output_path=str(output_file),
                    style=args.style,
                    provider=provider
                )
                results.append(result)
                
                if result.success:
                    print(f"  ✅ {variant_desc}: {result.image_path}")
                else:
                    print(f"  ❌ {variant_desc}: {result.error}")
        
        success_count = sum(1 for r in results if r.success)
        print(f"\n✅ Generated {success_count}/{len(results)} character variants successfully")
    
    elif args.mode == "from-images":
        # Process existing images
        image_dir = Path(args.image_dir)
        if not image_dir.exists():
            print(f"❌ Image directory not found: {image_dir}")
            sys.exit(1)
        
        images = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.jpeg"))
        print(f"🖼️ Found {len(images)} images in {image_dir}")
        
        results = []
        for i, image_path in enumerate(images):
            output_file = output_dir / f"processed_{image_path.stem}.png"
            
            # Note: Actual implementation would use img2img
            result = generator._generate(
                prompt=args.prompt or f"anime style {args.style}",
                image_type=ImageType.CHARACTER,
                provider=provider,
                output_path=str(output_file)
            )
            results.append(result)
            
            if result.success:
                print(f"  ✅ {image_path.name}: {result.image_path}")
            else:
                print(f"  ❌ {image_path.name}: {result.error}")
        
        success_count = sum(1 for r in results if r.success)
        print(f"\n✅ Processed {success_count}/{len(results)} images successfully")
    
    return 0


if __name__ == "__main__":
    import json
    sys.exit(main())
