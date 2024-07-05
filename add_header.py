import os
import re
from datetime import datetime

content_dir = 'content/weekly'

header_template = """---
date: {date}
title: {title}
weight: 2
---
"""

def extract_title_from_content(content):
    match = re.search(r'^# (.+)', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"

def add_header_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'date:' not in content and 'title:' not in content:
        title = extract_title_from_content(content)
        date = datetime.now().isoformat()

        header = header_template.format(date=date, title=title)
        new_content = header + content

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)

for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith('.md') and file != '_index.md':
            filepath = os.path.join(root, file)
            add_header_to_file(filepath)
