#!/bin/bash
# quick_replace.sh - 快速替换原文件（无备份）

DIR="../static/covers"
COLOR="000000"

echo "⚠️  警告: 此操作将直接修改原文件!"
echo "目录: $DIR"
echo "继续吗? (y/N): "
read -r confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "取消操作"
    exit 1
fi

# 处理 JPG
for img in "$DIR"/*.{jpg,jpeg,JPG,JPEG}; do
    [ -f "$img" ] || continue
    echo "处理: $(basename "$img")"
    sips -Z 1344 "$img" --out /tmp/temp.jpg
    sips --padToHeightWidth 768 1344 --padColor "$COLOR" /tmp/temp.jpg --out "$img"
done

# 处理 PNG
for img in "$DIR"/*.{png,PNG}; do
    [ -f "$img" ] || continue
    echo "处理: $(basename "$img")"
    sips -Z 1344 "$img" --out /tmp/temp.jpg
    sips --padToHeightWidth 768 1344 --padColor "$COLOR" /tmp/temp.jpg --out /tmp/temp_filled.jpg
    sips -s format png /tmp/temp_filled.jpg --out "$img"
done

echo "✅ 完成!"