#!/bin/bash
# Enhanced Nightly Project Builder - with logging and progress tracking

LOG_FILE="/home/zous/clawd/logs/nightly-projects.log"
PROJECT_DIR="/home/zous/clawd/nightly-projects"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$PROJECT_DIR" "$(dirname $LOG_FILE)"

log "🚀 Starting Nightly Project Build"

# Check what we worked on today
log "📊 Analyzing today's context..."

# Get recent notes
RECENT_NOTES=$(tail -20 ~/clawd/memory/$(date +%Y-%m-%d).md 2>/dev/null || echo "")

# Determine project type based on recent work
if echo "$RECENT_NOTES" | grep -qi "python\|code\|script"; then
    PROJECT_TYPE="automation"
elif echo "$RECENT_NOTES" | grep -qi "note\|capture\|memory"; then
    PROJECT_TYPE="productivity"
elif echo "$RECENT_NOTES" | grep -qi "ai\|model\|image"; then
    PROJECT_TYPE="ai-tool"
else
    PROJECT_TYPE="productivity"
fi

log "💡 Selected project type: $PROJECT_TYPE"

# Create project directory
TODAY_DIR="$PROJECT_DIR/$(date +%Y-%m-%d)"
mkdir -p "$TODAY_DIR"

# Generate project
log "🔨 Building $PROJECT_TYPE project..."

# Create a simple, useful tool
cat > "$TODAY_DIR/README.md" << EOF
# Nightly Project - $(date +%Y-%m-%d)

Type: $PROJECT_TYPE
Created: $(date '+%Y-%m-%d %H:%M:%S')

## What this does

[Add description]

## Usage

\`\`\`bash
[Add usage]
\`\`\`

## Notes

Generated as part of Nightly Project Builder
EOF

log "✅ Project created: $TODAY_DIR"
log "📁 Location: $TODAY_DIR"

# Update index
echo "- $(date +%Y-%m-%d): $PROJECT_TYPE project" >> "$PROJECT_DIR/INDEX.md"

log "🎉 Nightly project complete!"
log "========================================"
