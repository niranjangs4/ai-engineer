import requests


# -------------------------------
# LLM CALL
# -------------------------------
def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get("response", "")


# -------------------------------
# TOOL 1 : CALCULATOR
# -------------------------------
def calculator(expression):

    try:
        result = eval(expression)
        return f"Calculator Result: {result}"

    except Exception:
        return "Invalid math expression"


# -------------------------------
# TOOL 2 : DOCUMENT SEARCH
# -------------------------------
def search_docs(question):

    docs = {
        "playwright": "Playwright supports Chromium, Firefox and WebKit.",
        "python": "Python is widely used for AI, automation and web development.",
        "selenium": "Selenium is a browser automation tool used for testing."
    }

    for key in docs:

        if key in question.lower():
            return docs[key]

    return "No documentation found"


# -------------------------------
# AGENT DECISION
# -------------------------------
def decide_tool(question):

    prompt = f"""
You are an AI agent.

Decide which tool should answer the user question.

Available tools:
1 calculator → for math questions
2 search_docs → for documentation questions

Return ONLY the tool name.

Question:
{question}
"""

    decision = ask_llm(prompt)

    return decision.lower()


# -------------------------------
# AGENT LOOP
# -------------------------------
def run_agent():

    print("\nSimple AI Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        question = input("User: ")

        if question.lower() == "exit":
            break

        tool = decide_tool(question)

        print(f"\nAgent selected tool: {tool}\n")

        if "calculator" in tool:

            result = calculator(question)

        else:

            result = search_docs(question)

        print("Agent:", result)
        print()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    run_agent()