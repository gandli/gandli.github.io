#!/usr/bin/env python3
"""Generate cover image for a diary post using Cloudflare Workers AI (FLUX-1-schnell)."""

import sys
import os
import re
import io
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
    # Strip language suffix (.zh, .en) from basename
    if basename.endswith('.zh') or basename.endswith('.en'):
        basename = basename.rsplit('.', 1)[0]

    prompt = (
        f"A cute cartoon lobster character in a cozy workspace, digital illustration, "
        f"warm colors, clean blog cover art. Theme: {title}. "
        f"Flat design, vibrant, minimal text."
    )

    try:
        img_bytes = generate_image(prompt)
        cover_dir = "static/covers"
        os.makedirs(cover_dir, exist_ok=True)
        cover_file = f"{cover_dir}/{basename}.jpg"

        # Convert to JPG at 1344x768 (16:9), crop to maintain aspect ratio
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(img_bytes))
            img = img.convert('RGB')
            
            # Target size and aspect ratio
            target_w, target_h = 1344, 768
            target_ratio = target_w / target_h  # 16:9
            
            # Calculate crop dimensions to maintain aspect ratio
            w, h = img.size
            current_ratio = w / h
            
            if current_ratio > target_ratio:
                # Image is wider, crop width
                new_w = int(h * target_ratio)
                left = (w - new_w) // 2
                img = img.crop((left, 0, left + new_w, h))
            elif current_ratio < target_ratio:
                # Image is taller, crop height
                new_h = int(w / target_ratio)
                top = (h - new_h) // 2
                img = img.crop((0, top, w, top + new_h))
            # else: already correct ratio
            
            img = img.resize((target_w, target_h), Image.LANCZOS)
            img.save(cover_file, 'JPEG', quality=90)
        except ImportError:
            # Fallback: save raw bytes if Pillow not available
            with open(cover_file, 'wb') as f:
                f.write(img_bytes)

        inject_cover(filepath, f"/covers/{basename}.jpg")
        print(f"Cover generated: {cover_file}")
    except Exception as e:
        print(f"Cover generation error: {e}")


if __name__ == '__main__':
    main()
