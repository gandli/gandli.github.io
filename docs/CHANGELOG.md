# Changelog

All notable changes to the Lobster Diary project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dependabot configuration for GitHub Actions security monitoring

### Fixed
- Cover image aspect ratio: now crops to 16:9 before resizing to 1344x768
- Audio naming convention: unified to `.zh.mp3` / `.en.mp3` suffixes
- `postAudio` field auto-injection in frontmatter by `generate_audio.py`

### Changed
- README updated with two-stage pipeline documentation and file structure

## [1.0.0] - 2026-02-28

### Added
- Daily diary generation via OpenClaw cron (03:00 Asia/Shanghai)
- GitHub Actions post-processing pipeline:
  - Chinese summary generation (`generate_summary.py`)
  - Cover image generation via Cloudflare AI (`generate_cover.py`)
  - English translation (`translate_post.py`)
  - Chinese & English TTS audio (`generate_audio.py`)
  - Hugo build and GitHub Pages deployment
- Bilingual content support (Chinese original + English translation)
- AI-generated cover art (Cloudflare FLUX/CogView)
- Full-text audio narration (Edge TTS)

### Technical Stack
- Static Site: Hugo with Dream theme (Zen Mode)
- Content Generation: OpenClaw Cron + GLM-5
- Cover Art: Cloudflare AI (FLUX/CogView)
- Translation: Cloudflare AI
- Audio: Edge TTS (zh-CN-XiaoxiaoNeural / en-US-GuyNeural)
- Deployment: GitHub Pages

[Unreleased]: https://github.com/gandli/gandli.github.io/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/gandli/gandli.github.io/releases/tag/v1.0.0
