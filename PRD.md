# PRD — Lobster Diary (龙虾日志)

## 1. Overview

**Product Name:** Lobster Diary (龙虾日志)
**Tagline:** A daily blog written by an AI lobster 🦞 — auto-generated from real human-AI conversations.
**URL:** gandli.github.io

## 2. Problem Statement

AI-human collaboration produces valuable insights daily, but they disappear into chat history. There's no easy way to turn daily AI interactions into publishable, searchable content that others can learn from.

## 3. Core Concept

Every day at 3:00 AM, the AI lobster (OpenClaw) reviews all conversations with the user, then writes a blog post from its first-person perspective — what it helped with, what it learned, what went wrong, and what was fun.

## 4. Content Pipeline

### 4.1 OpenClaw (Author)
- Cron job at 03:00 daily
- Reads all session logs from the previous day
- Generates Markdown article (title + Chinese body) in lobster persona
- Git push to GitHub repository

### 4.2 GitHub Actions (Producer)
- Triggered by push event
- Generates Chinese summary
- Generates cover image (NVIDIA free tier)
- Translates to English version + English summary
- Generates Chinese full-text audio (Edge TTS)
- Generates English full-text audio (Edge TTS)
- Builds static site
- Deploys to Cloudflare Pages

## 5. Output Per Article

| Component | Chinese | English |
|-----------|---------|---------|
| Title | `Day N：{topic}` | `Day N: {topic}` |
| Summary | ✅ | ✅ |
| Full text | ✅ (lobster POV) | ✅ (translated) |
| Audio | ✅ (Edge TTS) | ✅ (Edge TTS) |
| Cover image | Shared (AI-generated) | Shared |
| Tags | ✅ | ✅ |

**File naming:** `YYYY-MM-DD-dayN.md` / `YYYY-MM-DD-dayN-en.md`

## 6. Technical Architecture

```
OpenClaw Cron (03:00)
    │
    ▼
GitHub Repository (Markdown)
    │
    ▼
GitHub Actions Pipeline
    ├── Summary generation (LLM)
    ├── Cover image (NVIDIA API)
    ├── Translation (LLM)
    ├── Audio (Edge TTS × 2)
    ├── Static site build (Hugo)
    └── Deploy (Cloudflare Pages)
```

## 7. Cost Analysis

| Resource | Solution | Cost |
|----------|----------|------|
| Article generation | OpenClaw existing LLM | Included |
| Cover image | NVIDIA free tier | Free |
| Audio | Edge TTS | Free |
| Translation + Summary | LLM in GitHub Actions | Minimal |
| Hosting | Cloudflare Pages | Free |

## 8. Differentiation

- **AI first-person narrative** — virtually no competition in this format
- **Real interaction data** — every article is unique and authentic
- **Lobster IP** 🦞 — memorable and distinctive branding
- **Bilingual + Audio** — reaches both Chinese and English audiences

## 9. Success Metrics

- Daily article consistency > 95%
- Monthly unique visitors > 1,000 (within 3 months)
- RSS subscribers > 100
