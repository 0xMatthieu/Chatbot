# Chatbot

## How to setup:

Create virtual env: ```source python3 -m venv .venv```
Activate virtual env : linux ```source .venv/bin/activate``` or Windows ```.venv\Scripts\activate```
Install packages : ```python3 -m pip install -r requirements.txt```

## llama.cpp :

Documentation : https://python.langchain.com/v0.2/docs/integrations/llms/llamacpp/

### To install
build depends on HW: 

for MAC 2019 with Intel GPU: ```CMAKE_ARGS="-DGGML_METAL=on" FORCE_CMAKE=1 python3 -m pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir```
link : https://github.com/abetlen/llama-cpp-python#installation-with-openblas--cublas--clblast

## Model
To use a model, download the gguf file from HF, add it to .model folder and set the link to desired model in secrets.toml

Example : https://huggingface.co/Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF

## Prompt

Prompt is set in secrets.toml
Example is set to be use with LLama3 models, see https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_rag_agent_llama3_local.ipynb

## Ressources

LLama.cpp and Langchain : https://lolevsky.medium.com/running-locally-llama-and-langchain-accelerated-by-gpu-a52a2fd72d79