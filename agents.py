# agent.py

import os
import arxiv
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

# ---- LLM ----
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm_endpoint = HuggingFaceEndpoint(
    repo_id='meta-llama/Llama-3.2-1B-Instruct',
    task='text-generation'
)

llm = ChatHuggingFace(llm=llm_endpoint)

wiki_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500)
)

# =========================
# LPI TOOL 1
# =========================
def lpi_wikipedia_tool(query: str):
    result = wiki_tool.run(query)
    return {
        "tool_name": "LPI_Wikipedia",
        "data": result
    }

# =========================
# LPI TOOL 2
# =========================
def lpi_arxiv_tool(query: str, max_results: int = 3):
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

    return {
        "tool_name": "LPI_Arxiv",
        "data": papers
    }

# =========================
# SYNTHESIS
# =========================
def synthesize(query, wiki_data, arxiv_data):

    arxiv_text = ""
    for i, p in enumerate(arxiv_data, 1):
        arxiv_text += f"""
Paper {i}: {p['title']}
Summary: {p['summary']}
"""

    prompt = f"""
You MUST use both sources.

Question:
{query}

Wikipedia:
{wiki_data}

Arxiv:
{arxiv_text}

OUTPUT FORMAT:

COMBINED ANSWER:
- Must integrate both sources
- Must include at least one research insight

WIKIPEDIA CONTRIBUTION:
- bullet points

ARXIV CONTRIBUTION:
- bullet points (with paper references)

TOOL TRACE:
- LPI_Wikipedia → what it provided
- LPI_Arxiv → what it provided

Do NOT repeat content.
"""

    response = llm.invoke(prompt)
    return response.content

# =========================
# PIPELINE
# =========================
def run_agent(query: str):

    print("\n==============================")
    print("QUERY:", query)
    print("==============================")

    # LPI TOOL 1
    wiki = lpi_wikipedia_tool(query)
    wiki_text = wiki["data"]

    # LPI TOOL 2
    arxiv_res = lpi_arxiv_tool(query)
    arxiv_data = arxiv_res["data"]

    # Synthesis
    answer = synthesize(query, wiki_text, arxiv_data)

    return {
        "answer": answer,
        "tool_trace": {
            "LPI_Wikipedia": "General knowledge and definitions",
            "LPI_Arxiv": "Research papers and technical insights"
        },
        "sources": {
            "Wikipedia": wiki_text[:300],
            "Arxiv": arxiv_data
        }
    }

# =========================
# PRINT
# =========================
def print_result(result):

    print("\n========== ANSWER ==========\n")
    print(result["answer"])

    print("\n========== TOOL TRACE ==========\n")
    for k, v in result["tool_trace"].items():
        print(f"{k} → {v}")

    print("\n========== SOURCES ==========\n")

    print("Wikipedia:")
    print(result["sources"]["Wikipedia"])

    print("\nArxiv Papers:")
    for p in result["sources"]["Arxiv"]:
        print("-", p["title"])


if __name__ == "__main__":
    res = run_agent("What is machine learning?")
    print_result(res)
