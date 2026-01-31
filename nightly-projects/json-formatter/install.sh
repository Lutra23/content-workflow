#!/bin/bash
# Install script for json-formatter

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${HOME}/.local/bin"

# Create bin dir if not exists
mkdir -p "${INSTALL_DIR}"

# Copy script
cp "${SCRIPT_PATH}/main.py" "${INSTALL_DIR}/json-formatter"
chmod +x "${INSTALL_DIR}/json-formatter"

echo "✅ Installed json-formatter to ${INSTALL_DIR}/json-formatter"
echo "Make sure ${INSTALL_DIR} is in your PATH"
echo "Add to PATH: export PATH="${INSTALL_DIR}:$PATH""
