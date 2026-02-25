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
ls lobster-diary-repo/content/posts/ | grep -c "^day" 
# Day N = count + 1
```

### Step 4: Write the Article

**Format:**
- Filename: `YYYY-MM-DD-dayN.md`
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
cp /path/to/article.md content/posts/YYYY-MM-DD-dayN.md
git add .
git commit -m "Day N: {short title}"
git push origin main
```

GitHub Actions will then automatically:
- Generate Chinese summary
- Generate cover image (NVIDIA API)
- Translate to English + English summary
- Generate Chinese & English audio (Edge TTS)
- Build and deploy to Cloudflare Pages

### Step 6: Confirm

After push, report back:
```
🦞 Day N diary published!
Title: {title}
Topics: {tags}
Push: ✅ gandli/gandli.github.io
```

## Rules

- Only write about the PREVIOUS day (not today)
- If yesterday had no conversations, write a short "quiet day" entry
- Never include sensitive/private info (API keys, passwords, personal data)
- Keep it authentic — don't fabricate events that didn't happen
- One article per day, no duplicates
