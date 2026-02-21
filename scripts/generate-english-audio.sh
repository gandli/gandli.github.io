#!/bin/bash
# 生成英文版日记音频

set -e

REPO="/Users/user/.openclaw/projects/gandli.github.io"
cd "$REPO"

# 英文语音（Edge TTS）
VOICE="en-US-GuyNeural"

for day in 1 2 3 4 5; do
  EN_FILE="content/posts/2026-02-*-day${day}-en.md"
  AUDIO_FILE="static/audio/day${day}-en.mp3"
  
  if ls $EN_FILE 1> /dev/null 2>&1; then
    echo "Generating audio for Day $day (English)..."
    
    # 提取正文（去除 front matter）
    sed -n '/^---$/,/^---$/!p' $EN_FILE > /tmp/day${day}_en_content.txt
    
    # 生成音频
    edge-tts --voice "$VOICE" \
      --file /tmp/day${day}_en_content.txt \
      --write-media "$AUDIO_FILE"
    
    echo "✅ Day $day English audio: $AUDIO_FILE"
  fi
done

echo "All English audio files generated!"
