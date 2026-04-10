# LLM Learning Project

A hands-on project for learning how to fine-tune, maintain, and manage context in Large Language Models.

## Learning Path

| Module | Topic | Key Skills |
|--------|-------|------------|
| 01 | Fundamentals | Tokenization, transformer architecture, HuggingFace basics |
| 02 | Fine-tuning | LoRA/QLoRA, training loops, saving & loading models |
| 03 | RAG | Vector databases, embeddings, retrieval pipelines |
| 04 | Context Management | Keeping knowledge fresh, data pipelines, re-indexing |
| 05 | Evaluation | Measuring quality, benchmarks, tracking drift |

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then launch Jupyter:

```bash
jupyter notebook
```

## Module Overview

### 01 - Fundamentals
Understand how LLMs work under the hood: tokenization, attention, and how to load pre-trained models with HuggingFace Transformers.

### 02 - Fine-tuning
Fine-tune an open-source model on your own data using LoRA (Low-Rank Adaptation) — efficient enough to run on a single GPU or even CPU.

### 03 - RAG (Retrieval-Augmented Generation)
Connect your LLM to an external knowledge base so it can answer questions about up-to-date information without retraining.

### 04 - Context Management
Learn how to keep your RAG knowledge base fresh: automated data pipelines, re-indexing strategies, and handling stale data.

### 05 - Evaluation
Measure whether your model is performing well and detect when it starts to degrade over time.

## Recommended Models (beginner-friendly)
- `distilgpt2` — tiny, fast, good for learning
- `microsoft/phi-2` — small but capable
- `mistralai/Mistral-7B-v0.1` — production quality, needs a GPU

## Resources
- [HuggingFace Docs](https://huggingface.co/docs)
- [PEFT Library (LoRA)](https://huggingface.co/docs/peft)
- [LangChain Docs](https://python.langchain.com)
- [ChromaDB Docs](https://docs.trychroma.com)
