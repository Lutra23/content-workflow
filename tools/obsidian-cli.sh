#!/bin/bash
# Obsidian Vault CLI - Simple wrapper for managing Obsidian vaults

DEFAULT_VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian}"

usage() {
    cat << 'USAGE'
Usage: obsidian [command] [options]

Commands:
    list [vault]          List notes in vault
    search <query>        Search notes
    create <name>         Create new note
    open <note>           Open note in Obsidian app
    today                 Open today's daily note
    path <note>           Print note path

Options:
    --vault <path>        Vault path (default: $DEFAULT_VAULT)
    --help                Show this help

Examples:
    obsidian list
    obsidian search "AI"
    obsidian create "New Note"
    obsidian open "Daily Notes"
    obsidian today
USAGE
    exit 0
}

VAULT="$DEFAULT_VAULT"

while [[ $# -gt 0 ]]; do
    case $1 in
        --vault)
            VAULT="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

CMD="$1"
shift || true

if [ ! -d "$VAULT" ]; then
    echo "Error: Vault not found: $VAULT"
    echo "Set OBSIDIAN_VAULT env var or use --vault"
    exit 1
fi

case "$CMD" in
    list)
        find "$VAULT" -name "*.md" -type f | sed "s|$VAULT/||" | head -20
        ;;
    search)
        query="$*"
        grep -r "$query" "$VAULT" --include="*.md" -l 2>/dev/null | sed "s|$VAULT/||" | head -10
        ;;
    create)
        name="$1"
        filename=$(echo "$name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md
        cat > "$VAULT/$filename" << 'NOTE'
---
created: 
---
NOTE
        sed -i "s|created: |created: $(date +%Y-%m-%d)|" "$VAULT/$filename"
        echo "# $name" >> "$VAULT/$filename"
        echo "Created: $VAULT/$filename"
        ;;
    open)
        name="$*"
        xdg-open "obsidian://open?vault=Obsidian&file=$name" 2>/dev/null || \
        echo "Open: obsidian://open?vault=Obsidian&file=$name"
        ;;
    today)
        date=$(date +%Y-%m-%d)
        xdg-open "obsidian://open?vault=Obsidian&file=Daily%20Notes/$date" 2>/dev/null || \
        echo "Open: obsidian://open?vault=Obsidian&file=Daily%20Notes/$date"
        ;;
    path)
        name="$*"
        filename=$(echo "$name" | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md
        find "$VAULT" -name "$filename" -type f 2>/dev/null | head -1
        ;;
    *)
        usage
        ;;
esac
