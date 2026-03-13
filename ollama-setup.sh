#!/bin/bash
set -e

apt-get update && apt-get install -y curl

curl -L -o /root/.ollama/Qwen3.5-4B-UD-Q4_K_XL.gguf \
  "https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/resolve/main/Qwen3.5-4B-UD-Q4_K_XL.gguf"

echo "FROM /root/.ollama/Qwen3.5-4B-UD-Q4_K_XL.gguf" > /Modelfile

ollama serve &
sleep 10

ollama create qwen3.5-unsloth -f /Modelfile

wait