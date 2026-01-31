#!/usr/bin/env python3
"""
json-formatter - Format and validate JSON files

Usage:
    python main.py [file] [options]

Options:
    --help      Show this help
    --install   Install to PATH
    --version   Show version
    --pretty    Pretty print (default)
    --minify    Minify JSON
    --validate  Validate only, no output
"""

import argparse
import sys
import os
import json

VERSION = "1.0.0"


def format_json(content, minify=False):
    """Format or minify JSON content"""
    data = json.loads(content)
    if minify:
        return json.dumps(data, separators=(',', ':'))
    else:
        return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="json-formatter")
    parser.add_argument("file", nargs="?", help="JSON file to process (stdin if not provided)")
    parser.add_argument("--install", action="store_true", help="Install to PATH")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--pretty", action="store_true", help="Pretty print (default)")
    parser.add_argument("--minify", action="store_true", help="Minify JSON")
    parser.add_argument("--validate", action="store_true", help="Validate only, no output")

    args = parser.parse_args()

    if args.version:
        print(f"json-formatter v{VERSION}")
        return

    if args.install:
        install()
        return

    # Read input
    if args.file:
        try:
            with open(args.file, "r") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return
    else:
        content = sys.stdin.read()

    # Validate
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    if args.validate:
        print("✅ Valid JSON")
        return

    # Output
    minify = args.minify
    output = format_json(content, minify=minify)
    print(output)


def install():
    """Install script to PATH"""
    script_path = os.path.abspath(__file__)
    install_dir = os.path.expanduser("~/.local/bin")

    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    # Create wrapper script
    wrapper = """#!/bin/bash
python3 "{script_path}" "$@"
""".format(script_path=script_path)
    wrapper_path = os.path.join(install_dir, "json-formatter")

    with open(wrapper_path, "w") as f:
        f.write(wrapper)
    os.chmod(wrapper_path, 0o755)

    print("Installed to {wrapper_path}".format(wrapper_path=wrapper_path))
    print("Make sure {install_dir} is in your PATH".format(install_dir=install_dir))


if __name__ == "__main__":
    main()
