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
