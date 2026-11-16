# 🤖 Agentic AI Projects

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.5-1C3C3C?logo=langchain&logoColor=white)
![uv](https://img.shields.io/badge/managed%20with-uv-DE5FE9)

Hands-on projects where I build **AI agents**: LLM apps that decide which tools to call, fetch
information, and take actions. I care as much about making them **safe and testable** as about
making them work.

---

## 📂 Projects

| Project | What it does | Highlights |
|---|---|---|
| [**🛎️ Desk App**](desk-app/) | A customer-support agent for an online shop. It answers order questions, handles refunds and searches policy documents. | Tool calling · RAG · Guardrails · Human approval · Memory · Tests with no API key |

> 👉 **Start with [`desk-app/`](desk-app/)**. Its README explains the design, the safety choices and how to run it.

---

## 🛠️ Tech stack

- **Language:** Python 3.15
- **Agent framework:** LangChain 1.x (`create_agent`, middleware), LangGraph (checkpointing, interrupts)
- **LLM provider:** Groq (`gpt-oss-120b`); the code can also use OpenAI and Google Gemini
- **Retrieval:** LangChain text splitters and an in-memory vector store
- **Testing:** pytest with scripted stand-in models
- **Tooling:** [uv](https://docs.astral.sh/uv/) for fast, reproducible environments

---

## 🧱 Repository layout

Each project is its **own uv project**, with its own `pyproject.toml`, `uv.lock` and `.venv`, so
package versions never clash between projects.

```text
agentic-ai/
├── .env              # API keys (not committed); every project finds it through load_dotenv()
├── .python-version   # Python version shared by all projects
└── desk-app/         # project 1: support desk agent
```

---

## 🚀 Quick start

```sh
git clone https://github.com/Abhi-NSUT/agentic-ai.git
cd agentic-ai
echo "GROQ_API_KEY=your_key_here" > .env

cd desk-app
uv sync
uv run desk-app
```

### Add a new project

```sh
uv init --package my-project
cd my-project
uv add langchain
uv run my-project
```
