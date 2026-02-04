
<!---
<img src="https://generativeintelligencelab.ai/images/owlmind-icon-bw.png" height=100>
--->

# OwlMind 

<br/>
<div align="left">
  <img src="https://img.shields.io/badge/Generative_AI-Lab-blueviolet?style=for-the-badge&logo=openai&logoColor=white" alt="Generative AI" />
  <img src="https://img.shields.io/badge/Ollama-Supported-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.14" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</div>

---

## Overview

The OwlMind Framework provides an experimentation environment and pedagogical sandbox for [Generative Intelligence Systems](https://medium.com/lecture-notes-on-generative-intelligence/generative-intelligence-systems-5b23727acffe). The platform defines a standardized programming structure and command-line interface across multiple architectural layers. This structure enables comparative experiments around the behaviors of Large Language Models (LLMs), AI pipelines, and component-level configurations.

#### Installation:

```bash
pip install owlmind
```

Verify the installation:

```bash
owlmind --version
```


#### Configuration 

OwlMind can be configured using environment variables.

```bash
# OLLAMA_HOST -- URL of the Ollama server
export OLLAMA_HOST=http://localhost:11434

# OLLAMA_MODEL -- Default model for queries	llama3
export OLLAMA_MODEL=llama3
```

OwlMind automatically loads .env files from the working directory.

```bash
# File: .env
# .env files are loaded automatically 

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama
```


#### Command-Line Interface

```
owlmind
usage: owlmind [-h] [--version] [--debug] [--url URL] {ping,info,query} ...
owlmind: error: the following arguments are required: command
```

You can access help at any level using --help (or -h):

```
owlmind --help
```

```
owlmind query --help
```



#### Connectivity Check 

Verify that your model provider is reachable.

```bash
owlmind ping
```

Expected output:
```bash
Status: ONLINE (Host: http://localhost:11434)
```

#### Environment & Capability Information

Inspect your runtime environment, available models, and supported parameters.

```bash
owlmind info
```

Example output:

```bash
----------------------------------------
Status  : online
Host    : http://minipc:11434
Model   : llama3
----------------------------------------
Available Models: 5
  - gpt-oss:latest
  - gemma:latest
  - tinyllama:latest
  - llama3:latest
  - llama3.2:latest
----------------------------------------
Accepted Parameters (9):
  - temperature
  - top_p
  - seed
  - num_ctx
  - num_predict
  - repeat_penalty
  - top_k
  - stop
  - system
----------------------------------------
```

#### Simple Query

Runs a single inference using the default model and prints the response.

```bash
owlmind query "How do AI-driven organizations scale?" 
```


#### Activating Debug 

Runs the query with debug-level logging enabled for internal execution visibility.

```bash
owlmind --debug query "How do AI-driven organizations scale?"
```


#### Working with Querying Parameters

Override inference parameters while keeping the default model.

```bash
owlmind query "How do AI-driven organizations scale?" -p temperature=1.2,num_ctx=4096
```

Parameters can also be provided incrementally:

```bash
owlmind query "Explain transformers" \
  -p temperature=0.8 \
  -p num_ctx=4096
```

To see the full list of supported parameters, run:

```bash
owlmind info
```

#### Querying Different Models

Run a query using a specific model and custom parameters.

```bash
owlmind query "How do AI-driven organizations scale?" \
  -m gpt-oss \
  -p temperature=1.2,num_ctx=4096
```
This allows rapid comparison between models without changing code.


#### Prompt Loading

OwlMind supports loading prompts directly from files.

##### Using the @ prefix

```bash
owlmind query @my_prompt.txt
```

##### Using an explicit input flag

```bash
owlmind query --input research_paper.md
```



