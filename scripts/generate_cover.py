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
    if 'cover:' in text.split('---')[1] if '---' in text else '':
        text = re.sub(r'cover:.*', f'cover: {cover_path}', text, count=1)
    else:
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = f'---\n{parts[1].strip()}\ncover: {cover_path}\n---{parts[2]}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    filepath = sys.argv[1]
    api_key = os.environ.get('NVIDIA_API_KEY')
    
    if not api_key:
        print("Warning: NVIDIA_API_KEY not set, skipping cover generation")
        return
    
    title, tags = extract_title_and_tags(filepath)
    basename = os.path.splitext(os.path.basename(filepath))[0]
    
    # Generate image prompt from title
    prompt = f"A cute cartoon lobster 🦞 in a cozy workspace, digital art style. Theme: {title}. Tags: {tags}. Warm colors, clean illustration, blog cover art."
    
    # Call NVIDIA image generation API
    url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "text_prompts": [{"text": prompt, "weight": 1}],
        "cfg_scale": 7,
        "height": 512,
        "width": 1024,
        "samples": 1,
        "steps": 30,
        "seed": 0
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        if "artifacts" in data and len(data["artifacts"]) > 0:
            img_data = base64.b64decode(data["artifacts"][0]["base64"])
            cover_dir = "static/covers"
            os.makedirs(cover_dir, exist_ok=True)
            cover_file = f"{cover_dir}/{basename}.jpg"
            with open(cover_file, 'wb') as f:
                f.write(img_data)
            
            # Inject cover path into frontmatter
            cover_url = f"/covers/{basename}.jpg"
            inject_cover(filepath, cover_url)
            print(f"Cover generated: {cover_file}")
        else:
            print("No image generated from API response")
    except Exception as e:
        print(f"Cover generation error: {e}")
        print("Using default cover or no cover")

if __name__ == '__main__':
    main()
