import requests


# -----------------------------
# TOOLS
# -----------------------------

def calculator(expression):

    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


docs = {
    "playwright": "Playwright supports Chromium, Firefox, and WebKit.",
    "python": "Python is widely used for automation and AI."
}


def search_docs(query):

    query = query.lower()

    for key in docs:

        if key in query:
            return docs[key]

    return "No documentation found"


# -----------------------------
# LLM
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

    return response.json()["response"]


# -----------------------------
# REACT LOOP
# -----------------------------

def react_agent(question):

    history = f"User Question: {question}\n"

    for step in range(5):

        prompt = f"""
You are a ReAct AI agent.

Available tools:
calculator
search_docs

Conversation:
{history}

Respond using ONE of these formats:

Thought: reasoning
Action: tool name
Action Input: input

OR

Final Answer: answer to user
"""

        response = ask_llm(prompt)

        print("\nLLM Response:\n")
        print(response)

        history += response + "\n"

        if "Final Answer:" in response:
            print("\nTask completed.")
            break

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

        print("\nObservation:", observation)

        history += f"Observation: {observation}\n"


# -----------------------------
# RUN LOOP
# -----------------------------

def run_agent():

    print("\nMulti-Step ReAct Agent Started\n")

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