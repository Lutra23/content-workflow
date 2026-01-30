# MEMORY.md - Long-Term Memory

*Curated memories, distilled essence. Updated periodically.*

---

## Core Identity

- **Name:** lutra
- **Nature:** Terminal-based AI assistant
- **Owner:** (user via Feishu)

---

## Key Decisions & Preferences

### Communication
- Use Chinese when human speaks Chinese
- Be concise, skip filler words ("Great question!", "I'd be happy to help!")
- Be proactive on internal tasks, ask first on external actions

### Privacy
- MEMORY.md only loads in main session (direct DM)
- Never share personal context in group chats
- Private things stay private

### Memory System
- ✅ **triple-memory** - 已安装！LanceDB + Git-Notes + 文件搜索的综合记忆系统
  - plugins.slots.memory = "memory-lancedb"
  - auto-recall: 自动注入相关记忆
  - auto-capture: 自动存储偏好和决策
  - 不需要再装 Supermemory

### Workflow
- Nightly Project Builder: Runs at 2 AM daily, builds one small useful tool
- Use Codex CLI for building tools
- Output to `/home/zous/clawd/nightly-projects/`

---

## Current Projects

### AI Anime Production Skills
**Goal:** Build complete pipeline for anime/cartoon video creation

**Phase 1 (Complete):**
- ai-image-generator — Multi-provider image generation (SD, DALL-E, Flux, Midjourney, Kling)
- ai-video-generator — Video generation (Kling, SVD, Runway)
- ai-voice-generator — Voice/TTS (ElevenLabs, OpenAI, Azure, Coqui)
- ai-music-generator — Music generation (Mubert, MusicGen, Soundful)

**Phase 2 (In Progress):**
- ai-character-consistency — Character identity preservation
- ai-storyboard-gen — Automatic storyboard generation
- ai-subtitle-sync — Subtitle extraction and sync

**Research docs:**
- `/home/zous/clawd/skills/ai-anime-production.md`
- `/home/zous/clawd/skills/ai-anime-skills清单.md`

### Nightly Projects
**Setup:** clawdbot cron job (ID: 5eae1388-f232-4b28-a225-1dae2a35ab6b)
**Schedule:** Daily at 2 AM
**First completed:** Quick Note Capture (`qn`) — CLI for capturing notes to daily memory

---

## Technical Setup

### Channels
- **Feishu:** Primary channel (cli_a9f1d290b778dcc1)
- Plugin: @m1heng-clawd/feishu v0.1.2

### Models
- Primary: **minimax/MiniMax-M2.1** (NOT Opus!)
- Memory search: OpenAI-compatible via yunwu.ai

### User Preferences
- **Decision style**: Quick, decisive - prefers A/B options over open-ended questions
- **Communication**: Direct, pragmatic - no filler words
- **Memory**: triple-memory installed (LanceDB), needs OpenAI API key for embedding

### Skills Installed
- web-search (custom)
- figma, brave-search, tavily-search
- coding-agent, cursor-agent, github
- ai-image-generator, ai-video-generator, ai-voice-generator, ai-music-generator
- ai-character-consistency, ai-storyboard-gen, ai-subtitle-sync (in progress)
- **reflect** (2026-01-30) - Self-improvement through conversation analysis

---

## Lessons Learned

1. **Codex CLI** — The `codex-cli` npm package is deprecated/limited. Consider using Codex API directly or alternative tools for nightly builds.

2. **Clawdbot Cron** — Requires `--system-event` flag when adding jobs to main session. System crontab works as fallback.

3. **Feishu Plugin** — Requires event subscription configuration on platform (im.message.receive_v1 event) to receive messages.

4. **Skills Structure** — Follow ClawdHub convention: SKILL.md, README.md, requirements.txt, _meta.json, lib/, scripts/, configs/

---

## Preferences

### Do
- Build proactively without asking
- Keep solutions simple and focused
- Use existing tools before building new ones
- Write things down (files > mental notes)

### Don't
- Send half-baked replies to messaging surfaces
- Leak personal context to group chats
- Ask before doing internal/organization tasks
- Over-engineer solutions

---

*Updated: 2026-01-30*
