#!/usr/bin/env python3
"""Generate cover image for a diary post using Cloudflare Workers AI (FLUX-1-schnell)."""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(__file__))
from cf_ai import chat, generate_image


def extract_title_and_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    title_match = re.search(r'title:\s*"(.+)"', text)
    tags_match = re.search(r'tags:\s*\[(.+)\]', text)
    title = title_match.group(1) if title_match else "Lobster Diary"
    tags = tags_match.group(1) if tags_match else ""
    return title, tags


def inject_cover(filepath, cover_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        return
    fm = parts[1]
    if re.search(r'^cover:', fm, re.MULTILINE):
        fm = re.sub(r'^cover:.*$', f'cover: {cover_path}', fm, count=1, flags=re.MULTILINE)
    else:
        fm = fm.rstrip() + f'\ncover: {cover_path}\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm.strip()}\n---{parts[2]}')


def main():
    filepath = sys.argv[1]

    if not os.environ.get('CF_API_TOKEN'):
        print("Warning: CF_API_TOKEN not set, skipping cover generation")
        return

    title, tags = extract_title_and_tags(filepath)
    basename = os.path.splitext(os.path.basename(filepath))[0]

    prompt = (
        f"A cute cartoon lobster character in a cozy workspace, digital illustration, "
        f"warm colors, clean blog cover art. Theme: {title}. "
        f"Flat design, vibrant, minimal text."
    )

    try:
        img_bytes = generate_image(prompt)
        cover_dir = "static/covers"
        os.makedirs(cover_dir, exist_ok=True)
        cover_file = f"{cover_dir}/{basename}.png"
        with open(cover_file, 'wb') as f:
            f.write(img_bytes)

        inject_cover(filepath, f"/covers/{basename}.png")
        print(f"Cover generated: {cover_file} ({len(img_bytes)} bytes)")
    except Exception as e:
        print(f"Cover generation error: {e}")


if __name__ == '__main__':
    main()
