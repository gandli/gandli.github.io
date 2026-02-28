#!/usr/bin/env python3
"""Translate a Chinese diary post to English using Cloudflare Workers AI."""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(__file__))
from cf_ai import chat


def extract_frontmatter_and_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) >= 3:
        return parts[1].strip(), parts[2].strip()
    return '', text


def main():
    src_file = sys.argv[1]
    dst_file = sys.argv[2]

    if not os.environ.get('CF_API_TOKEN'):
        print("Warning: CF_API_TOKEN not set, skipping translation")
        return

    frontmatter, content = extract_frontmatter_and_content(src_file)

    # Extract metadata from original
    title_match = re.search(r'title:\s*"(.+)"', frontmatter)
    title_zh = title_match.group(1) if title_match else "Untitled"
    tags_match = re.search(r'tags:\s*\[(.+)\]', frontmatter)
    tags_zh = tags_match.group(1) if tags_match else ''
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1) if date_match else ''
    cover_match = re.search(r'cover:\s*(.+)', frontmatter)
    cover_path = cover_match.group(1) if cover_match else ''
    # Strip .zh from cover path if present (covers are language-neutral)
    cover_path = re.sub(r'\.zh\.(jpg|png|webp)$', r'.\1', cover_path)
    cover = f'\ncover: {cover_path}' if cover_path else ''

    # Translate title
    title_en = chat(
        f'Translate this blog title to English. Keep "Day N" format if present. Return ONLY the title:\n{title_zh}',
        max_tokens=100
    ).strip().strip('"').strip("'")

    # Translate tags
    tags_en = ''
    if tags_zh:
        tags_en = chat(
            f"Translate these tags to English, comma-separated. Return ONLY the tags list:\n{tags_zh}",
            max_tokens=100
        ).strip()

    # Translate content (chunk if long)
    translated = chat(
        f"""Translate this Chinese blog post to English. Maintain Markdown formatting and code blocks.
Keep technical terms as-is. The author is an AI lobster assistant 🦞 writing a daily diary.

{content}

Return ONLY the translated Markdown body, no frontmatter.""",
        max_tokens=4096
    ).strip()

    # Generate English summary
    summary_en = chat(
        f"Generate a one-line summary (under 100 chars) in English for this post. Return ONLY the summary:\n{translated[:2000]}",
        max_tokens=200
    ).strip().strip('"').strip("'")

    # Write English post
    tags_line = f'tags: [{tags_en}]' if tags_en else 'tags: []'
    en_post = f"""---
title: "{title_en}"
date: {date}
draft: false
author: "Lobster 🦞"
categories: ["diary"]
{tags_line}
summary: "{summary_en}"{cover}
---

{translated}
"""

    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write(en_post)

    print(f"Translated: {src_file} -> {dst_file}")
    print(f"Title EN: {title_en}")
    print(f"Summary EN: {summary_en}")


if __name__ == '__main__':
    main()
