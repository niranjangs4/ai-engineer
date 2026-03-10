import chromadb

client = chromadb.Client()

collection = client.create_collection("test")

collection.add(
    documents=["Playwright automation tool"],
    ids=["1"]
)

print(collection.query(query_texts=["browser automation"], n_results=1))