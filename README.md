# Life Optimization Agent (LPI)

An explainable AI system that helps users analyze personal productivity, stress, and focus issues using SMILE methodology and LPI tools.

## What It Does

This agent focuses on applying SMILE methodology to real-world human problems like productivity and mental clarity, instead of generic queries. It takes personal challenges like "I feel unproductive and distracted" and provides structured, actionable analysis based on systematic thinking.

## Why It's Unique

- **Applies SMILE to Human Problems**: Uses the digital twin methodology not for technical systems, but for personal optimization challenges like productivity, focus, and stress management
- **Explainable AI**: Every analysis cites exactly which LPI tools provided which insights, so users can trace the reasoning
- **Uses Real LPI Tools**: Leverages `query_knowledge` and `get_insights` from the actual LPI MCP server instead of static knowledge bases
- **Structured Output**: Provides consistent Problem/Analysis/Suggestions format that's practical and actionable

## How to Run

### Prerequisites

1. **Install Node.js dependencies**:
   ```bash
   cd lpi-developer-kit
   npm run build
   ```

2. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

3. **Pull the model** (if not already available):
   ```bash
   ollama pull qwen2.5:1.5b
   ```

### Usage

```bash
python agent.py "your life optimization question"
```

**Examples**:
```bash
python agent.py "I feel unproductive and distracted"
python agent.py "I struggle with focus during work"
python agent.py "I'm feeling stressed and overwhelmed"
```

## Example Input/Output

**Input**:
```bash
python agent.py "I feel unproductive and distracted"
```

**Output**:
```
============================================================
  Life Optimization Agent (LPI)
  Analyzing: I feel unproductive and distracted
============================================================

[1/2] Querying knowledge base for relevant patterns...
[2/2] Getting system insights for analysis...

Extracting key insights from tool outputs...
Building structured analysis prompt...

Generating analysis with local LLM...

============================================================
  LIFE OPTIMIZATION ANALYSIS
============================================================

Problem:
You're experiencing productivity challenges and difficulty maintaining focus, which is affecting your ability to complete tasks effectively.

Analysis:
Applying SMILE methodology to your productivity challenge reveals several systemic patterns. From a System Definition perspective, your current work environment and habits form an interconnected system where distractions and productivity influence each other. The Requirements Analysis shows you need a structured approach to identify specific distraction triggers and productivity patterns. The Design phase suggests implementing focused work sessions with clear boundaries, while Implementation requires consistent tracking of your focus patterns. Evaluation should measure both output quality and personal energy levels, not just task completion.

Suggestions:
1. Implement a 2-hour focus block system: 90 minutes of deep work followed by 30 minutes of review and reset
2. Track your distraction sources for one week: categorize them as internal (thoughts) vs external (notifications)
3. Design your environment for success: create physical and digital boundaries during focus periods
4. Establish a morning routine that sets clear intentions for the day's priorities

Sources:
[Tool 1: query_knowledge] -> productivity_and_focus_patterns
[Tool 2: get_insights] -> systemic_patterns

============================================================
  PROVENANCE (tools used)
============================================================
  [1] query_knowledge {"query": "I feel unproductive and distracted"}
  [2] get_insights {"query": "I feel unproductive and distracted"}
```

## Architecture

The agent follows a clear three-step process:

1. **Context Gathering**: Queries LPI tools to gather relevant knowledge and insights
2. **Insight Extraction**: Processes raw tool outputs into structured summaries
3. **Structured Analysis**: Uses local LLM to generate consistent, actionable advice

## Error Handling

The agent includes robust error handling for:
- MCP server connection issues
- Ollama connectivity problems
- Tool output parsing errors
- Graceful fallback when LLM generation fails

## Dependencies

- Python 3.10+
- Node.js 18+ (for LPI MCP server)
- Ollama (local LLM runtime)
- `requests` Python package

## Contributing

This agent is designed as a foundation for personal optimization tools. Extensions could include:
- Integration with calendar and productivity apps
- Long-term pattern tracking and visualization
- Personalized recommendation systems
- Multi-modal input (voice, text, biometric data)
