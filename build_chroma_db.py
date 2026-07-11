import chromadb

from storage.vector_store import load_embeddings


CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "attendance_leave_policy"

#Current json file contains "text" and corresponding "embedding value"
knowledge_base = load_embeddings("data/knowledge_base.json")

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

ids = []
documents = []
embeddings = []
metadatas = []

for index, item in enumerate(knowledge_base, start=1):
    ids.append(f"chunk_{index}")
    documents.append(item["text"])
    embeddings.append(item["embedding"])
    metadatas.append(
        {
            "chunk_number": index,
            "source": "attendance_leave_policy"
        }
    )

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Chroma database created successfully.")
print(f"Total chunks added: {len(ids)}")