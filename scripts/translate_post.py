#!/usr/bin/env python3
"""Translate a Chinese diary post to English using NVIDIA NIM API."""

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


def call_nvidia_llm(prompt, api_key, model="meta/llama-3.1-8b-instruct"):
    """Call NVIDIA NIM API for text generation."""
    url = f"https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.3
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def translate_in_chunks(content, api_key, chunk_size=3000):
    """Translate long content in chunks."""
    # Split by paragraphs to avoid breaking mid-sentence
    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = para + '\n\n'
        else:
            current_chunk += para + '\n\n'
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        prompt = (
            "Translate the following Chinese text to English. "
            "Keep the markdown formatting exactly as is. "
            "Return only the translated text, no explanations.\n\n"
            f"{chunk}"
        )
        translated = call_nvidia_llm(prompt, api_key)
        translated_chunks.append(translated)
        print(f"  Translated chunk {i+1}/{len(chunks)}")
    
    return '\n\n'.join(translated_chunks)


def main():
    src_file = sys.argv[1]
    dst_file = sys.argv[2] if len(sys.argv) > 2 else src_file.replace('.zh.md', '.en.md')

    api_key = os.environ.get('NVIDIA_API_KEY')
    
    if not api_key:
        print("Warning: NVIDIA_API_KEY not set, skipping translation")
        return

    fm, content = extract_frontmatter_and_content(src_file)

    try:
        # Translate content in chunks if needed
        if len(content) > 3000:
            print("  Content is long, translating in chunks...")
            translated = translate_in_chunks(content, api_key)
        else:
            prompt = (
                "Translate the following Chinese blog post to English. "
                "Keep the markdown formatting exactly as is. "
                "Return only the translated content, no explanations.\n\n"
                f"{content}"
            )
            translated = call_nvidia_llm(prompt, api_key)
        
        # Translate title in frontmatter
        title_match = re.search(r'title:\s*"(.+)"', fm)
        if title_match:
            title_zh = title_match.group(1)
            title_en = call_nvidia_llm(
                f"Translate this Chinese title to English. Return only the translated title, nothing else:\n\n{title_zh}",
                api_key
            ).strip().strip('"')
            fm = re.sub(r'title:\s*".+"', f'title: "{title_en}"', fm)
        
        # Write translated file
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(f'---\n{fm}\n---\n{translated}')
        
        print(f"Translated: {src_file} -> {dst_file}")
    except Exception as e:
        print(f"Translation error: {e}")
        raise


if __name__ == '__main__':
    main()