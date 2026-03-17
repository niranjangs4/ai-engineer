import torch

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


# ----------------------------
# 1. Load document
# ----------------------------

loader = TextLoader("docs.txt")
documents = loader.load()


# ----------------------------
# 2. Split document into chunks
# ----------------------------

text_splitter = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

docs = text_splitter.split_documents(documents)


# ----------------------------
# 3. Create embeddings
# ----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ----------------------------
# 4. Create vector database
# ----------------------------

db = FAISS.from_documents(docs, embeddings)

retriever = db.as_retriever(search_kwargs={"k": 2})


# ----------------------------
# 5. Load fine-tuned model
# ----------------------------

model_path = "../week11/phi2-merged"

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.float16
).to("cuda")

model.eval()


# ----------------------------
# 6. Create HF pipeline
# ----------------------------

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0
)

llm = HuggingFacePipeline(pipeline=pipe)


# ----------------------------
# 7. Ask question
# ----------------------------

query = "How to click a button in Playwright?"


# ----------------------------
# 8. Retrieve relevant docs
# ----------------------------

relevant_docs = retriever.invoke(query)

context = "\n".join([doc.page_content for doc in relevant_docs])


# ----------------------------
# 9. Prompt
# ----------------------------
prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

Context:
{context}

Question: {query}

Provide a short answer in one sentence.

Answer:
"""

# ----------------------------
# 10. Generate response
# ----------------------------

with torch.no_grad():
    result = llm.invoke(
        prompt,
        max_new_tokens=60,
        do_sample=False
    )

print("\n===== AI Answer =====\n")
print(result)