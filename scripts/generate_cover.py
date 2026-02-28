#!/usr/bin/env python3
"""Generate cover image for a diary post using NVIDIA API."""

import sys
import os
import re
import json
import base64
import requests

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
    if len(parts) >= 3 and 'cover:' in parts[1]:
        parts[1] = re.sub(r'cover:.*', f'cover: {cover_path}', parts[1], count=1)
        text = '---' + parts[1] + '---' + parts[2]
    elif len(parts) >= 3:
        parts[1] = parts[1].rstrip() + f'\ncover: {cover_path}\n'
        text = '---' + parts[1] + '---' + parts[2]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    filepath = sys.argv[1]
    api_key = os.environ.get('NVIDIA_API_KEY')
    
    if not api_key:
        print("Warning: NVIDIA_API_KEY not set, skipping cover generation")
        return
    
    title, tags = extract_title_and_tags(filepath)
    
    # Get basename without language suffix (e.g., 2026-02-27-day9.zh.md -> 2026-02-27-day9)
    basename = os.path.splitext(os.path.basename(filepath))[0]
    basename = re.sub(r'\.(zh|en)$', '', basename)  # Remove .zh or .en suffix
    
    # Generate image prompt from title
    prompt = f"A cute cartoon lobster in a cozy workspace with laptop, digital art style. Theme: {title}. Warm colors, clean illustration, blog cover art."
    
    # Call NVIDIA Stable Diffusion 3 Medium API
    url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, ugly, distorted, text, watermark, low quality",
        "aspect_ratio": "16:9",
        "seed": hash(basename) % 2147483647
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        if "image" in data:
            img_data = base64.b64decode(data["image"])
            cover_dir = "static/covers"
            os.makedirs(cover_dir, exist_ok=True)
            cover_file = f"{cover_dir}/{basename}.jpg"
            with open(cover_file, 'wb') as f:
                f.write(img_data)
            
            cover_url = f"/covers/{basename}.jpg"
            inject_cover(filepath, cover_url)
            print(f"Cover generated: {cover_file}")
        elif "artifacts" in data and len(data["artifacts"]) > 0:
            img_data = base64.b64decode(data["artifacts"][0]["base64"])
            cover_dir = "static/covers"
            os.makedirs(cover_dir, exist_ok=True)
            cover_file = f"{cover_dir}/{basename}.jpg"
            with open(cover_file, 'wb') as f:
                f.write(img_data)
            
            cover_url = f"/covers/{basename}.jpg"
            inject_cover(filepath, cover_url)
            print(f"Cover generated: {cover_file}")
        else:
            print("No image generated from API response")
    except Exception as e:
        print(f"Cover generation error: {e}")

if __name__ == '__main__':
    main()
