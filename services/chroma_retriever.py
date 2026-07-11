import chromadb

from services.embedding_service import get_embedding


CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "attendance_leave_policy"


#ChromaDB connection string
def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def search_similar_chunks_chroma(question: str, top_k: int = 3) -> list[dict]:
    #Load all ChromaDB -> contains data in vector format and get corresponding
    collection = get_chroma_collection()

    #Convert user into vector format and get corresponding number
    question_embedding = get_embedding(question)

    #Get the top 3 matching embedding similar to user question
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    matched_chunks = []

    #Loop through "results" and store it into "matched_chunk" array
    for index in range(len(results["ids"][0])):
        matched_chunks.append(
            {
                "chunk_number": results["metadatas"][0][index]["chunk_number"],
                "text": results["documents"][0][index],
                "score": results["distances"][0][index]
            }
        )

    return matched_chunks