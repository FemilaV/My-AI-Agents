# GhostWriter 👻✍️  
### Agentic AI Blog Generation System

GhostWriter is a production-style agentic AI system that autonomously researches, writes, and edits long-form blog content using a hybrid LLM stack (local + OpenAI).

The project is designed with **cost efficiency, performance instrumentation, and deterministic outputs** in mind — focusing on real-world constraints rather than demos.

---

## 🚀 Features

- 🔍 Web research using Tavily Search + Crawl4AI
- 🧠 Multi-agent architecture (Researcher → Writer → Editor)
- ⚡ Cost-aware LLM routing
- ⏱️ End-to-end performance timing
- 🛡️ Safe, single-call OpenAI usage
- 🖥️ Local LLM inference via Ollama

---

## 🧠 Architecture Overview

User Topic
   │
   ▼
┌──────────────────────┐
│   Researcher Agent   │
│  (Tavily + Crawl4AI) │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────────────┐
│ Fast Local LLM (phi-3 mini)  │
│ • Summarize research         │
│ • Generate blog outline      │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ Writer Agent (Local LLM)     │
│ llama3.2 via Ollama          │
│ • Full blog generation       │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ Final Editor Agent (OpenAI)  │
│ GPT-4o (single paid call)    │
│ • Grammar, clarity, polish   │
└─────────┬────────────────────┘
          │
          ▼
     Final Blog Output

---

## 🤖 Model Strategy

| Task | Model | Reason |
|----|----|----|
| Research + Outline | `phi3:mini` (local) | Fast, cheap, structured output |
| Writing | `llama3.2` (local) | Long-form generation |
| Editing | `gpt-4o` | High-quality polish (1 call only) |

This minimizes cost while maintaining output quality.

---

## ⏱️ Performance (Typical Run)

| Stage | Time |
|----|----|
| Research | ~3.5 minutes |
| Writing | ~2.3 minutes |
| Editing | ~6 seconds |
| **Total** | **~5–6 minutes** |

---

## 🛠️ Tech Stack

- Python
- LangChain
- Ollama (local LLMs)
- Tavily Search API
- Crawl4AI
- OpenAI API

---

## ▶️ How to Run

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull local models
ollama pull llama3.2
ollama pull phi3:mini

# Run
python main.py


