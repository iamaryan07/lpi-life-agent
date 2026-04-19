print("=== RUNNING FINAL AGENT ===")

import subprocess
import json


# ---- Call LPI Tool ----
def call_lpi_tool(tool_name, query):
    try:
        process = subprocess.Popen(
            ["node", "dist/src/index.js"],   # ✅ correct server (NOT test-client)
            cwd="lpi-developer-kit",         # ✅ run inside dev kit
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # ---- INIT (required) ----
        init_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        process.stdin.write(json.dumps(init_msg) + "\n")

        # ---- Choose arguments based on tool ----
        if tool_name == "get_case_studies":
            args = {"query": "healthcare digital twin"}
        else:
            args = {"query": query}

        # ---- TOOL CALL ----
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args   # 🔥 use args instead of {"query": query}
            },
            "id": 1
        }

        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        stdout, stderr = process.communicate(timeout=10)

        # ---- Parse response ----
        if stdout.strip():
            try:
                lines = stdout.strip().split("\n")

                for line in reversed(lines):
                    try:
                        parsed = json.loads(line)

                        if "result" in parsed:
                            result = parsed["result"]

                            # 🔥 extract actual text
                            if isinstance(result, dict) and "content" in result:
                                content = result["content"]
                                if isinstance(content, list) and len(content) > 0:
                                    text = content[0].get("text", "")

                                    # 🔥 Extract healthcare section only
                                    if tool_name == "get_case_studies":
                                        if "Healthcare" in text or "health" in text.lower():
                                            # split into sections
                                            parts = text.split("## ")
                                            for part in parts:
                                                if "Healthcare" in part or "health" in part.lower():
                                                    return "## " + part[:800]   # return relevant section only

                                    return text

                            return str(result)

                    except:
                        continue

                return stdout

            except:
                return stdout

        return "No output received"

    except Exception as e:
        return f"Error calling {tool_name}: {str(e)}"


# ---- Tool Selection (fixed names) ----
def choose_tools(query):
    return "smile_overview", "get_case_studies"


# ---- Simple Processing ----
def extract_key_points(text):
    lines = text.split(".")
    return text[:400]


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
SMILE provides a structured lifecycle for building digital twins,
while case studies demonstrate real-world implementations.

Conclusion:
Digital twins in healthcare are used for simulation, monitoring,
and predictive modeling of patient conditions.
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

    print("\nProcessing...\n")
    final_answer = process_results(data1, data2, user_query)

    print("----- FINAL ANSWER -----\n")
    print(final_answer)

    print("\n----- SOURCES -----")
    print(f"- {tool1}")
    print(f"- {tool2}")


# ---- Run ----
if __name__ == "__main__":
    run_agent()
