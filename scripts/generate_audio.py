#!/usr/bin/env python3
"""Generate audio for a diary post using Cloudflare MeloTTS.

Usage: python generate_audio.py <post_file> <lang> <output_mp3>
  lang: zh or en
"""

import sys
import os
import re
import subprocess
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from cf_ai import tts


def strip_markdown(text: str) -> str:
    """Remove markdown formatting for cleaner TTS."""
    # Remove frontmatter
    parts = text.split('---', 2)
    body = parts[2] if len(parts) >= 3 else text
    # Remove headings markers
    body = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
    # Remove bold/italic
    body = re.sub(r'\*+([^*]+)\*+', r'\1', body)
    # Remove links, keep text
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    # Remove inline code
    body = re.sub(r'`[^`]+`', '', body)
    # Remove code blocks
    body = re.sub(r'```[\s\S]*?```', '', body)
    # Remove blockquotes, list markers, table lines
    body = re.sub(r'^[>\-\|].*$', '', body, flags=re.MULTILINE)
    # Remove images
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    # Collapse whitespace
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    return body


def wav_to_mp3(wav_bytes: bytes, output_path: str):
    """Convert WAV bytes to MP3 using ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp.write(wav_bytes)
        tmp_path = tmp.name
    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', tmp_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', output_path],
            check=True, capture_output=True
        )
    finally:
        os.unlink(tmp_path)


def main():
    post_file = sys.argv[1]
    lang = sys.argv[2]  # zh or en
    output_mp3 = sys.argv[3]

    if not os.environ.get('CF_API_TOKEN'):
        print(f"Warning: CF_API_TOKEN not set, skipping {lang} audio")
        return

    with open(post_file, 'r', encoding='utf-8') as f:
        text = f.read()

    clean_text = strip_markdown(text)
    if not clean_text.strip():
        print(f"Warning: no content to generate audio for {post_file}")
        return

    # MeloTTS has input length limits; chunk if needed
    MAX_CHARS = 3000
    chunks = []
    while clean_text:
        chunks.append(clean_text[:MAX_CHARS])
        clean_text = clean_text[MAX_CHARS:]

    os.makedirs(os.path.dirname(output_mp3) or '.', exist_ok=True)

    if len(chunks) == 1:
        audio_bytes = tts(chunks[0], lang=lang)
        wav_to_mp3(audio_bytes, output_mp3)
    else:
        # Generate chunks and concat
        tmp_files = []
        for i, chunk in enumerate(chunks):
            audio_bytes = tts(chunk, lang=lang)
            tmp_mp3 = f"/tmp/audio_chunk_{i}.mp3"
            wav_to_mp3(audio_bytes, tmp_mp3)
            tmp_files.append(tmp_mp3)

        # Concat with ffmpeg
        list_file = "/tmp/audio_concat.txt"
        with open(list_file, 'w') as f:
            for p in tmp_files:
                f.write(f"file '{p}'\n")
        subprocess.run(
            ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_file, '-c', 'copy', output_mp3],
            check=True, capture_output=True
        )
        for p in tmp_files:
            os.unlink(p)

    size = os.path.getsize(output_mp3)
    print(f"Audio ({lang}): {output_mp3} ({size} bytes)")


if __name__ == '__main__':
    main()
