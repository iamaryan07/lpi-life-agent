# Explainable Knowledge Agent (LPI) — Level 3

An explainable AI agent that answers user queries by combining **general knowledge (Wikipedia)** and **research-level insights (Arxiv)**.

Built for **Track A — Level 3** — a transparent pipeline that uses multiple LPI tools, processes retrieved data, and clearly shows where each part of the answer comes from.

---

## 🚀 Features

- **Two Registered LPI Tools**
  - `LPI_Wikipedia` — general explanations and definitions
  - `LPI_Arxiv` — research papers and technical insights
- **Explainable Output** — every answer includes a TOOL TRACE showing which tool contributed what
- **Full Error Handling** — every tool call and LLM call is wrapped in try/except; the pipeline degrades gracefully
- **Deterministic Pipeline** — tools are explicitly called in sequence, no unpredictable agent loop behavior

---

## LPI Tools Used

| Tool | Registered Name | Source | What It Provides |
|------|----------------|--------|-----------------|
| 1 | `LPI_Wikipedia` | Wikipedia API via `WikipediaQueryRun` | General knowledge, definitions, background context |
| 2 | `LPI_Arxiv` | Arxiv SDK | Top 3 relevant research papers with titles, authors, URLs, summaries |

Both are registered as `langchain.tools.Tool` objects with explicit `name=` fields, making them inspectable and composable.

---

## Architecture
User Query
│
├──► LPI_Wikipedia.func(query)   → structured dict (status + data)
│
├──► LPI_Arxiv.func(query)       → structured dict (status + papers list)
│
└──► LLM Synthesis (Llama-3.2-1B via HuggingFace)
│
└──► Structured Answer
├── COMBINED ANSWER
├── WIKIPEDIA CONTRIBUTION
├── ARXIV CONTRIBUTION
└── TOOL TRACE

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Language | Python 3 |
| LLM | `meta-llama/Llama-3.2-1B-Instruct` via HuggingFace |
| Framework | LangChain |
| Tool registration | `langchain.tools.Tool` |
| APIs | Wikipedia API, Arxiv API |

---

## Installation

```bash
git clone https://github.com/iamaryan07/lpi-life-agent.git
cd lpi-life-agent
pip install -r requirements.txt
```

Add a `.env` file with your HuggingFace token:
HUGGINGFACEHUB_API_TOKEN=your_token_here

---

## Usage

```bash
python agents.py
```

Or call `run_agent()` directly:

```python
from agents import run_agent, print_result
res = run_agent("What is machine learning?")
print_result(res)
```

---

## Sample Output
[Calling LPI_Wikipedia...]

LPI_Wikipedia status: success

[Calling LPI_Arxiv...]

LPI_Arxiv status: success
========== ANSWER ==========

COMBINED ANSWER:

Machine learning enables systems to learn from data without explicit programming (Wikipedia).
Recent Arxiv research highlights challenges in model validation and data reliability.

WIKIPEDIA CONTRIBUTION:

Definition and statistical foundation of machine learning

ARXIV CONTRIBUTION:

Paper: DOME — validation standards for ML models
Paper: Data Sources — reliability challenges in real-world applications

TOOL TRACE:

LPI_Wikipedia → provided background definition and context
LPI_Arxiv → provided 3 research papers with technical insights


---

## Project Structure
.
├── agents.py          # Main agent pipeline + LPI tool definitions
├── HOW_I_DID_IT.md    # Solution write-up and design decisions
├── README.md          # Project documentation
└── requirements.txt   # Dependencies

---

## How This Meets Level 3 Requirements

| Requirement | Status |
|-------------|--------|
| Accepts user input | ✅ |
| Queries at least 2 LPI tools | ✅ `LPI_Wikipedia` + `LPI_Arxiv` |
| Tools registered as LangChain Tool objects | ✅ |
| Processes and combines outputs | ✅ |
| Explainability and source traceability | ✅ TOOL TRACE in every answer |
| Error handling | ✅ try/except on every tool + LLM call |
Two things worth noting:

The filename is now agents.py throughout (your original README said agent.py which didn't match the repo)
Added the .env setup instruction since people cloning it will need the HuggingFace token — easy thing that often causes confusion for evaluators trying to run your code
