import chromadb
import requests
from sentence_transformers import SentenceTransformer


# -------------------------------
# LLM
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

    return response.json().get("response", "")


# -------------------------------
# VECTOR DB SETUP
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.get_or_create_collection("docs")


# -------------------------------
# DOCUMENTS
# -------------------------------
documents = [
    "Playwright supports Chromium Firefox and WebKit.",
    "Python is widely used for automation and AI.",
    "Selenium is used for browser automation testing.",
    "Pytest is a popular testing framework in Python."
]


def load_docs():

    embeddings = model.encode(documents)

    for i, doc in enumerate(documents):

        collection.add(
            documents=[doc],
            embeddings=[embeddings[i].tolist()],
            ids=[str(i)]
        )


# -------------------------------
# SEARCH VECTOR DB
# -------------------------------
def search_docs(question):

    query_embedding = model.encode(question)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

    return results["documents"][0]


# -------------------------------
# AGENT
# -------------------------------
def run_agent():

    load_docs()

    print("\nRAG Agent Started")
    print("Type 'exit' to stop\n")

    while True:

        question = input("User: ")

        if question == "exit":
            break

        context = search_docs(question)

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""
        print("prompt:", prompt)
        answer = ask_llm(prompt)

        print("\nAgent:", answer)
        print()


if __name__ == "__main__":
    run_agent()