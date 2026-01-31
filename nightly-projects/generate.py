#!/usr/bin/env python3
"""
Nightly Project Generator

Usage:
    python generate.py <project-name> --desc "description" --features "feat1,feat2,feat3" --example "usage example"

Examples:
    python generate.py url-shortener --desc "Quick URL shortener CLI" --features "shorten,expand,stats" --example "python main.py bit.ly/abc"
"""

import os
import sys
import argparse
import shutil
from datetime import datetime

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), ".template")
PROJECTS_DIR = os.path.join(os.path.dirname(__file__))


def substitute(content, substitutions):
    """Simple string substitution"""
    for key, value in substitutions.items():
        content = content.replace(key, value)
    return content


def generate_project(name, description, features, usage_example):
    """Generate a new nightly project from template"""

    # Slugify name
    slug = name.lower().replace(" ", "-")

    # Create project directory
    project_dir = os.path.join(PROJECTS_DIR, slug)
    if os.path.exists(project_dir):
        print(f"❌ Project '{slug}' already exists")
        sys.exit(1)

    os.makedirs(project_dir)
    print(f"📁 Creating project: {slug}")

    # Template substitutions
    substitutions = {
        "%%PROJECT_NAME%%": name,
        "%%PROJECT_SLUG%%": slug,
        "%%PROJECT_DIR%%": slug,
        "%%DESCRIPTION%%": description,
        "%%FEATURE_1%%": features[0] if len(features) > 0 else "Useful feature",
        "%%FEATURE_2%%": features[1] if len(features) > 1 else "Another feature",
        "%%FEATURE_3%%": features[2] if len(features) > 2 else "Bonus feature",
        "%%USAGE_EXAMPLE%%": usage_example or "python main.py",
        "%%DATE%%": datetime.now().strftime("%Y-%m-%d"),
    }

    # Generate files from template
    for template_file in os.listdir(TEMPLATE_DIR):
        if template_file.startswith("."):
            continue

        src = os.path.join(TEMPLATE_DIR, template_file)
        dst = os.path.join(project_dir, template_file.replace(".template", ""))

        # Read and substitute
        with open(src, "r") as f:
            content = substitute(f.read(), substitutions)

        # Write generated file
        with open(dst, "w") as f:
            f.write(content)

        # Make shell scripts executable
        if dst.endswith(".sh"):
            os.chmod(dst, 0o755)

        print(f"   ✅ {template_file} → {os.path.basename(dst)}")

    # Create empty CHANGELOG.md
    changelog = f"""# Changelog

## v1.0.0 ({datetime.now().strftime("%Y-%m-%d")})
- Initial release
"""
    with open(os.path.join(project_dir, "CHANGELOG.md"), "w") as f:
        f.write(changelog)

    print(f"\n🎉 Project created: {project_dir}")
    print(f"   cd {project_dir}")
    print(f"   python main.py --help")


def main():
    parser = argparse.ArgumentParser(description="Nightly Project Generator")
    parser.add_argument("name", help="Project name (e.g., url-shortener)")
    parser.add_argument("--desc", required=True, help="Project description")
    parser.add_argument("--features", default="", help="Comma-separated features")
    parser.add_argument("--example", default="", help="Usage example")

    args = parser.parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]

    generate_project(args.name, args.desc, features, args.example)


if __name__ == "__main__":
    main()
