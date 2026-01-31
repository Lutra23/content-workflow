#!/usr/bin/env python3
"""
%%PROJECT_NAME%% - %%DESCRIPTION%%

Usage:
    python main.py [options]

Options:
    --help      Show this help
    --install   Install to PATH
    --version   Show version
"""

import argparse
import sys
import os

VERSION = "1.0.0"


def main():
    parser = argparse.ArgumentParser(description="%%PROJECT_NAME%%")
    parser.add_argument("--install", action="store_true", help="Install to PATH")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()

    if args.version:
        print("%%PROJECT_NAME%% v{VERSION}")
        return

    if args.install:
        install()
        return

    # Main logic here
    print("%%PROJECT_NAME%% - %%DESCRIPTION%%")
    print("Use --help for options")


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
    wrapper_path = os.path.join(install_dir, "%%PROJECT_SLUG%%")

    with open(wrapper_path, "w") as f:
        f.write(wrapper)
    os.chmod(wrapper_path, 0o755)

    print("Installed to {wrapper_path}".format(wrapper_path=wrapper_path))
    print("Make sure {install_dir} is in your PATH".format(install_dir=install_dir))


if __name__ == "__main__":
    main()
