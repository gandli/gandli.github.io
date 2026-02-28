---
name: lobster-diary
description: "Write the Lobster Diary — generate a blog post from the previous day's conversations. Use when: cron triggers daily diary writing, user asks to write yesterday's diary, or user asks to preview/draft a diary entry. Reads session logs, writes a Markdown article in lobster first-person perspective, and pushes to GitHub."
metadata: { "openclaw": { "emoji": "🦞" } }
---

# Lobster Diary Writer

Generate a daily blog post from the previous day's AI-human conversations, written from the lobster's (AI assistant's) first-person perspective.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Two-Stage Pipeline                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Stage 1: OpenClaw (Content Generation)                                 │
│  ════════════════════════════════════                                    │
│  03:00 Cron → Gather conversations → Write Markdown → Git push          │
│                                                                          │
│  Stage 2: GitHub Actions (Post-Processing)                              │
│  ══════════════════════════════════════════                              │
│  Push trigger → Summary + Cover + Translation + Audio → Deploy          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Trigger

- Cron job at 03:00 daily (automatic)
- User says "write yesterday's diary" / "写日记" (manual)

## Workflow

### Step 1: Gather Yesterday's Conversations

```
1. Determine yesterday's date (Asia/Shanghai timezone)
2. Use `sessions_list` to find all sessions active yesterday
3. Use `sessions_history` to pull conversation content from each session
4. Also read `memory/YYYY-MM-DD.md` for yesterday's daily notes
```

### Step 2: Analyze & Extract

From all conversations, identify:
- **Main topics** — What did we work on?
- **Achievements** — What got done?
- **Interesting moments** — Funny, surprising, or insightful exchanges
- **Technical learnings** — New tools, techniques, or discoveries
- **Challenges** — What went wrong or was tricky?

### Step 3: Determine Day Number

```bash
cd /tmp && git clone --depth 1 git@github.com:gandli/gandli.github.io.git lobster-diary-repo 2>/dev/null
ls lobster-diary-repo/content/posts/ | grep -c "\.zh\.md"
# Day N = count + 1
```

### Step 4: Write the Article

**File naming:**
- `content/posts/YYYY-MM-DD-dayN.zh.md` (Chinese original)
- GitHub Actions generates: `YYYY-MM-DD-dayN.en.md` (English translation)

**Markdown frontmatter:**
```yaml
---
title: "Day N：{catchy title summarizing the day}"
date: YYYY-MM-DDT03:00:00+08:00
draft: false
tags: [tag1, tag2, tag3]
summary: "{one-line summary, under 100 chars}"
# cover and postAudio auto-injected by GitHub Actions
---
```

**Writing guidelines:**
- Language: Chinese (中文)
- Perspective: First-person lobster 🦞
- Tone: Conversational, witty, genuine
- Length: 800-1500 words
- Include specific details (tool names, file paths, actual numbers)
- Reference the human as "老板" naturally

### Step 5: Push to GitHub

```bash
cd /tmp/lobster-diary-repo
cp /path/to/article.md content/posts/YYYY-MM-DD-dayN.zh.md
git add .
git commit -m "Day N: {short title}"
git push origin main
```

## GitHub Actions Pipeline

After push, `.github/workflows/process-diary.yml` automatically:

| Step | Script | Output |
|------|--------|--------|
| Summary | `generate_summary.py` | Injected `summary:` in frontmatter |
| Cover | `generate_cover.py` | `static/covers/YYYY-MM-DD-dayN.jpg` + `cover:` |
| Translation | `translate_post.py` | `content/posts/YYYY-MM-DD-dayN.en.md` |
| Audio (ZH) | `generate_audio.py zh` | `static/audio/YYYY-MM-DD-dayN.zh.mp3` + `postAudio:` |
| Audio (EN) | `generate_audio.py en` | `static/audio/YYYY-MM-DD-dayN.en.mp3` + `postAudio:` |
| Deploy | Hugo build | GitHub Pages |

### Asset Naming Convention

```
content/posts/
├── YYYY-MM-DD-dayN.zh.md   # Chinese original
└── YYYY-MM-DD-dayN.en.md   # English translation

static/covers/
└── YYYY-MM-DD-dayN.jpg     # Cover image (1344x768, 16:9)

static/audio/
├── YYYY-MM-DD-dayN.zh.mp3  # Chinese narration
└── YYYY-MM-DD-dayN.en.mp3  # English narration
```

## Configuration

### Cron Setup (OpenClaw)

```json
{
  "name": "lobster-diary",
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "写昨天的日记" },
  "sessionTarget": "isolated"
}
```

### Required Secrets (GitHub)

- `CF_API_TOKEN` — Cloudflare AI API token
- `CF_ACCOUNT_ID` — Cloudflare account ID

## Technical Stack

| Component | Technology |
|-----------|------------|
| Static Site | Hugo + Dream theme (Zen Mode) |
| Content Generation | OpenClaw Cron + GLM-5 |
| Cover Art | Cloudflare AI (FLUX/CogView) |
| Translation | Cloudflare AI |
| Audio (ZH) | Edge TTS (zh-CN-XiaoxiaoNeural) |
| Audio (EN) | Edge TTS (en-US-GuyNeural) |
| Deployment | GitHub Pages |

## Rules

- Only write about the PREVIOUS day (not today)
- If yesterday had no conversations, write a short "quiet day" entry
- Never include sensitive/private info (API keys, passwords, personal data)
- Keep it authentic — don't fabricate events that didn't happen
- One article per day, no duplicates

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.
