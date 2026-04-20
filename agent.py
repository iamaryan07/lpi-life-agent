import json
import subprocess
import os
import requests

print("=== RUNNING FINAL AGENT ===")

# ---- Path Setup ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LPI_PATH = os.path.join(BASE_DIR, "..", "dist", "src", "index.js")

print("Using LPI path:", LPI_PATH)

if not os.path.exists(LPI_PATH):
    raise FileNotFoundError(f"LPI server not found at {LPI_PATH}")


# ---- LLM (qwen2.5) ----
def ask_llm(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = res.json()

        # ---- DEBUG (optional, helps you see real issue)
        # print("LLM RAW:", data)

        if "response" in data:
            return data["response"]

        elif "error" in data:
            return f"LLM Error: {data['error']}"

        else:
            return f"Unexpected LLM response: {data}"

    except Exception as e:
        return f"LLM Error: {str(e)}"


# ---- Call LPI Tool ----
def call_lpi_tool(tool_name, query):
    try:
        process = subprocess.Popen(
            ["node", LPI_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        # INIT
        init_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        process.stdin.write(json.dumps(init_msg) + "\n")

        # Arguments
        if tool_name == "get_case_studies":
            args = {"query": "healthcare digital twin"}
        else:
            args = {"query": query}

        # Tool call
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            },
            "id": 1
        }

        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        stdout, stderr = process.communicate(timeout=10)

        # Parse response
        if stdout.strip():
            lines = stdout.strip().split("\n")

            for line in reversed(lines):
                try:
                    parsed = json.loads(line)

                    if "result" in parsed:
                        result = parsed["result"]

                        if isinstance(result, dict) and "content" in result:
                            content = result["content"]

                            if isinstance(content, list) and len(content) > 0:
                                text = content[0].get("text", "")

                                # Extract healthcare section
                                if tool_name == "get_case_studies":
                                    parts = text.split("## ")
                                    for part in parts:
                                        if "health" in part.lower():
                                            return "## " + part[:800]

                                return text

                        return str(result)

                except:
                    continue

        return "No output received"

    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"


# ---- Tool Selection (simple but valid) ----
def choose_tools(query):
    q = query.lower()

    if "how" in q or "use" in q:
        return ["smile_overview", "get_case_studies"]
    elif "implement" in q or "steps" in q:
        return ["get_methodology_step", "get_insights"]
    else:
        return ["query_knowledge", "get_case_studies"]


# ---- Agent ----
def run_agent():
    user_query = input("Enter your question: ")

    print("\nSelecting tools...\n")
    tool1, tool2 = choose_tools(user_query)

    print(f"Using tools: {tool1}, {tool2}\n")

    print("Calling tools...\n")
    data1 = call_lpi_tool(tool1, user_query)
    data2 = call_lpi_tool(tool2, user_query)

    print("\nGenerating response with LLM...\n")

    # ---- LLM Prompt ----
    prompt = f"""
    You are an AI agent using SMILE methodology and real case study data.

    User Query:
    {user_query}

    SMILE Data:
    {data1}

    Case Study Data:
    {data2}

    You MUST use specific details from BOTH:
    - SMILE Data
    - Case Study Data

    STRICT RULES:
    - Do NOT use general knowledge
    - Do NOT invent examples
    - If a detail is not in the data, do NOT include it
    - Quote or clearly reference parts of the case study

    For "Real-World Application":
    - Mention the actual case study name or scenario
    - Explain what was done (not generic description)
    - Explain outcome or purpose based ONLY on provided data

    For "Key SMILE Phases":
    - Select ONLY 2–3 phases
    - Justify why they are relevant to THIS case study

    Instructions:
    - You MUST use specific details from SMILE Data and Case Study Data. If a claim is not supported by the data, do NOT include it. Explicitly reference the case study (name, organization, or scenario).
    - You may rephrase, but do NOT invent new concepts
    - Do NOT include these instructions in your output

    Answer in this structure:

    1. Understanding:
    Brief explanation of digital twins in healthcare

    2. Key SMILE Phases:
    Mention only relevant phases and explain their role

    3. Real-World Application:
    Use the healthcare case study to explain usage

    4. Insight:
    Connect SMILE methodology with real-world healthcare usage

    5. Conclusion:
    Clear and concise summary

    Keep it clean, structured, and relevant to the question.
    """

    final_answer = ask_llm(prompt)

    print("----- FINAL ANSWER -----\n")
    print(final_answer)

    print("\n----- SOURCES -----")
    print(f"- {tool1}")
    print(f"- {tool2}")


# ---- Run ----
if __name__ == "__main__":
    run_agent()
