import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.create_collection("documents")
print(model)
print(client)
print(collection)
documents = [
    "Playwright is a browser automation framework",
    "Selenium is used for web automation",
    "Python is widely used for AI development"
]

embeddings = model.encode(documents)
print(embeddings)
for i, doc in enumerate(documents):
    print(i, doc)
    collection.add(
        documents=[doc],
        embeddings=[embeddings[i].tolist()],
        ids=[str(i)]
    )

query = input("Search query: ")

query_embedding = model.encode(query)

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3
)

print("\nResults:\n")

for doc in results["documents"][0]:
    print("-", doc)