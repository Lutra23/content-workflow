#!/usr/bin/env python3
"""🔍 Emoji Search CLI - Quick emoji search tool."""

import sys
import json

# Simple emoji data (subset for demo)
EMOJI_DATA = {
    "😀": ["grin", "smile", "happy"],
    "😂": ["laugh", "tears", "joy"],
    "😃": ["smiley", "happy"],
    "😄": ["smile", "happy"],
    "😅": ["sweat", "nervous"],
    "😆": ["laugh", "happy"],
    "😉": ["wink", "flirt"],
    "😊": ["blush", "happy"],
    "😋": ["yum", "tasty"],
    "😎": ["cool", "sunglasses"],
    "😍": ["love", "heart eyes"],
    "😘": ["kiss", "love"],
    "🥰": ["love", "hearts"],
    "😗": ["kiss"],
    "😙": ["kiss", "smile"],
    "😚": ["kiss", "closed eyes"],
    "🙂": ["slightly happy"],
    "🤗": ["hug", "happy"],
    "🤔": ["think", "hmm"],
    "🤨": ["skeptical"],
    "😐": ["neutral"],
    "😑": ["expressionless"],
    "😶": ["no mouth"],
    "🙄": ["eye roll"],
    "😏": ["smirk"],
    "😣": ["suffering"],
    "😥": ["sad", "disappointed"],
    "😮": ["surprised", "open mouth"],
    "🤐": ["zipper", "silence"],
    "😯": ["silent", "surprised"],
    "😪": ["sleepy", "tired"],
    "😫": ["tired", "upset"],
    "😴": ["sleep", "zzz"],
    "😌": ["relief", "relaxed"],
    "😛": ["tongue"],
    "😜": ["tongue", "wink"],
    "🤪": ["crazy", "zany"],
    "😝": ["tongue", "laugh"],
    "🤑": ["money", "rich"],
    "🤗": ["hug", "happy"],
    "🤭": ["hand over mouth"],
    "🤫": ["shh", "quiet"],
    "🤔": ["think", "hmm"],
    "🤭": ["oops"],
    "🤥": ["lie", "liar"],
    "🤫": ["shush"],
    "🤭": ["hidden"],
    "🤐": ["zip it"],
    "🤨": ["doubt"],
    "🧐": ["monocle"],
    "🤓": ["nerd", "smart"],
    "🤠": ["cowboy", "hat"],
    "🥳": ["party", "celebration"],
    "😎": ["cool", "sunglasses"],
    "🤓": ["glasses", "smart"],
    "🧐": ["glasses", "detective"],
    "🥸": ["disguise", "incognito"],
    "😏": ["smirk"],
    "😐": ["neutral"],
    "😑": ["blank"],
    "🙂": ["slight smile"],
    "😏": ["smirk"],
    "😒": ["unamused"],
    "😞": ["disappointed"],
    "😔": ["sad", "pensive"],
    "😟": ["worried"],
    "😣": ["persevere"],
    "😖": ["frustrated"],
    "😫": ["tired"],
    "😩": ["weary"],
    "😤": ["triumph"],
    "😢": ["cry", "tears"],
    "😭": ["sob", "crying"],
    "😱": ["scream", "scared"],
    "😨": ["scared", "fear"],
    "😰": ["anxious", "nervous"],
    "😥": ["disappointed"],
    "😢": ["crying"],
    "🤧": ["sneeze", "sick"],
    "🥵": ["hot", "heat"],
    "🥶": ["cold", "freeze"],
    "🥴": ["woozy", "dizzy"],
    "😵": ["dizzy"],
    "🤯": ["exploding head", "shock"],
    "🤠": ["cowboy"],
    "🥳": ["party"],
    "🥴": ["confused"],
    "🔥": ["fire", "flame", "hot"],
    "❤️": ["heart", "love", "red"],
    "🧡": ["orange heart"],
    "💛": ["yellow heart"],
    "💚": ["green heart"],
    "💙": ["blue heart"],
    "💜": ["purple heart"],
    "🖤": ["black heart"],
    "🤍": ["white heart"],
    "🤎": ["brown heart"],
    "💔": ["broken heart"],
    "❣️": ["exclamation heart"],
    "💕": ["two hearts"],
    "💞": ["revolving hearts"],
    "💓": ["beating heart"],
    "💗": ["growing heart"],
    "💖": ["sparkling heart"],
    "💘": ["arrow heart"],
    "💝": ["gift heart"],
    "💟": ["heart decoration"],
    "✨": ["sparkles", "stars"],
    "⭐": ["star", "yellow"],
    "🌟": ["glowing star"],
    "💫": ["dizzy star"],
    "🌙": ["moon", "night"],
    "🌞": ["sun", "day"],
    "🌤️": ["sun behind cloud"],
    "🌈": ["rainbow"],
    "⚡": ["lightning", "zap"],
    "💧": ["droplet", "water"],
    "🌊": ["wave", "ocean"],
    "❄️": ["snowflake"],
    "🌸": ["cherry blossom", "flower"],
    "🌺": ["hibiscus", "flower"],
    "🌻": ["sunflower", "flower"],
    "🌹": ["rose", "flower"],
    "🌷": ["tulip", "flower"],
    "💐": ["bouquet", "flowers"],
    "🍀": ["four leaf clover", "lucky"],
    "🌿": ["herb", "plant"],
    "🌱": ["seedling", "plant"],
    "🌲": ["evergreen tree"],
    "🌳": ["deciduous tree"],
    "🌴": ["palm tree"],
    "🌵": ["cactus"],
    "🍁": ["maple leaf"],
    "🍂": ["fallen leaf"],
    "🍃": ["leaf fluttering"],
    "🐶": ["dog", "puppy"],
    "🐱": ["cat", "kitten"],
    "🐭": ["mouse"],
    "🐹": ["hamster"],
    "🐰": ["rabbit", "bunny"],
    "🦊": ["fox"],
    "🐻": ["bear"],
    "🐼": ["panda"],
    "🐨": ["koala"],
    "🐯": ["tiger"],
    "🦁": ["lion"],
    "🐮": ["cow"],
    "🐷": ["pig"],
    "🐸": ["frog"],
    "🐙": ["octopus"],
    "🦋": ["butterfly"],
    "🐛": ["bug"],
    "🐞": ["ladybug"],
    "🐜": ["ant"],
    "🐝": ["bee"],
    "🐌": ["snail"],
    "🦗": ["cricket"],
    "🕷️": ["spider"],
    "🦂": ["scorpion"],
    "🦟": ["mosquito"],
    "🦠": ["microbe", "virus"],
    "💐": ["flowers"],
    "🌈": ["rainbow"],
}


def search_emojis(keyword: str, limit: int = 30) -> list:
    """Search for emojis matching the keyword."""
    keyword_lower = keyword.lower()
    results = []
    for emo, aliases in EMOJI_DATA.items():
        # Check if keyword in emoji or any alias
        for alias in aliases:
            if keyword_lower in alias.lower():
                results.append((emo, aliases))
                break
        if len(results) >= limit:
            break
    return results


def main():
    if len(sys.argv) < 2:
        print("🔍 Emoji Search CLI")
        print("Usage: es <keyword>")
        print("Example: es fire")
        print("         es happy cat")
        sys.exit(0)
    
    keyword = " ".join(sys.argv[1:])
    results = search_emojis(keyword)
    
    if not results:
        print(f"❌ No emojis found for: '{keyword}'")
        print("💡 Try: love, fire, happy, cat, star, moon, flower, etc.")
        sys.exit(1)
    
    print(f"🔍 Found {len(results)} emojis for '{keyword}':\n")
    
    for i, (emoji_char, aliases) in enumerate(results, 1):
        alias_list = ", ".join(aliases[:3]) if aliases else "no alias"
        print(f"{i:2}. {emoji_char}  ({alias_list})")
    
    print("\n💡 Copy emoji directly from terminal")


if __name__ == "__main__":
    main()
