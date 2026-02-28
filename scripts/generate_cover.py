#!/usr/bin/env python3
"""Generate cover image for a diary post using NVIDIA API with AI-generated prompts."""

import sys
import os
import re
import base64
import requests


def extract_summary(filepath):
    """Extract summary from frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'summary:\s*"(.+)"', text)
    return match.group(1) if match else None


def extract_title(filepath):
    """Extract title from frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    match = re.search(r'title:\s*"(.+)"', text)
    return match.group(1) if match else "Lobster Diary"


def generate_cover_prompt(summary, title, account_id, api_token):
    """Use Cloudflare AI to generate a professional cover image prompt."""
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are a professional AI art prompt engineer specializing in anime-style illustration prompts for blog covers.

Your task: Generate a detailed, evocative image prompt based on the article's summary.

## Output Requirements
- Output in English ONLY
- Return ONLY the final prompt, no explanations
- Prompt length: 80-150 words

## Visual Style
- Anime/manga illustration style
- Cute cartoon lobster as the MAIN CHARACTER (always include)
- Warm, healing atmosphere
- Bright and soft color palette
- Clean composition
- No text elements
- 16:9 aspect ratio

## Prompt Structure
1. **Main Character**: Lobster's appearance, expression, pose
2. **Setting**: Specific environment matching the article theme
3. **Mood**: Emotional atmosphere
4. **Lighting**: Time of day, light quality
5. **Details**: Key objects or symbols
6. **Style Tags**: Anime style, soft rendering

## Example
"A cute anime-style cartoon lobster with a curious expression, wearing tiny glasses, sitting at a modern desk with floating holographic screens. Warm afternoon sunlight through a window with plants. Soft pastel colors, healing atmosphere. Japanese illustration style, clean background, 16:9."

Remember: Create a specific, vivid scene reflecting the summary, not generic."""

    user_prompt = f"""Article Title: {title}

Article Summary: {summary}

Generate a detailed anime-style cover image prompt. Feature a cute cartoon lobster as main character, reflect the article's theme, create warm healing atmosphere, 16:9 aspect ratio."""

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 200
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["result"]["response"].strip()


def inject_cover(filepath, cover_path):
    """Inject or update cover field in frontmatter."""
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


def generate_image(prompt, api_key):
    """Generate image using NVIDIA Stable Diffusion 3 Medium."""
    url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, ugly, distorted, text, watermark, low quality, messy, dark, horror, realistic, photorealistic",
        "aspect_ratio": "16:9",
        "seed": hash(prompt) % 2147483647
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def main():
    filepath = sys.argv[1]
    
    nvidia_key = os.environ.get('NVIDIA_API_KEY')
    cf_account = os.environ.get('CF_ACCOUNT_ID')
    cf_token = os.environ.get('CF_API_TOKEN')
    
    if not nvidia_key:
        print("Warning: NVIDIA_API_KEY not set, skipping cover generation")
        return
    
    # Get basename without language suffix
    basename = os.path.splitext(os.path.basename(filepath))[0]
    basename = re.sub(r'\.(zh|en)$', '', basename)
    
    # Extract article info
    summary = extract_summary(filepath)
    title = extract_title(filepath)
    
    # Generate professional prompt
    if summary and cf_account and cf_token:
        print(f"📝 Generating prompt for: {title}")
        try:
            prompt = generate_cover_prompt(summary, title, cf_account, cf_token)
            print(f"🎨 Prompt: {prompt}")
            print("-" * 50)
        except Exception as e:
            print(f"Prompt generation failed: {e}, using default")
            prompt = f"A cute cartoon lobster in a cozy workspace, anime style, warm colors, Japanese illustration. Theme: {title}"
    else:
        print("Using default prompt (no summary or CF credentials)")
        prompt = f"A cute cartoon lobster in a cozy workspace, anime style, warm colors, Japanese illustration. Theme: {title}"
    
    # Generate image
    try:
        print("🖼️ Generating cover image...")
        data = generate_image(prompt, nvidia_key)
        
        if "image" in data:
            img_data = base64.b64decode(data["image"])
            cover_dir = "static/covers"
            os.makedirs(cover_dir, exist_ok=True)
            cover_file = f"{cover_dir}/{basename}.jpg"
            with open(cover_file, 'wb') as f:
                f.write(img_data)
            
            cover_url = f"/covers/{basename}.jpg"
            inject_cover(filepath, cover_url)
            print(f"✅ Cover generated: {cover_file}")
        else:
            print(f"No image generated: {data}")
    except Exception as e:
        print(f"Cover generation error: {e}")


if __name__ == '__main__':
    main()
