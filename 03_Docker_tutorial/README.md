
## 一、安装 Docker
### 1. 下载 Docker 安装包
### 2. 安装到指定路径
1. 使用管理员权限运行 `PowerShell`
2. 切换到安装包所在目录
3. 执行命令，以 `E:\Development_Tool\docker` 路径为例子
```shell
Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license', '--installation-dir=E:\Development_Tool\docker', '--windows-containers-default-data-root=E:\Development_Tool\docker\windows-containers', '--wsl-default-data-root=E:\Development_Tool\docker\wsl'
```

## 二、基于 Docker 部署 redis-stack
https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-stack/docker/


### 1. 拉取 Redis 镜像
```shell
docker pull redis/redis-stack
```
### 2. 运行 Redis 容器
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

```shell
docker run 
redis/redis-stack:latest     # 镜像名称和标签
-d                           # 后台运行
--name redis-stack           # 给容器命名
-p 6379:6379                 # 映射端口(本机端口：容器端口)，Redis
-p 8001:8001                 # 映射端口(本机端口：容器端口)，RedisInsight
```
执行后：
- 程序可以通过 `localhost:6379` 连接 Redis；
- 浏览器可以打开 `http://localhost:8001` 使用 RedisInsight 管理数据。

## 三、基于 Docker 部署 FastGPT
源码位置：https://github.com/1abring/FastGPT

https://doc.fastgpt.cn/zh-CN/self-host/deploy/docker