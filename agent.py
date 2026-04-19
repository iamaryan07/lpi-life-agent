print("=== RUNNING UPDATED AGENT ===")

import subprocess
import json


# ---- Call LPI Tool ----
def call_lpi_tool(tool_name, query):
    try:
        process = subprocess.Popen(
            ["node", "lpi-developer-kit/dist/test-client.js"],  # FIXED PATH
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": {"query": query}
            },
            "id": 1
        }

        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        stdout, stderr = process.communicate(timeout=10)

        print("RAW STDOUT:", stdout)   # DEBUG
        print("RAW STDERR:", stderr)   # DEBUG

        if stdout.strip():
            try:
                parsed = json.loads(stdout)
                if "result" in parsed:
                    return str(parsed["result"])
                return str(parsed)
            except:
                return stdout

        return "No output received"

    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"


# ---- Smart Tool Selection ----
def choose_tools(query):
    q = query.lower()

    if "health" in q or "hospital" in q:
        return "smile_overview", "case_study_healthcare"

    elif "manufacturing" in q or "factory" in q:
        return "smile_overview", "case_study_manufacturing"

    elif "energy" in q:
        return "smile_overview", "case_study_energy"

    else:
        # fallback
        return "smile_overview", "case_study_general"


# ---- Better Processing ----
def extract_key_points(text):
    # very simple heuristic summarization
    lines = text.split(".")
    return ". ".join(lines[:3])  # first 3 sentences


def process_results(smile_data, case_data, user_query):
    smile_summary = extract_key_points(smile_data)
    case_summary = extract_key_points(case_data)

    return f"""
Question: {user_query}

SMILE Framework (Summary):
{smile_summary}

Case Study (Summary):
{case_summary}

Analysis:
The SMILE framework provides a structured methodology (phases, lifecycle thinking),
while the case study demonstrates real-world execution.

Conclusion:
Digital twins are effective when theoretical structure (SMILE)
is combined with domain-specific implementation (case study).
"""


# ---- Agent ----
def run_agent():
    user_query = input("Enter your question: ")

    print("\nSelecting tools...\n")
    tool1, tool2 = choose_tools(user_query)

    print(f"Using tools: {tool1}, {tool2}\n")

    print("Calling tools...\n")
    data1 = call_lpi_tool(tool1, user_query)
    data2 = call_lpi_tool(tool2, user_query)

    print("Processing...\n")
    final_answer = process_results(data1, data2, user_query)

    print("----- FINAL ANSWER -----\n")
    print(final_answer)

    print("\n----- SOURCES -----")
    print(f"- {tool1}")
    print(f"- {tool2}")


# ---- Run ----
if __name__ == "__main__":
    run_agent()
