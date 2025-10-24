+++
date = '2025-10-24T19:38:29+08:00'
draft = false
title = 'Burp Suite Extensions 开发'
categories:
  - categories
tags:
  - burp
  - extensions
  - Cloudflare
  - Worker
  - Flareprox
  - proxy
+++

## Flareprox_Burp_Extension

Flareprox_Burp_Extension 是一个 Burp Suite 扩展，可按需配置 Cloudflare Worker 代理，并将您的流量通过 Cloudflare 的边缘网络进行传输。它帮助红队成员、渗透测试人员和研究人员从不同的 Cloudflare PoPs 发起请求，而无需更改本地代理布局，从而更容易与 Cloudflare 发起的流量融合或在测试期间轮换 IP 地址。

## 开发环境 🛠️

参考： [手动设置您的扩展开发环境](https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/set-up/manual-setup)

- IDE：推荐使用 IntelliJ IDEA 社区版 💡
  - macOS：`brew install intellij-idea-ce`
  - Windows：`scoop install extras/idea`
- JDK：推荐使用 Liberica JDK 21 Full ☕️
  - macOS：`brew install bell-sw/liberica/liberica-jdk21-full`
  - Windows：`scoop bucket add java && scoop install java/liberica21-full-jdk`

## 参考

- [Cloudflare Workers 指定区域运行](https://blog.lyc8503.net/post/cloudflare-worker-region/)
- [IPRotate_Burp_Extension](https://github.com/RhinoSecurityLabs/IPRotate_Burp_Extension)
-[FlareProx](https://github.com/MrTurvey/flareprox)
- [Montoya API（GitHub 仓库）](https://github.com/PortSwigger/burp-extensions-montoya-api)
- [Montoya API 示例（GitHub 仓库）](https://github.com/PortSwigger/burp-extensions-montoya-api-examples)
- [Montoya API 文档（Javadoc）](https://portswigger.github.io/burp-extensions-montoya-api/javadoc/)
- [httpbin.org](https://httpbin.org/)：用于请求测试
- [Burp-Suite-Extender-Montoya-Course（GitHub 仓库）](https://github.com/federicodotta/Burp-Suite-Extender-Montoya-Course)
- [Extending Burp Suite for Fun and Profit — The Montoya Way（Part 1）](https://hnsecurity.it/blog/extending-burp-suite-for-fun-and-profit-the-montoya-way-part-1/)
