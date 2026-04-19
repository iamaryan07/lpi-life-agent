# agents.py
import os
import arxiv
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool

load_dotenv()

# ---- LLM ----
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm_endpoint = HuggingFaceEndpoint(
    repo_id='meta-llama/Llama-3.2-1B-Instruct',
    task='text-generation'
)
llm = ChatHuggingFace(llm=llm_endpoint)

# ---- Base Wikipedia runner ----
wiki_runner = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500)
)

# =========================
# LPI TOOL 1 — Wikipedia
# =========================
def _lpi_wikipedia_run(query: str) -> dict:
    """Call the LPI_Wikipedia tool and return structured output."""
    try:
        result = wiki_runner.run(query)
        if not result or result.strip() == "":
            result = "No Wikipedia article found for this query."
        return {
            "tool_name": "LPI_Wikipedia",
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "tool_name": "LPI_Wikipedia",
            "status": "error",
            "data": f"LPI_Wikipedia failed: {str(e)}"
        }

LPI_Wikipedia = Tool(
    name="LPI_Wikipedia",
    func=_lpi_wikipedia_run,
    description=(
        "LPI tool that queries Wikipedia for general knowledge and definitions. "
        "Input: a search query string. "
        "Output: a structured dict with tool_name, status, and data."
    )
)

# =========================
# LPI TOOL 2 — Arxiv
# =========================
def _lpi_arxiv_run(query: str, max_results: int = 3) -> dict:
    """Call the LPI_Arxiv tool and return structured output."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers = []
        for paper in search.results():
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors[:3]],
                "url": paper.entry_id,
                "summary": paper.summary[:400],
            })
        if not papers:
            return {
                "tool_name": "LPI_Arxiv",
                "status": "empty",
                "data": []
            }
        return {
            "tool_name": "LPI_Arxiv",
            "status": "success",
            "data": papers
        }
    except Exception as e:
        return {
            "tool_name": "LPI_Arxiv",
            "status": "error",
            "data": f"LPI_Arxiv failed: {str(e)}"
        }

LPI_Arxiv = Tool(
    name="LPI_Arxiv",
    func=_lpi_arxiv_run,
    description=(
        "LPI tool that queries Arxiv for research-level insights and papers. "
        "Input: a search query string. "
        "Output: a structured dict with tool_name, status, and list of paper dicts."
    )
)

# ---- Registered LPI tools ----
LPI_TOOLS = [LPI_Wikipedia, LPI_Arxiv]

# =========================
# SYNTHESIS
# =========================
def synthesize(query: str, wiki_result: dict, arxiv_result: dict) -> str:
    """Combine LPI tool outputs using the LLM."""
    try:
        wiki_data = wiki_result.get("data", "No data available.")
        arxiv_data = arxiv_result.get("data", [])

        arxiv_text = ""
        if isinstance(arxiv_data, list):
            for i, p in enumerate(arxiv_data, 1):
                arxiv_text += f"\nPaper {i}: {p['title']}\nSummary: {p['summary']}\n"
        else:
            arxiv_text = str(arxiv_data)

        prompt = f"""
You MUST use both sources below.

Question:
{query}

Wikipedia (from LPI_Wikipedia tool):
{wiki_data}

Arxiv Papers (from LPI_Arxiv tool):
{arxiv_text}

OUTPUT FORMAT:

COMBINED ANSWER:
- Must integrate both sources
- Must include at least one research insight from Arxiv

WIKIPEDIA CONTRIBUTION:
- bullet points summarising what Wikipedia provided

ARXIV CONTRIBUTION:
- bullet points with paper references

TOOL TRACE:
- LPI_Wikipedia → what it provided
- LPI_Arxiv → what it provided

Do NOT repeat content between sections.
"""
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Synthesis failed: {str(e)}"

# =========================
# PIPELINE
# =========================
def run_agent(query: str) -> dict:
    print("\n==============================")
    print("QUERY:", query)
    print("==============================")

    # --- LPI TOOL 1: Wikipedia ---
    print("\n[Calling LPI_Wikipedia...]")
    wiki_result = LPI_Wikipedia.func(query)
    print(f"LPI_Wikipedia status: {wiki_result.get('status')}")

    # --- LPI TOOL 2: Arxiv ---
    print("\n[Calling LPI_Arxiv...]")
    arxiv_result = LPI_Arxiv.func(query)
    print(f"LPI_Arxiv status: {arxiv_result.get('status')}")

    # --- Synthesis ---
    print("\n[Synthesizing with LLM...]")
    answer = synthesize(query, wiki_result, arxiv_result)

    return {
        "answer": answer,
        "tool_trace": {
            "LPI_Wikipedia": wiki_result.get("status", "unknown"),
            "LPI_Arxiv": arxiv_result.get("status", "unknown"),
        },
        "sources": {
            "Wikipedia": str(wiki_result.get("data", ""))[:300],
            "Arxiv": arxiv_result.get("data", [])
        }
    }

# =========================
# PRINT
# =========================
def print_result(result: dict):
    print("\n========== ANSWER ==========\n")
    print(result["answer"])
    print("\n========== TOOL TRACE ==========\n")
    for k, v in result["tool_trace"].items():
        print(f"{k} → {v}")
    print("\n========== SOURCES ==========\n")
    print("Wikipedia:")
    print(result["sources"]["Wikipedia"])
    print("\nArxiv Papers:")
    arxiv_papers = result["sources"]["Arxiv"]
    if isinstance(arxiv_papers, list):
        for p in arxiv_papers:
            print("-", p.get("title", "Unknown"))
    else:
        print(arxiv_papers)

if __name__ == "__main__":
    try:
        res = run_agent("What is machine learning?")
        print_result(res)
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
