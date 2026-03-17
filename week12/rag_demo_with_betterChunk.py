import torch

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


# 1. Load documents
loader = TextLoader("docs.txt")
documents = loader.load()


# 2. Smart chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)


# 3. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Vector database
db = FAISS.from_documents(docs, embeddings)

retriever = db.as_retriever(search_kwargs={"k": 4})


# 5. Load fine-tuned model
model_path = "../week11/phi2-merged"

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.float16
).to("cuda")

model.eval()


# 6. HuggingFace pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0
)

llm = HuggingFacePipeline(pipeline=pipe)


# 7. Question
query = "How to click a button in Playwright?"


# 8. Retrieve context
relevant_docs = retriever.invoke(query)

context = "\n".join([doc.page_content for doc in relevant_docs])


# 9. Prompt
prompt = f"""
You are a QA automation assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question: {query}

Answer:
"""


# 10. Generate response
with torch.no_grad():
    result = llm.invoke(
        prompt,
        max_new_tokens=80,
        do_sample=False
    )

print("\n===== AI Answer =====\n")
print(result)