# autoDeploy.sh
#!/bin/bash
# deploy-dev.sh
echo Deploy Project # 获取最新版代码

# 拉取代码
git pull

# 下面的先注释，等配置完 docker-compose 和 Nginx 再打开
# 强制重新编译容器
docker-compose down
docker-compose up -d --force-recreate --build
