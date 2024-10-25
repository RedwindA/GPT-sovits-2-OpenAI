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
```

Start with Docker:

```shell
docker compose up -d
```

## Important Notes

Authentication is not implemented, be cautious when exposing to public network

**Since Docker is used, make sure the container can properly access the GPT-sovits API**

If both are running on the same host machine, and GPT-sovits API is running directly (non-docker), the environment variable should be `BACKEND_URL=http://host.docker.internal:9880` (current default configuration)
You can also combine both in the same docker network through docker compose.
