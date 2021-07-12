---
title: 'Webhook'
date: 2021-07-11T15:32:04+08:00
draft: false
description: Webhook 就是一个接收 HTTP POST（或GET，PUT，DELETE）的URL，一个实现了 Webhook 的 API 提供商就是在当事件发生的时候会向这个配置好的 URL 发送一条信息，与请求-响应式不同，使用 Webhook 你可以实时接受到变化。
tags:
  - Webhook
categories:
  - Webhook
---

# [Docker🐳+Nginx+WebHook+Node 一键自动化持续部署](https://juejin.cn/post/6844904080595238919)

```bash
# autoDeploy.sh
#!/bin/bash
# deploy-dev.sh
echo pull # 获取最新版代码

# 拉取代码
cd html
git pull

# 下面的先注释，等配置完 docker-compose 和 Nginx 再打开
# 强制重新编译容器
cd ..
docker-compose down
docker-compose up -d --force-recreate --build
```

```yml
# docker-compose.yml
# 这里也有坑，version 是和你的 docker-compose版本有关的，如果报错就试试改成 3 或者 3.1
# 打包后存放的文件夹，我的叫dist！！！ 别忘了修改成自己的
version: '2'
services:
  nginx:
    restart: always
    image: nginx
    ports:
      - 80:80
    volumes:
      - ./nginx/conf/:/etc/nginx/conf.d
      - ./html/:/var/www/html/
```

```conf
# nginx/conf/docker.conf
# 80端口是 Nginx 容器的，后面会做映射
server {
listen 80;
location / {
root /var/www/html;
index index.html index.htm;
}
}
```

```javascript
// webhook.js
const http = require('http');
const createHandler = require('github-webhook-handler'); //这个插件使用前先安装 npm i github-webhook-handler -D

function run_cmd(cmd, args, callback) {
  var spawn = require('child_process').spawn;
  var child = spawn(cmd, args);
  var resp = '';
  child.stdout.on('data', function (buffer) {
    resp += buffer.toString();
  });
  child.stdout.on('end', function () {
    // console.log('Deploy 完成');
    callback(resp);
  });
}

const handler = createHandler({
  path: '/resume-hook', // url 后缀
  secret: 'webhook', // 你的密码
});

// 注意要在阿里云安全组里面添加开放端口
// 还要在ubuntu防火墙关闭对应端口
http
  .createServer((req, res) => {
    handler(req, res, (err) => {
      res.statusCode = 404;
      res.end('no such location');
    });
  })
  .listen(7778, () => {
    console.log('Webhook listen at 7778');
  });

handler.on('error', (err) => {
  console.error('Error', err.message);
});

// 拦截push，执行 Deploy 脚本
handler.on('push', function (event) {
  console.log(
    'Received a push event for %s to %s',
    event.payload.repository.name,
    event.payload.ref
  );
  // 分支判断
  if (event.payload.ref === 'refs/heads/gh-pages') {
    // console.log('deploy gh-pages ...');
    run_cmd('sh', ['./autoDeploy.sh'], function (text) {
      console.log(text);
    });
  }
});
```
