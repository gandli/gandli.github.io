+++
title = 'Python 调用 openai gpt-4o-mini 为 Hugo 生成文章摘要'
date = 2024-10-10T13:16:26+08:00
draft = false
summary = '借助 OpenAI 的 GPT-4 模型，Python 开发者可以轻松为博客文章生成吸引人的摘要，从而在信息海洋中快速提取核心内容，提升阅读体验。'
+++


不少博客已用上了AI摘要，我们也可以给自己的博客加上。借助 OpenAI 的 GPT-4 模型，Python 开发者可以轻松调用这一强大的自然语言处理工具，生成精准的文章摘要。本篇文章将详细介绍如何通过 Python 调用 GPT-4o-mini 版本，来实现自动生成文章摘要的功能，帮助用户更快地从海量信息中获取所需内容。

## 具体流程如下：

1. 初始化 OpenAI 客户端：从环境变量中获取 API 密钥和自定义的 API 基础 URL，初始化 OpenAI 客户端。
2. 生成摘要：函数 generate_summary 调用 OpenAI API 生成文章摘要。摘要是针对正文内容生成的，要求简洁明了并且带有吸引力。
3. 处理 Markdown 文件：函数 process_markdown_file 打开并读取每个 Markdown 文件，检查是否已有摘要。如果没有，则调用 generate_summary 生成摘要并插入到文件元数据中。
4. 批量处理：通过 process_all_markdown_files 函数，遍历指定目录下的所有 Markdown 文件，批量处理每个文件的摘要生成和插入。

## 代码实现

```python
import os
from openai import OpenAI
from pathlib import Path

# 从环境变量中获取 API 密钥和自定义 base_url
token = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("OPENAI_API_BASE")  # 自定义 Azure OpenAI API base URL
model_name = "gpt-4o-mini"  # 模型名称

# 初始化 OpenAI 客户端
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

POSTS_DIR = Path("content/posts")
SUMMARY_KEY = "summary"


def generate_summary(text):
    """调用 Azure OpenAI API 生成摘要"""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的文章摘要助手。",
            },
            {
                "role": "user",
                "content": f"为以下文章写一句话摘要，既要体现核心要点，又要能留下hook吸引人点击:\n\n{text}",
            },
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=150,  # 控制摘要长度
        model=model_name,
    )
    return response.choices[0].message.content.strip()


# 遍历 content/posts 目录下的所有 Markdown 文件
for md_file in POSTS_DIR.glob("*.md"):
    with open(md_file, "r") as file:
        lines = file.readlines()

    content = "".join(lines)

    # 检查文件头部是否以 '+++' 开始，表示存在元数据
    if content.startswith("+++"):
        front_matter_start = content.find("+++")  # 第一个 '+++'
        front_matter_end = content.find("+++", front_matter_start + 3)  # 第二个 '+++'

        # 提取元数据部分
        front_matter = content[front_matter_start : front_matter_end + 3]

        # 如果 summary 已经存在，跳过该文件
        if f"{SUMMARY_KEY} =" in front_matter:
            print(f"跳过 {md_file}，摘要已存在。")
            continue

        # 调用 OpenAI API 生成摘要
        summary = generate_summary(
            content[front_matter_end + 3 :]
        )  # 提取正文部分生成摘要

        # 将 summary 插入到元数据的最后一行（在第二个 '+++' 之前）
        summary_line = f"summary = '{summary}'\n"
        new_front_matter = front_matter[:-3] + summary_line + "+++\n"

        # 重新组合文件内容
        new_content = new_front_matter + content[front_matter_end + 3 :]

        # 写入修改后的文件
        with open(md_file, "w") as file:
            file.write(new_content)

        print(f"已为 {md_file} 添加摘要。")

    else:
        print(f"跳过 {md_file}，未找到有效的元数据。")
```