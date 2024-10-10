# 我的个人博客 [![Deploy Hugo site to Pages](https://github.com/gandli/gandli.github.io/actions/workflows/hugo.yaml/badge.svg)](https://github.com/gandli/gandli.github.io/actions/workflows/hugo.yaml)

欢迎来到我的个人博客！这个博客使用 [Hugo](https://gohugo.io/) 作为静态网站生成器，并托管在 [GitHub Pages](https://pages.github.com/) 上。博客旨在分享我的学习、项目和想法。

## 特性

- **Hugo 驱动**: 通过 Hugo 生成静态页面，快速、高效。
- **自动摘要生成**: 使用 Azure OpenAI 服务自动生成文章摘要，简化内容管理。
- **Markdown 支持**: 所有文章使用 Markdown 格式撰写，便于编辑和管理。
- **GitHub Actions 自动化部署**: 通过 GitHub Actions 实现文章的自动摘要生成和博客自动构建、发布。
  
## 文件结构

```
├── content           # 博客内容目录
│   └── posts         # 文章存储目录
│       └── my-first-post.md
├── static            # 静态资源目录 (图片、CSS、JavaScript 等)
├── layouts           # 自定义 Hugo 布局
├── themes            # 主题目录
├── config.toml       # Hugo 配置文件
├── .github           # GitHub Actions 配置
│   └── workflows     # 自动化工作流
└── README.md         # 项目说明文件
```

## 使用方法

### 克隆项目

```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名
```

### 安装 Hugo

根据 [Hugo 官方文档](https://gohugo.io/getting-started/installing/) 安装 Hugo。

### 本地预览

运行以下命令在本地启动服务器：

```bash
hugo server
```

然后在浏览器中打开 `http://localhost:1313` 预览博客。

### 添加新文章

```bash
hugo new posts/your-post-title.md
```

编辑生成的 Markdown 文件并发布。

### 自动摘要生成

每次向 `content/posts` 目录中添加或修改 `.md` 文件时，GitHub Actions 将自动调用 Azure OpenAI 服务为新文章生成摘要并将其添加到文章的元数据中。

### 部署

当你推送修改到 `main` 分支时，GitHub Actions 会自动构建并部署博客到 GitHub Pages。

## 贡献

如果你发现任何问题或有改进建议，欢迎提交 [Issue](https://github.com/gandli/gandli.github.io/issues) 或发起 Pull Request。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。
