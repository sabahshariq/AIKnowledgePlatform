import json

from services.pdf_reader import read_pdf
from storage.text_splitter import split_text
from services.embedding_service import get_embedding
from storage.vector_store import save_embeddings

pdf_path = "policy/attendance_leave_policy.pdf"

def save_chunks(chunks: list[str], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)

def load_chunks(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


policy_text = read_pdf(pdf_path)
chunks = split_text(policy_text)
save_chunks(chunks, "chunks.json")

chunks = load_chunks("chunks.json")


knowledge_base = []

for index, chunk in enumerate(chunks, start=1):

    print(f"Embedding chunk {index}/{len(chunks)}")

    embedding = get_embedding(chunk)

    knowledge_base.append({
        "text": chunk,
        "embedding": embedding
    })

    save_embeddings(
    knowledge_base,
    "knowledge_base.json"
    )
    
    print("Knowledge base created successfully.")