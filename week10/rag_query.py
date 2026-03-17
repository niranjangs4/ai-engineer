import chromadb
import requests
from sentence_transformers import SentenceTransformer

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# CONNECT TO CHROMA
# -----------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(name="qa_docs")

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

    return response.json()["response"]


# -----------------------------
# RAG QUERY
# -----------------------------

def rag_query(question):

    embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=2
    )

    docs = results["documents"][0]

    context = "\n".join(docs)

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""

    answer = ask_llm(prompt)

    return answer


# -----------------------------
# CHAT LOOP
# -----------------------------

def run():

    print("\nRAG QA Assistant Started")
    print("Type 'exit' to stop\n")

    while True:

        q = input("Question: ")

        if q == "exit":
            break

        answer = rag_query(q)

        print("\nAnswer:\n", answer)


if __name__ == "__main__":

    run()