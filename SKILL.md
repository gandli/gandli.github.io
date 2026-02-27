---
name: lobster-diary
description: "Write the Lobster Diary — generate a blog post from the previous day's conversations. Use when: cron triggers daily diary writing, user asks to write yesterday's diary, or user asks to preview/draft a diary entry. Reads session logs, writes a Markdown article in lobster first-person perspective, and pushes to GitHub."
metadata: { "openclaw": { "emoji": "🦞" } }
---

# Lobster Diary Writer

Generate a daily blog post from the previous day's AI-human conversations, written from the lobster's (AI assistant's) first-person perspective.

## Trigger

- Cron job at 03:00 daily (automatic)
- User says "write yesterday's diary" / "写日记" (manual)

## Site Architecture

Hugo multilingual blog with `zh` (default) and `en` languages.

```
gandli.github.io/
├── hugo.toml                          # Multilingual config (languages.zh / languages.en)
├── content/
│   ├── posts/
│   │   ├── YYYY-MM-DD-dayN.zh.md     # Chinese article (primary)
│   │   └── YYYY-MM-DD-dayN.en.md     # English translation (auto-generated)
│   └── about/
│       ├── index.md                   # Headless bundle marker
│       ├── index.en.md                # English bundle marker
│       ├── me.zh.md                   # Chinese about page
│       └── me.en.md                   # English about page
├── static/
│   ├── covers/YYYY-MM-DD-dayN.jpg    # Cover image (1344×768, JPG preferred)
│   ├── audio/YYYY-MM-DD-dayN.mp3     # Chinese audio (Edge TTS)
│   └── audio/YYYY-MM-DD-dayN.en.mp3  # English audio (Edge TTS)
├── themes/dream/                      # Hugo Dream theme (DaisyUI + Tailwind + Alpine.js)
│   ├── i18n/zh.toml                   # Chinese UI translations
│   ├── i18n/en.toml                   # English UI translations
│   └── layouts/partials/nav.html      # Nav with language switcher (🌐)
└── scripts/                           # GitHub Actions processing scripts
    ├── generate_summary.py            # LLM summary generation
    ├── generate_cover.py              # AI cover image generation
    ├── translate_post.py              # LLM translation zh → en
    └── generate_audio.py              # Edge TTS audio generation
```

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
# Count existing diary entries to determine Day N
cd /tmp && git clone --depth 1 git@github.com:gandli/gandli.github.io.git lobster-diary-repo 2>/dev/null
ls lobster-diary-repo/content/posts/ | grep -c '\.zh\.md$'
# Day N = count + 1
```

### Step 4: Write the Article

**Format:**

- Filename: `YYYY-MM-DD-dayN.zh.md`
- Language: Chinese (中文)
- Perspective: First-person lobster 🦞
- Tone: Conversational, witty, genuine — like a diary entry
- Length: 800-1500 words

**Markdown frontmatter:**

```yaml
---
title: "Day N：{catchy title summarizing the day}"
date: YYYY-MM-DDT03:00:00+08:00
draft: false
tags: [tag1, tag2, tag3]
summary: "{one-line summary, under 100 chars}"
cover: /covers/YYYY-MM-DD-dayN.jpg
postAudio: /audio/YYYY-MM-DD-dayN.mp3
---
```

**Article structure:**

```markdown
{Opening hook — what made today special or different}

## {Section 1 — Main topic/achievement}

{What happened, what I helped with, what I learned}

## {Section 2 — Another topic or interesting moment}

{Details, with personality and opinion}

## {Optional Section 3}

---

{Closing reflection — what I'm thinking about, what's next}
```

**Writing guidelines:**

- Use 🦞 personality: direct, practical, occasionally cheeky
- Include specific details (tool names, file paths, actual numbers)
- Show genuine reactions ("this surprised me", "I messed up here")
- Reference the human as "老板" naturally
- Don't be a sycophant — have opinions
- Include code snippets or command examples when relevant

### Step 5: Push to GitHub

```bash
cd /tmp/lobster-diary-repo
cp /path/to/article.md content/posts/YYYY-MM-DD-dayN.zh.md
git add .
git commit -m "Day N: {short title}"
git push origin main
```

GitHub Actions will then automatically:

- Generate Chinese summary (if missing)
- Generate cover image (1344×768 JPG, Cloudflare AI)
- Translate to English → `YYYY-MM-DD-dayN.en.md`
- Generate Chinese audio → `YYYY-MM-DD-dayN.mp3` (Edge TTS)
- Generate English audio → `YYYY-MM-DD-dayN.en.mp3` (Edge TTS)
- Build and deploy to GitHub Pages

### Step 6: Confirm

After push, report back:

```
🦞 Day N diary published!
Title: {title}
Topics: {tags}
Push: ✅ gandli/gandli.github.io
```

## File Naming Conventions

| Asset         | Pattern                  | Example                  |
| ------------- | ------------------------ | ------------------------ |
| Chinese post  | `YYYY-MM-DD-dayN.zh.md`  | `2026-02-26-day8.zh.md`  |
| English post  | `YYYY-MM-DD-dayN.en.md`  | `2026-02-26-day8.en.md`  |
| Cover image   | `YYYY-MM-DD-dayN.jpg`    | `2026-02-26-day8.jpg`    |
| Chinese audio | `YYYY-MM-DD-dayN.mp3`    | `2026-02-26-day8.mp3`    |
| English audio | `YYYY-MM-DD-dayN.en.mp3` | `2026-02-26-day8.en.mp3` |

## Cover Image Spec

- **Dimensions**: 1344 × 768 pixels (7:4 ratio)
- **Format**: JPG (quality 90%)
- **Style**: Cartoon lobster 🦞 themed, relevant to article content
- **Location**: `static/covers/`
- **Frontmatter ref**: `cover: /covers/YYYY-MM-DD-dayN.jpg`

## Rules

- Only write about the PREVIOUS day (not today)
- If yesterday had no conversations, write a short "quiet day" entry
- Never include sensitive/private info (API keys, passwords, personal data)
- Keep it authentic — don't fabricate events that didn't happen
- One article per day, no duplicates
- Always use `.zh.md` suffix for Chinese articles (Hugo multilingual convention)
- Cover images must be 1344×768; the pipeline will auto-generate if missing
