"""
Track A — Level 3 Agent
LPI Tools used:
  1. Wikipedia  (general knowledge)
  2. Arxiv      (research papers)
LLM: Anthropic Claude (claude-sonnet-4-20250514) via the Anthropic Python SDK
"""

import os
import textwrap
import arxiv

from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

# ── Llama client ──────────────────────────────────────────────────────────
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm_endpoint = HuggingFaceEndpoint(
    repo_id='meta-llama/Llama-3.2-1B-Instruct',
    task='text-generation'
)

llm = ChatHuggingFace(llm=llm_endpoint)

# ── Tool 1: Wikipedia ─────────────────────────────────────────────────────────
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500))


def run_wikipedia(query: str) -> str:
    """Query Wikipedia and return a plain-text snippet."""
    try:
        return wiki_tool.run(query)
    except Exception as exc:
        return f"[Wikipedia error: {exc}]"


# ── Tool 2: Arxiv ─────────────────────────────────────────────────────────────
def run_arxiv(query: str, max_results: int = 3) -> list[dict]:
    """Search Arxiv and return a list of {title, authors, url, summary} dicts."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers = []
        for paper in search.results():
            papers.append(
                {
                    "title": paper.title,
                    "authors": [a.name for a in paper.authors[:3]],
                    "url": paper.entry_id,
                    "summary": paper.summary[:500],
                }
            )
        return papers
    except Exception as exc:
        return [{"title": "Error", "authors": [], "url": "", "summary": str(exc)}]


def synthesize_with_llama(query: str, wiki_text: str, arxiv_papers: list[dict]) -> str:
    arxiv_block = ""
    for i, p in enumerate(arxiv_papers, 1):
        arxiv_block += f"""
Paper {i}:
  Title   : {p['title']}
  Authors : {', '.join(p['authors'])}
  URL     : {p['url']}
  Summary : {p['summary']}
""".rstrip()

    prompt = f"""
You are a research assistant that synthesizes knowledge from multiple sources.

You will be given:
- SOURCE 1: Wikipedia (general knowledge)
- SOURCE 2: Arxiv papers (research insights)

Rules:
1. Write a COMBINED ANSWER using BOTH sources
2. Include at least one concrete insight from Arxiv
3. Show how research extends or refines the basic definition
4. Then add:

WIKIPEDIA CONTRIBUTION:
- bullet points

ARXIV CONTRIBUTION:
- bullet points with paper titles

Be concise. Do NOT repeat points.

---

Question: {query}

SOURCE 1 (Wikipedia):
{wiki_text}

SOURCE 2 (Arxiv):
{arxiv_block}
"""

    response = llm.invoke(prompt)
    return response.content


def run_agent(query: str) -> dict:
    """
    Full pipeline:
      1. Accept user question
      2. Query Wikipedia  (LPI Tool 1)
      3. Query Arxiv      (LPI Tool 2)
      4. Synthesize with Claude LLM
      5. Return answer + full source citations
    """
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")

    # Step 2 – Wikipedia
    print("\n[Tool 1 / Wikipedia] Searching …")
    wiki_result = run_wikipedia(query)
    print(f"  → Retrieved {len(wiki_result)} characters")

    # Step 3 – Arxiv
    print("\n[Tool 2 / Arxiv] Searching …")
    arxiv_results = run_arxiv(query)
    print(f"  → Retrieved {len(arxiv_results)} papers")

    # Step 4 – LLM synthesis
    print("\n[LLM / Claude] Synthesizing answer …")
    answer = synthesize_with_llama(query, wiki_result, arxiv_results)

    result = {
        "query": query,
        "answer": answer,
        "sources": {
            "Wikipedia": {
                "tool": "WikipediaQueryRun (langchain-community)",
                "snippet": wiki_result[:400] + ("…" if len(wiki_result) > 400 else ""),
            },
            "Arxiv": {
                "tool": "arxiv Python SDK",
                "papers": [
                    {
                        "title": p["title"],
                        "authors": p["authors"],
                        "url": p["url"],
                    }
                    for p in arxiv_results
                ],
            },
        },
    }
    return result


def print_result(result: dict) -> None:
    print(f"\n{'='*60}")
    print("ANSWER")
    print(f"{'='*60}")
    print(result["answer"])

    print(f"\n{'='*60}")
    print("SOURCES  (explainability trace)")
    print(f"{'='*60}")

    wiki = result["sources"]["Wikipedia"]
    print(f"\n[Wikipedia]  tool: {wiki['tool']}")
    print(f"  Snippet: {wiki['snippet']}")

    arxiv_src = result["sources"]["Arxiv"]
    print(f"\n[Arxiv]  tool: {arxiv_src['tool']}")
    for i, p in enumerate(arxiv_src["papers"], 1):
        print(f"  Paper {i}: {p['title']}")
        print(f"    Authors : {', '.join(p['authors'])}")
        print(f"    URL     : {p['url']}")


if __name__ == "__main__":
    query = "What is machine learning?"
    result = run_agent(query)
    print_result(result)