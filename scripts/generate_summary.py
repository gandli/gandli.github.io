#!/usr/bin/env python3
"""Generate summary for a diary post using Cloudflare Workers AI."""

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


def main():
    filepath = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'zh'

    if not os.environ.get('CF_API_TOKEN'):
        print("Warning: CF_API_TOKEN not set, skipping summary")
        return

    _, content = extract_frontmatter_and_content(filepath)

    lang_name = '中文' if lang == 'zh' else 'English'
    prompt = (
        f"为以下博客文章生成一句话摘要（{lang_name}，100字以内）。"
        f"只返回摘要文本，不要任何其他内容。\n\n{content[:4000]}"
    )

    summary = chat(prompt, max_tokens=200).strip().strip('"').strip("'")
    inject_field(filepath, 'summary', summary)
    print(f"Summary ({lang}): {summary}")


if __name__ == '__main__':
    main()
