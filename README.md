
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

The OwlMind Platform is a foundational experimentation environment engineered by The Generative Intelligence Lab. It serves as a pedagogical sandbox where students and researchers can interrogate the mechanics of Generative Intelligence. By implementing a standardized CLI over a provider-agnostic abstraction layer, OwlMind enables learners to conduct comparative analyses of LLM behaviors through interchangeable parameters within a controlled, observable setup

Installation:

```bash
pip install owlmind
```

---

## Commands

#### Configuration 
Control OwlMind via environment variables

```bash
# OLLAMA_HOST -- URL of the Ollama server
export OLLAMA_HOST=http://localhost:11434

# OLLAMA_MODEL -- Default model for queries	llama3
export OLLAMA_MODEL=llama3
```


#### System Audit
View your current environment configuration

```bash
owlmind info
```

#### Connectivity Check 
Verify if your model provider is online.

```bash
owlmind ping
```


#### Generation
Run inference with full control over sampling parameters.

```bash
owlmind query "How do AI-driven organizations scale?" --temp 1.2 --ctx-size 4096
```

#### Prompt Loading (@file syntax)
OwlMind supports loading prompts directly from files using the @ prefix. This is ideal for long-form instructions or code analysis.

```bash
owlmind query @my_prompt.txt
```

Explicit Flag:

```bash
owlmind query --input research_paper.md
```

