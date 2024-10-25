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

```shell
git clone https://github.com/RedwindA/GPT-sovits-2-OpenAI
cd GPT-sovits-2-OpenAI
cp .env.example .env
```

使用Docker 启动：

```shell
docker compose up -d
```

## 注意事项

没有实现鉴权，开放到公网请谨慎