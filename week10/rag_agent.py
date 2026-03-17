import chromadb
import requests
from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.get_or_create_collection(name="qa_docs")


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
# TOOL 1: RAG SEARCH
# -----------------------------

def search_docs(question):

    embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=2
    )

    docs = results["documents"][0]

    context = "\n".join(docs)

    return context


# -----------------------------
# TOOL 2: GENERATE AUTOMATION
# -----------------------------

def generate_code(feature):

    prompt = f"""
Generate Playwright automation for the following feature:

{feature}

Return only the code.
"""

    return ask_llm(prompt)


# -----------------------------
# AGENT
# -----------------------------

def agent(question):

    prompt = f"""
You are a QA automation AI agent.

Decide which action to take.

Actions:

search_docs
generate_code
answer_directly

User question:
{question}

Return only the action.
"""

    action = ask_llm(prompt).strip().lower()

    if "search_docs" in action:

        context = search_docs(question)

        final_prompt = f"""
Use this context to answer the question.

Context:
{context}

Question:
{question}
"""

        return ask_llm(final_prompt)

    elif "generate_code" in action:

        return generate_code(question)

    else:

        return ask_llm(question)


# -----------------------------
# CHAT LOOP
# -----------------------------

def run():

    print("\nRAG Agent Started")

    while True:

        q = input("\nUser: ")

        if q == "exit":
            break

        answer = agent(q)

        print("\nAgent:\n", answer)


if __name__ == "__main__":
    run()