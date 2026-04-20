# Explainable Knowledge Agent (LPI)

## Overview

This project implements a Level 3 agent using the Life Programmable Interface (LPI).

The agent answers user queries by:

* selecting relevant tools from the LPI
* retrieving structured knowledge (SMILE methodology + case studies)
* combining multiple sources
* generating a structured, explainable response using an LLM (Qwen via Ollama)

---

## Features

* Multi-tool coordination using LPI
* Query-based tool selection (rule-based logic)
* JSON-RPC communication with LPI server
* Context-aware filtering of case studies (healthcare-focused)
* LLM-based reasoning and response generation
* Structured output format:

  * Understanding
  * SMILE Phases
  * Real-World Application
  * Insight
  * Conclusion

---

## Architecture

```text
User Query
   ↓
Tool Selection (rule-based)
   ↓
LPI Tools (SMILE + Case Studies)
   ↓
Filtering & Parsing
   ↓
LLM (Qwen via Ollama)
   ↓
Structured Final Answer
```

---

## Tools Used

* `smile_overview` → SMILE framework and methodology
* `get_case_studies` → real-world digital twin implementations
* `get_methodology_step` → step-by-step guidance
* `get_insights` → contextual recommendations

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/iamaryan07/lpi-life-agent.git
cd lpi-life-agent
```

---

### 2. Install dependencies

```bash
pip install requests
npm install
npm run build
```

---

### 3. Start LPI server

```bash
node dist/src/index.js
```

---

### 4. Start Ollama and run model

```bash
ollama serve
ollama run qwen2.5:1.5b
```

---

### 5. Run the agent

```bash
python agent.py
```

---

## Example

**Input:**

```text
How are digital twins used in healthcare?
```

**Output includes:**

* Explanation of digital twins
* Relevant SMILE phases
* Real-world healthcare case study
* Insight connecting theory and practice
* Structured conclusion

---

## Design Highlights

* Combines multiple knowledge sources (methodology + real-world data)
* Uses LLM for reasoning instead of rule-based summaries
* Applies filtering to improve relevance of case studies
* Ensures grounded responses by constraining LLM output

---

## Limitations

* Tool selection is rule-based (not fully adaptive)
* Single-pass reasoning (no iterative refinement)
* Depends on LLM quality for final output

---

## Future Improvements

* Add reasoning trace for explainability
* Implement multi-step agent loop
* Improve error handling and robustness
* Expand tool coverage for broader queries

---

## Tech Stack

* Python (agent logic)
* Node.js (LPI server)
* Ollama (local LLM runtime)
* Qwen (LLM model)

---

## License

This project is for educational and evaluation purposes.
