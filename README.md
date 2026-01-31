
<!---
<img src="https://generativeintelligencelab.ai/images/owlmind-banner.png" width=800>
--->

# OwlMind

<div align="left">
  <img src="https://img.shields.io/badge/Generative_AI-Lab-blueviolet?style=for-the-badge&logo=openai&logoColor=white" alt="Generative AI" />
  <img src="https://img.shields.io/badge/Ollama-Supported-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.14" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</div>

---

## Overview

The OwlMind Framework provides an experimentation environment and pedagogical sandbox for studying [Generative Intelligence Systems](https://medium.com/lecture-notes-on-generative-intelligence/generative-intelligence-systems-5b23727acffe). The plaform defines a standardized programming structure and command-line interface across multiple architectural layers. This structure enables comparative experiments around the behaviours of LLMS, AI pipelines, and component-level configurations.

#### Installation:

```bash
pip install owlmind
```

#### Configuration 
Control OwlMind via environment variables

```bash
# OLLAMA_HOST -- URL of the Ollama server
export OLLAMA_HOST=http://localhost:11434

# OLLAMA_MODEL -- Default model for queries	llama3
export OLLAMA_MODEL=llama3
```

#### Information
View your current environment configuration

```bash
owlmind info
```

#### Connectivity 
Verify if your model provider is online.

```bash
owlmind ping
```

#### Generation with Parameters
Run inference with full control over sampling parameters.

```bash
owlmind query "How do AI-driven organizations scale?" --temp 1.2 --ctx-size 4096
```

Other parameters:

```bash
$ owlmind query --help
usage: owlmind query [-h] [--input INPUT_FILE] [--model MODEL] [--temp TEMPERATURE] [--top-k TOP_K]
                     [--top-p TOP_P] [--max-tokens MAX_TOKENS] [--ctx-size NUM_CTX]
                     [prompt]

positional arguments:
  prompt                Prompt text or @filename

options:
  -h, --help            show this help message and exit
  --input, -i INPUT_FILE
                        Explicit path to a prompt file
  --model, -m MODEL
  --temp, -t TEMPERATURE
  --top-k, -k TOP_K
  --top-p, -p TOP_P
  --max-tokens, -n MAX_TOKENS
  --ctx-size, -c NUM_CTX
```


#### Prompt Loading
OwlMind supports loading prompts directly from files using the @ prefix. This is ideal for long-form instructions or code analysis.

```bash
owlmind query @my_prompt.txt
```

Explicit Flag:

```bash
owlmind query --input research_paper.md
```


