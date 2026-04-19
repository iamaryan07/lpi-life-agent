# agents.py
import os
import json
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
# LPI TOOL 1 — LPI_Wikipedia
# Queries Wikipedia for general knowledge and definitions.
# Called via: LPI_Wikipedia.run(query)
# =========================
def _lpi_wikipedia_run(query: str) -> str:
    """
    LPI_Wikipedia tool handler.
    Fetches general knowledge from Wikipedia for a given query.
    Returns a JSON string with tool_name, status, and data.
    """
    try:
        result = wiki_runner.run(query)
        if not result or result.strip() == "":
            result = "No Wikipedia article found for this query."
        return json.dumps({
            "tool_name": "LPI_Wikipedia",
            "status": "success",
            "data": result
        })
    except Exception as e:
        return json.dumps({
            "tool_name": "LPI_Wikipedia",
            "status": "error",
            "data": f"LPI_Wikipedia failed: {str(e)}"
        })

# Register as a named LangChain Tool — name="LPI_Wikipedia"
LPI_Wikipedia = Tool(
    name="LPI_Wikipedia",
    func=_lpi_wikipedia_run,
    description=(
        "LPI tool 1: queries Wikipedia for general knowledge and definitions. "
        "Input: a search query string. "
        "Output: JSON string with tool_name='LPI_Wikipedia', status, and data."
    )
)

# =========================
# LPI TOOL 2 — LPI_Arxiv
# Queries Arxiv for research papers and technical insights.
# Called via: LPI_Arxiv.run(query)
# =========================
def _lpi_arxiv_run(query: str) -> str:
    """
    LPI_Arxiv tool handler.
    Fetches research papers from Arxiv for a given query.
    Returns a JSON string with tool_name, status, and list of papers.
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=3,
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
            return json.dumps({
                "tool_name": "LPI_Arxiv",
                "status": "empty",
                "data": []
            })
        return json.dumps({
            "tool_name": "LPI_Arxiv",
            "status": "success",
            "data": papers
        })
    except Exception as e:
        return json.dumps({
            "tool_name": "LPI_Arxiv",
            "status": "error",
            "data": f"LPI_Arxiv failed: {str(e)}"
        })

# Register as a named LangChain Tool — name="LPI_Arxiv"
LPI_Arxiv = Tool(
    name="LPI_Arxiv",
    func=_lpi_arxiv_run,
    description=(
        "LPI tool 2: queries Arxiv for research papers and technical insights. "
        "Input: a search query string. "
        "Output: JSON string with tool_name='LPI_Arxiv', status, and list of paper dicts."
    )
)

# ---- All registered LPI tools ----
LPI_TOOLS = [LPI_Wikipedia, LPI_Arxiv]

# =========================
# SYNTHESIS
# =========================
def synthesize(query: str, wiki_data: str, arxiv_data: list) -> str:
    """Combine LPI_Wikipedia and LPI_Arxiv outputs using the LLM."""
    try:
        arxiv_text = ""
        for i, p in enumerate(arxiv_data, 1):
            arxiv_text += f"\nPaper {i}: {p['title']}\nSummary: {p['summary']}\n"

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
- bullet points summarising what LPI_Wikipedia provided

ARXIV CONTRIBUTION:
- bullet points with paper references from LPI_Arxiv

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

    # --- Call LPI TOOL 1: LPI_Wikipedia ---
    print("\n[Calling LPI_Wikipedia.run()...]")
    try:
        wiki_raw = LPI_Wikipedia.run(query)
        wiki_result = json.loads(wiki_raw)
    except Exception as e:
        wiki_result = {"tool_name": "LPI_Wikipedia", "status": "error", "data": str(e)}
    print(f"LPI_Wikipedia status: {wiki_result.get('status')}")

    # --- Call LPI TOOL 2: LPI_Arxiv ---
    print("\n[Calling LPI_Arxiv.run()...]")
    try:
        arxiv_raw = LPI_Arxiv.run(query)
        arxiv_result = json.loads(arxiv_raw)
    except Exception as e:
        arxiv_result = {"tool_name": "LPI_Arxiv", "status": "error", "data": str(e)}
    print(f"LPI_Arxiv status: {arxiv_result.get('status')}")

    # --- Synthesis ---
    print("\n[Synthesizing with LLM...]")
    wiki_data = wiki_result.get("data", "No data available.")
    arxiv_data = arxiv_result.get("data", [])
    if not isinstance(arxiv_data, list):
        arxiv_data = []

    answer = synthesize(query, wiki_data, arxiv_data)

    return {
        "answer": answer,
        "tool_trace": {
            "LPI_Wikipedia": wiki_result.get("status", "unknown"),
            "LPI_Arxiv": arxiv_result.get("status", "unknown"),
        },
        "sources": {
            "Wikipedia": str(wiki_data)[:300],
            "Arxiv": arxiv_data
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
    print("Wikipedia (LPI_Wikipedia):")
    print(result["sources"]["Wikipedia"])
    print("\nArxiv Papers (LPI_Arxiv):")
    for p in result["sources"]["Arxiv"]:
        print(f"  - {p.get('title', 'Unknown')} | {p.get('url', '')}")

if __name__ == "__main__":
    try:
        res = run_agent("What is machine learning?")
        print_result(res)
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
