#!/usr/bin/env python3
"""Generate audio for a diary post.

- Chinese: edge-tts (Microsoft Azure, high quality)
- English: edge-tts (consistent quality across languages)

Usage: python generate_audio.py <post_file> <lang> <output_mp3>
  lang: zh or en

Auto-injects postAudio into frontmatter for Chinese audio.
"""

import sys
import os
import re
import subprocess
import tempfile

# Voice mapping
VOICES = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-GuyNeural",
}


def strip_markdown(text: str) -> str:
    """Remove markdown formatting for cleaner TTS."""
    parts = text.split('---', 2)
    body = parts[2] if len(parts) >= 3 else text
    body = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
    body = re.sub(r'\*+([^*]+)\*+', r'\1', body)
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    body = re.sub(r'`[^`]+`', '', body)
    body = re.sub(r'```[\s\S]*?```', '', body)
    body = re.sub(r'^[>\-\|].*$', '', body, flags=re.MULTILINE)
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    # Remove bare URLs
    body = re.sub(r'https?://\S+', '', body)
    # Remove emoji (optional, sometimes TTS reads them weirdly)
    body = re.sub(r'[🦞🎨🔊📝🌐⏭️✅❌⚠️🚀🔧💡📋🔍💬🤖📦🎯💰📸🚬✝️🍱🔖📚🛡️🥗🌤️👶]', '', body)
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    return body


def generate_with_edge_tts(text: str, voice: str, output_mp3: str):
    """Generate audio using edge-tts."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
        tmp.write(text)
        tmp_path = tmp.name

    try:
        subprocess.run(
            ['edge-tts', '--voice', voice, '--file', tmp_path, '--write-media', output_mp3],
            check=True, capture_output=True, text=True
        )
    finally:
        os.unlink(tmp_path)


def inject_post_audio(filepath, audio_path):
    """Inject postAudio into frontmatter (only for Chinese audio)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        return
    fm = parts[1]
    if re.search(r'^postAudio:', fm, re.MULTILINE):
        fm = re.sub(r'^postAudio:.*$', f'postAudio: {audio_path}', fm, count=1, flags=re.MULTILINE)
    else:
        fm = fm.rstrip() + f'\npostAudio: {audio_path}\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm.strip()}\n---{parts[2]}')


def main():
    post_file = sys.argv[1]
    lang = sys.argv[2]
    output_mp3 = sys.argv[3]

    voice = VOICES.get(lang, VOICES["en"])

    with open(post_file, 'r', encoding='utf-8') as f:
        text = f.read()

    clean_text = strip_markdown(text)
    if not clean_text.strip():
        print(f"Warning: no content to generate audio for {post_file}")
        return

    os.makedirs(os.path.dirname(output_mp3) or '.', exist_ok=True)

    generate_with_edge_tts(clean_text, voice, output_mp3)

    size = os.path.getsize(output_mp3)
    print(f"Audio ({lang}): {output_mp3} ({size} bytes, voice={voice})")

    # Inject postAudio into frontmatter (for both Chinese and English)
    audio_public_path = output_mp3.replace('static/', '/')
    inject_post_audio(post_file, audio_public_path)
    print(f"Injected postAudio: {audio_public_path}")


if __name__ == '__main__':
    main()
