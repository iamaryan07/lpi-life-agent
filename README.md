# LPI Life Agent (Level 3)

## Overview

This project implements a Level 3 agent using the Life Programmable Interface (LPI).
The agent answers user questions by selecting and calling multiple tools from the LPI sandbox, processing their outputs, and generating a structured response.

---

## Features

* Multi-tool usage (`smile_overview`, `get_case_studies`)
* JSON-RPC based communication with LPI
* Dynamic tool argument handling
* Output parsing and filtering (healthcare-specific)
* Structured response generation (summary + analysis)

---

## Tech Stack

* Python (agent logic)
* Node.js (LPI sandbox)
* Subprocess + JSON-RPC communication

---

## Setup

### 1. Clone LPI Developer Kit

```bash
git clone https://github.com/iamaryan07/lpi-developer-kit
cd lpi-developer-kit
npm install
npm run build
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Agent

From the root directory:

```bash
python agent.py
```

Example query:

```text
How are digital twins used in healthcare?
```

---

## How It Works

1. Takes user input
2. Selects relevant tools:

   * `smile_overview`
   * `get_case_studies`
3. Starts LPI server via Node.js
4. Sends JSON-RPC requests
5. Receives and parses tool responses
6. Extracts healthcare-relevant case study
7. Generates final structured answer

---

## Example Output (Simplified)

```
SMILE Framework (Summary):
S.M.I.L.E. — Sustainable Methodology...

Case Study (Summary):
Continuous Patient Twin for Chronic Disease Management
Industry: Healthcare

Analysis:
SMILE structures digital twin development...

Conclusion:
Digital twins enable monitoring, prediction, and intervention...
```

---

## Project Structure

```
lpi-life-agent/
│
├── agent.py
├── README.md
├── HOW_I_DID_IT.md
├── requirements.txt
└── lpi-developer-kit/
```

---

## Notes

* Ensure `lpi-developer-kit` is built before running
* The agent uses the LPI server (`dist/src/index.js`), not the test client
* Tool outputs are filtered for relevance (healthcare use case)

---

## Status

Level 3 implementation complete.

---

## Reflection (Beyond Instructions)

### What I did beyond the instructions
- Filtered tool output to extract only healthcare-relevant case studies instead of returning full raw results.
- Modified tool arguments (`"healthcare digital twin"`) to improve relevance instead of directly passing the user query.
- Implemented manual parsing of nested JSON-RPC responses (`result → content → text`).
- Used the actual LPI server (`dist/src/index.js`) instead of the test client, and handled initialization explicitly.

### What I would do differently next time
- Abstract tool-calling logic into a reusable client instead of mixing it with agent logic.
- Add clearer reasoning traces showing why tools were selected and how outputs were combined.
- Improve summarization by structuring outputs (Challenge, Approach, Outcome) instead of truncation.
- Make tool selection adaptive instead of rule-based.
