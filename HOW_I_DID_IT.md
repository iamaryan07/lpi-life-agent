# HOW_I_DID_IT

## Approach

I built a deterministic pipeline instead of relying on autonomous agents.

Steps:
1. Accept user query
2. Call two LPI tools:
   - LPI_Wikipedia
   - LPI_Arxiv
3. Process outputs
4. Use LLM to synthesize
5. Return structured answer with traceability

## Key Decisions

- Explicit tool calls instead of agent-based tool selection
- Structured output to guarantee explainability
- Combined general + research sources

## Challenges

- Small model ignored Arxiv insights initially
- Fixed using strict prompt constraints

## Improvements

- Use stronger LLM (Llama 8B)
- Add ranking for research papers
- Improve extraction of insights
