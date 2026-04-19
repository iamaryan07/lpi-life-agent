# How I Built the Explainable Knowledge Agent

## Step-by-Step Process

### Phase 1: Understanding the Requirements

I started by carefully understanding the Level 3 requirements. The goal was not just to generate answers, but to build a transparent pipeline where:

- multiple tools are used
- outputs are processed
- every part of the answer is traceable

This shifted the focus from “just answering questions” to building an explainable system.

### Phase 2: Defining the Approach

Instead of building a generic chatbot, I designed a system that combines:

- general knowledge (Wikipedia)
- research-level insights (Arxiv)

This ensures that answers are both:

- easy to understand
- grounded in real research

### Phase 3: Tool Selection Strategy

I intentionally chose two complementary tools:

- **WikipediaQueryRun** – Provides clear definitions and general explanations
- **Arxiv API** – Provides research papers with summaries, authors, and links

This combination allows the agent to move beyond basic answers and include real-world research context.

### Phase 4: Building the Retrieval Layer

I implemented separate functions:

- `run_wikipedia()` → retrieves structured text from Wikipedia
- `run_arxiv()` → retrieves relevant research papers

Instead of relying on an autonomous agent, I explicitly called both tools to ensure:

- consistency
- reliability
- compliance with Level 3 requirements

### Phase 5: Designing the Synthesis Layer

The key challenge was combining outputs from both tools.

I built a structured prompt that forces the model to:

- use both sources
- include at least one research insight
- explain how research extends the basic definition

This ensures the system performs actual synthesis, not just summarization.

### Phase 6: Structured Output Design

To satisfy explainability, I enforced a strict format:

- **Combined Answer** → integrates both sources
- **Wikipedia Contribution** → what came from general knowledge
- **Arxiv Contribution** → specific insights from papers

This makes it easy to trace:

- which part of the answer came from which tool

### Phase 7: Handling Tool Outputs

I observed that raw outputs from tools can be noisy or too long.

To address this:

- Wikipedia output is truncated to relevant length
- Arxiv results are structured into:
  - title
  - authors
  - summary
  - URL

This improves clarity and makes the data usable for synthesis.

## Problems I Faced

### 1. Weak Synthesis from the Model

Using a small model (Llama 3.2 1B), the output was often:

- repetitive
- biased toward Wikipedia

**Solution:**  
I enforced strict prompt rules like:

- “must include Arxiv insight”
- “do not repeat points”

### 2. Tool Output Overload

Initially, passing full outputs caused:

- irrelevant details
- weaker answers

**Solution:**  
I trimmed and structured tool outputs before sending them to the model.

### 3. Ensuring Real Explainability

Early versions only listed sources without linking them to content.

**Solution:**  
I added explicit sections:

- Wikipedia contribution
- Arxiv contribution

### 4. Arxiv API Warnings

The API raised deprecation warnings during execution.

**Solution:**  
Handled warnings and ensured they do not affect output clarity.

## What I Learned

### 1. Combining Tools Improves Quality
- Wikipedia alone → basic explanation
- Arxiv alone → technical but fragmented
- Together → meaningful, balanced answers

### 2. Explainability Must Be Designed

It doesn’t happen automatically.  
You must explicitly structure:

- outputs
- prompts
- source mapping

### 3. Simpler Pipelines Are More Reliable

Using explicit tool calls instead of autonomous agents:

- reduces unpredictability
- improves consistency

### 4. Prompt Design Controls Output Quality

The biggest improvement came from:

- structured instructions
- strict formatting

Not from changing the model.

### 5. Model Size Affects Quality, Not Validity

Even with a smaller model:

- the system works
- requirements are satisfied

The pipeline matters more than the model.

## Final Thoughts

This project demonstrates that building an effective AI system is not just about generating answers, but about:

- retrieving real data
- combining multiple perspectives
- making outputs transparent and traceable

The final system is simple, but it clearly shows:

- how information flows
- how tools contribute
- how answers are constructed

This aligns directly with the goal of Explainable AI in Level 3.
