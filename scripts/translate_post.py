#!/usr/bin/env python3
"""Translate a Chinese diary post to English."""

import sys
import os
import re
from openai import OpenAI

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
    
    api_key = os.environ.get('LLM_API_KEY')
    api_base = os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')
    model = os.environ.get('LLM_MODEL', 'gpt-4o-mini')
    
    if not api_key:
        print("Warning: LLM_API_KEY not set, skipping translation")
        return
    
    frontmatter, content = extract_frontmatter_and_content(src_file)
    
    client = OpenAI(api_key=api_key, base_url=api_base)
    
    # Translate title
    title_match = re.search(r'title:\s*"(.+)"', frontmatter)
    title_zh = title_match.group(1) if title_match else "Untitled"
    
    # Translate content
    prompt = f"""Translate this Chinese blog post to English. Maintain the Markdown formatting, code blocks, and structure. Keep technical terms as-is. The author is an AI lobster assistant 🦞 writing a daily diary.

Title: {title_zh}

Content:
{content}

Return the translated content in Markdown format (no frontmatter, just the body)."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )
    
    translated = response.choices[0].message.content.strip()
    
    # Translate title
    title_prompt = f'Translate this blog post title to English. Keep "Day N" format. Return ONLY the title:\n{title_zh}'
    title_resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": title_prompt}],
        max_tokens=100
    )
    title_en = title_resp.choices[0].message.content.strip().strip('"').strip("'")
    
    # Generate English summary
    summary_prompt = f"Generate a concise one-line summary (under 100 characters) in English for this blog post. Return ONLY the summary:\n{translated[:2000]}"
    summary_resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=200
    )
    summary_en = summary_resp.choices[0].message.content.strip().strip('"').strip("'")
    
    # Build English frontmatter
    # Copy tags and other fields from original
    tags_match = re.search(r'tags:\s*\[(.+)\]', frontmatter)
    tags = tags_match.group(0) if tags_match else 'tags: []'
    
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1) if date_match else ''
    
    cover_match = re.search(r'cover:\s*(.+)', frontmatter)
    cover = f'\ncover: {cover_match.group(1)}' if cover_match else ''
    
    en_post = f"""---
title: "{title_en}"
date: {date}
draft: false
author: "Lobster 🦞"
categories: ["diary"]
{tags}
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
