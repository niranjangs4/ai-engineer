import chromadb
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.create_collection("docs")


def load_docs():
    with open("data/docs.txt") as f:
        return f.read()


def chunk_text(text, size=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)
        print("chunk:",chunk)
    print("chunks:", chunks)
    print("chunks:", len(chunks))
    return chunks


def store_chunks(chunks):

    for i, chunk in enumerate(chunks):

        embedding = model.encode(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding.tolist()],
            ids=[str(i)]
        )


def search_docs(query):

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

    return results["documents"][0]


def ask_llm(context, question):

    prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}
"""
    print("prompt:", prompt)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def main():

    docs = load_docs()

    chunks = chunk_text(docs)

    store_chunks(chunks)

    while True:

        question = input("\nAsk question: ")

        if question == "exit":
            break

        context = search_docs(question)

        answer = ask_llm(context, question)

        print("\nAI Answer:\n", answer)


if __name__ == "__main__":
    main()