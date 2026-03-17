import chromadb
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
# LOAD DOCUMENT
# -----------------------------

with open("../data/docs.txt", "r", encoding="utf-8") as f:
    text = f.read()

# -----------------------------
# SIMPLE CHUNKING
# -----------------------------

chunks = text.split("\n\n")

# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------

for i, chunk in enumerate(chunks):

    embedding = model.encode(chunk).tolist()

    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[f"doc_{i}"]
    )

print("Documents indexed successfully.")