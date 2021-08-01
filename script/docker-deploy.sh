#!/bin/bash
docker container stop werobot
docker container rm werobot
docker image rm werobot

docker build -t werobot:latest .
# -v 命令必须用绝对路径，而compose配置可以用相对路径
# 调试用：前台运行
#docker run -p 80:80 --name=werobot -v $(pwd)/app:/deploy/app werobot
# 调试用：后台运行并且不退出
#docker run -dit -p 80:80 --name=werobot -v $(pwd)/app:/deploy/app werobot
docker run -d -p 80:80 --name=werobot -v $(pwd)/app:/deploy/app werobot
