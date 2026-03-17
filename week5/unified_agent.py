import requests
import chromadb
from sentence_transformers import SentenceTransformer


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

    return response.json().get("response", "")


# -----------------------------
# CALCULATOR TOOL
# -----------------------------
def calculator(expression):

    try:
        result = eval(expression)
        return f"Calculator result: {result}"

    except:
        return "Invalid math expression"


# -----------------------------
# VECTOR DATABASE SETUP
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.get_or_create_collection("docs")

documents = [
    "Playwright supports Chromium Firefox and WebKit.",
    "Python is widely used for AI and automation.",
    "Selenium is used for browser automation testing.",
    "Pytest is a popular testing framework for Python."
]


def load_docs():

    embeddings = model.encode(documents)

    for i, doc in enumerate(documents):

        collection.add(
            documents=[doc],
            embeddings=[embeddings[i].tolist()],
            ids=[str(i)]
        )


def search_docs(question):

    query_embedding = model.encode(question)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

    return results["documents"][0]


# -----------------------------
# AGENT DECISION
# -----------------------------
def decide_tool(question):

    prompt = f"""
You are an AI agent.

Decide which tool should answer the user question.

Available tools:

calculator → for math questions
search_docs → for documentation questions
llm → for general knowledge

Return only the tool name.

Question:
{question}
"""

    decision = ask_llm(prompt)

    return decision.lower()


# -----------------------------
# AGENT LOOP
# -----------------------------
def run_agent():

    load_docs()

    print("\nUnified AI Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        question = input("User: ")

        if question == "exit":
            break

        tool = decide_tool(question)

        print(f"\nAgent selected tool: {tool}\n")

        if "calculator" in tool:

            result = calculator(question)

        elif "search_docs" in tool:

            context = search_docs(question)

            prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

            result = ask_llm(prompt)

        else:

            result = ask_llm(question)

        print("Agent:", result)
        print()


if __name__ == "__main__":

    run_agent()