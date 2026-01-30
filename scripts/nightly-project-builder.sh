#!/bin/bash
# Nightly AI Project Builder
# Runs every night at 2 AM to build a useful tool with Codex CLI

echo "========================================"
echo "🚀 Nightly AI Project Builder"
echo "📅 $(date)"
echo "========================================"

# 1. Analyze recent work
echo ""
echo "📊 Analyzing recent workflow..."
cd /home/zous/clawd

# Check what we worked on today
CLAWD_WORKSPACE="/home/zous/clawd"

# 2. Pick a small improvement project
echo ""
echo "💡 Selecting tonight's project..."

# Project ideas (rotate nightly):
# - Productivity script
# - Communication improvement  
# - Automation tool
# - Data visualization
# - Knowledge management

PROJECT_TYPE=$(shuf -e "productivity" "automation" "communication" "data-tool" "knowledge" -n 1)
echo "   → Tonight's focus: $PROJECT_TYPE"

# 3. Run Codex CLI to build something
echo ""
echo "🔨 Building with Codex CLI..."

# This will run Codex to create something useful
npx codex-cli@latest \
  --model "claude-sonnet-4-20250514" \
  --prompt "Build a small, useful tool for improving Clawdbot workflow. 
Focus: $PROJECT_TYPE.
Requirements:
- Keep it simple and focused
- Should solve one real problem
- Include clear documentation
- Should be ready to use

Output the code to /home/zous/clawd/nightly-projects/"

# 4. Report result
echo ""
echo "========================================"
echo "✅ Nightly project complete!"
echo "📁 Location: /home/zous/clawd/nightly-projects/"
echo "========================================"
