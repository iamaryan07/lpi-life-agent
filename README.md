# Explainable Knowledge Agent (LPI) — Level 3

An explainable AI agent that answers user queries by combining **general knowledge (Wikipedia)** and **research-level insights (Arxiv)**.

This project is built for **Track A — Level 3**, where the goal is to create a transparent pipeline that:
- uses multiple tools  
- processes retrieved data  
- clearly shows where each part of the answer comes from  

---

## 🚀 Features

- **Dual-Source Retrieval**
  - Wikipedia → general explanations  
  - Arxiv → research papers and technical insights  

- **Explainable AI**
  - Clearly separates:
    - Wikipedia contribution  
    - Arxiv contribution  
  - Full traceability of sources  

- **Structured Output**
  - Combined Answer  
  - Source Contributions  
  - Source Trace (papers, authors, URLs)  

- **Deterministic Pipeline**
  - Tools are explicitly called (no unreliable agent behavior)

---

## LPI Tools Used

1. **WikipediaQueryRun (langchain-community)**  
   - Retrieves general knowledge and definitions  

2. **Arxiv Python SDK**  
   - Retrieves real research papers with:
     - title  
     - authors  
     - summary  
     - URL  

---

## Architecture
User Query
↓
Wikipedia Tool (general knowledge)
↓
Arxiv Tool (research papers)
↓
LLM (Llama 3.2)
↓
Structured Answer + Source Attribution


---

## Tech Stack

- **Language:** Python 3  
- **LLM:** HuggingFace (`meta-llama/Llama-3.2-1B-Instruct`)  
- **Framework:** LangChain  
- **APIs:**  
  - Wikipedia API  
  - Arxiv API  

---

## Installation

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```

## Usage
python agent.py "What is machine learning?"

---

## Sample Output

COMBINED ANSWER:

Machine learning is defined as algorithms that learn from data (Wikipedia).
Arxiv research extends this by highlighting challenges such as model validation 
and data reliability in real-world applications.

WIKIPEDIA CONTRIBUTION:

- Definition of machine learning
- Statistical foundation

ARXIV CONTRIBUTION:

- Paper: DOME → validation standards
- Paper: Data Sources → reliability challenges

SOURCES:

Wikipedia snippet + Arxiv paper titles, authors, URLs

---

## Project Structure
.
├── agent.py          # Main agent pipeline
├── README.md         # Project documentation
├── requirements.txt  # Dependencies

---

## How This Meets Level 3 Requirements

✔ Accepts user input
✔ Uses at least 2 LPI tools
✔ Processes and combines outputs
✔ Provides clear explainability and traceability

---

## Testing

Tested with:

"What is machine learning?"

Results:

Wikipedia data retrieved successfully
Arxiv papers retrieved (titles, authors, summaries)
LLM combined both sources
Output remained structured and traceable
