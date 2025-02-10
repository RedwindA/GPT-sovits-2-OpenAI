# 将GPT-sovits转换为OpenAI TTS格式

## 前言

许多开源项目只支持常见的大厂TTS API。本项目旨在通过转换API请求来适配支持OpenAI TTS的客户端。

## 准备

根据原项目中的api.py自带的文档启动GPT-sovits的api服务。如果你使用的是整合包，务必以如下格式在整合包的根目录中启动：

```shell
runtime\python.exe api.py <省略后续的参数>
```

## 使用方法

克隆本仓库并修改配置

```Linux shell
git clone https://github.com/RedwindA/GPT-sovits-2-OpenAI
cd GPT-sovits-2-OpenAI
cp .env.example .env
cp config.yaml.example config.yaml
```

对于Windows，前两行不变，最后两行改为：

```cmd
copy .env.example .env
copy config.yaml.example config.yaml
```

使用Docker 启动：

```shell
docker compose up -d
```

启动后，本服务就作为一个OpenAI TTS的API服务运行。base_url为http://your_ip:5000/v1，完整的url为http://your_ip:5000/v1/audio/speech，填入应用中即可。

## 注意事项

1. **由于使用了docker，请确保容器能够正确访问GPT-sovits API。**
如果两者运行在同一台宿主机上，而GPT-sovits API是直接运行的（非docker），环境变量应该是`BACKEND_URL=http://host.docker.internal:9880`（目前的默认配置）。你也可以通过docker compose将两者组合在同一个docker网络中。

2. 如果不配置API_KEY，则服务可被所有人访问

## 未来开发计划

1. 支持流式传输
2. ~~移植或合并v2以支持不同的切分文本策略~~ 已在apiv2分支中实现