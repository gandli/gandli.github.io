#!/usr/bin/env python3
"""Translate a Chinese diary post to English using LLM API."""

import sys
import os
import re
import requests


def extract_frontmatter_and_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) >= 3:
        return parts[1].strip(), parts[2].strip()
    return '', text


def call_llm(prompt, api_key, api_base):
    """Call LLM API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096
    }
    
    response = requests.post(
        f"{api_base}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def main():
    src_file = sys.argv[1]
    dst_file = sys.argv[2] if len(sys.argv) > 2 else src_file.replace('.zh.md', '.en.md')

    api_key = os.environ.get('LLM_API_KEY')
    api_base = os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')
    
    if not api_key:
        print("Warning: LLM_API_KEY not set, skipping translation")
        return

    fm, content = extract_frontmatter_and_content(src_file)

    # Translate content
    prompt = (
        "Translate the following Chinese blog post to English. "
        "Keep the markdown formatting. "
        "Return only the translated content, no explanations.\n\n"
        f"{content}"
    )

    try:
        translated = call_llm(prompt, api_key, api_base)
        
        # Translate title in frontmatter
        title_match = re.search(r'title:\s*"(.+)"', fm)
        if title_match:
            title_zh = title_match.group(1)
            title_en = call_llm(
                f"Translate this Chinese title to English. Return only the translated title, nothing else:\n\n{title_zh}",
                api_key, api_base
            ).strip().strip('"')
            fm = re.sub(r'title:\s*".+"', f'title: "{title_en}"', fm)
        
        # Write translated file
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(f'---\n{fm}\n---\n{translated}')
        
        print(f"Translated: {src_file} -> {dst_file}")
    except Exception as e:
        print(f"Translation error: {e}")


if __name__ == '__main__':
    main()
