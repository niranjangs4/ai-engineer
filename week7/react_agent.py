import requests

# -----------------------------
# TOOL FUNCTIONS
# -----------------------------

def calculator(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid math expression"


docs = {
    "playwright": "Playwright supports Chromium, Firefox, and WebKit browsers.",
    "python": "Python is widely used for AI, automation, and data science."
}

def search_docs(query):

    query = query.lower()

    for key in docs:
        if key in query:
            return docs[key]

    return "No documentation found."


# -----------------------------
# LLM FUNCTION
# -----------------------------

def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json().get("response", "")


# -----------------------------
# REACT LOOP
# -----------------------------

def react_agent(question):

    print("\nStarting ReAct reasoning...\n")

    prompt = f"""
You are an AI agent using the ReAct pattern.

Available tools:

calculator
search_docs

Follow this format:

Thought: reasoning
Action: tool name
Action Input: input for tool

User Question:
{question}
"""

    response = ask_llm(prompt)

    print("LLM Response:\n")
    print(response)

    # Parse action
    action = None
    action_input = None

    for line in response.split("\n"):

        if line.lower().startswith("action:"):
            action = line.split(":")[1].strip()

        if line.lower().startswith("action input:"):
            action_input = line.split(":")[1].strip()

    if action == "calculator":

        observation = calculator(action_input)

    elif action == "search_docs":

        observation = search_docs(action_input)

    else:

        observation = "Unknown tool"

    print("\nObservation:")
    print(observation)

    # Final answer generation
    final_prompt = f"""
You are an AI assistant.

User Question:
{question}

Tool Observation:
{observation}

Provide the final answer.
"""

    final_answer = ask_llm(final_prompt)

    print("\nFinal Answer:\n")
    print(final_answer)


# -----------------------------
# AGENT LOOP
# -----------------------------

def run_agent():

    print("\nReAct Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        question = input("User: ")

        if question == "exit":
            break

        react_agent(question)


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    run_agent()