#!/usr/bin/env python3
"""Generate summary for a diary post using LLM API."""

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


def inject_field(filepath, field, value):
    """Inject or update a field in frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        return
    fm = parts[1]
    pattern = rf'^{field}:.*$'
    if re.search(pattern, fm, re.MULTILINE):
        fm = re.sub(pattern, f'{field}: "{value}"', fm, count=1, flags=re.MULTILINE)
    else:
        fm = fm.rstrip() + f'\n{field}: "{value}"\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm.strip()}\n---{parts[2]}')


def call_llm(prompt, api_key, api_base):
    """Call LLM API to generate summary."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    response = requests.post(
        f"{api_base}/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def main():
    filepath = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'zh'

    api_key = os.environ.get('LLM_API_KEY')
    api_base = os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')
    
    if not api_key:
        print("Warning: LLM_API_KEY not set, skipping summary")
        return

    _, content = extract_frontmatter_and_content(filepath)

    lang_name = '中文' if lang == 'zh' else 'English'
    prompt = (
        f"为以下博客文章生成一句话摘要（{lang_name}，100字以内）。"
        f"只返回摘要文本，不要任何其他内容。\n\n{content[:4000]}"
    )

    try:
        summary = call_llm(prompt, api_key, api_base).strip().strip('"').strip("'")
        inject_field(filepath, 'summary', summary)
        print(f"Summary ({lang}): {summary}")
    except Exception as e:
        print(f"Error generating summary: {e}")


if __name__ == '__main__':
    main()
