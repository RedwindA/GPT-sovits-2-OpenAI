# Convert GPT-sovits to OpenAI TTS Format

## Introduction

Many open-source projects only support common TTS APIs from major companies. This project aims to adapt clients that support OpenAI TTS by converting API requests.

## Preparation  

Start the GPT-sovits API service according to the documentation in api.py from the original project. If you're using an integrated package, make sure to start it in the root directory in the following format:

```shell
runtime\python.exe api.py <parameters omitted>
```

## Usage

Clone this repository and modify the configuration

```shell
git clone https://github.com/RedwindA/GPT-sovits-2-OpenAI
cd GPT-sovits-2-OpenAI
cp .env.example .env
cp config.yaml.example config.yaml
```

For Windows, the first two lines remain the same, and the last two lines are changed to:

```cmd
copy .env.example .env
copy config.yaml.example config.yaml
```

Start with Docker:

```shell
docker compose up -d
```

After starting, the service runs as an OpenAI TTS API service. The base_url is http://your_ip:5000/v1, and the complete url is http://your_ip:5000/v1/audio/speech, which can be filled in the application.

## Important Notes

1. **Since docker is used, please ensure the container can correctly access the GPT-sovits API.**
If both are running on the same host machine, and GPT-sovits API is running directly (non-dockerized), the environment variable should be `BACKEND_URL=http://host.docker.internal:9880` (current default configuration). You can also combine both using docker compose in the same docker network.

2. If API_KEY is not configured, the service will be accessible by everyone

## Future Development Plans

1. Support streaming
2. Port or merge v2 to support different text segmentation strategies

