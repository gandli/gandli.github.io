#!/usr/bin/env python3
"""Generate summary for a diary post and inject into frontmatter."""

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

def inject_summary(filepath, summary):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Check if summary already exists
    if 'summary:' in text.split('---')[1] if '---' in text else '':
        # Update existing summary
        text = re.sub(r'summary:.*', f'summary: "{summary}"', text, count=1)
    else:
        # Add summary before closing ---
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = f'---\n{parts[1].strip()}\nsummary: "{summary}"\n---{parts[2]}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    filepath = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'zh'
    
    api_key = os.environ.get('LLM_API_KEY')
    api_base = os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')
    model = os.environ.get('LLM_MODEL', 'gpt-4o-mini')
    
    if not api_key:
        print("Warning: LLM_API_KEY not set, skipping summary generation")
        return
    
    frontmatter, content = extract_frontmatter_and_content(filepath)
    
    client = OpenAI(api_key=api_key, base_url=api_base)
    
    prompt = f"Generate a concise one-line summary (under 100 characters) in {'Chinese' if lang == 'zh' else 'English'} for this blog post. Return ONLY the summary text, nothing else.\n\n{content[:3000]}"
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    summary = response.choices[0].message.content.strip().strip('"').strip("'")
    inject_summary(filepath, summary)
    print(f"Summary ({lang}): {summary}")

if __name__ == '__main__':
    main()
