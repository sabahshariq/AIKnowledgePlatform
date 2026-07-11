import faiss
import numpy as np

from services.embedding_service import get_embedding

def load_faiss_index(index_path: str):
    return faiss.read_index(index_path)

def search_similar_chunks(
        question: str,
        knowledge_base: list[dict],
        faiss_index,
        top_k: int = 3
        ) -> list[dict]:
    
    question_embedding = get_embedding(question)
    question_vector = np.array([question_embedding]).astype("float32")
    distance, indices = faiss_index.search(question_vector, top_k)

    matched_chunks = []

    for position, distance in zip(indices[0], distance[0]):
        item = knowledge_base[position]

        matched_chunks.append(
            {
                "chunk_number": int(position) + 1,
                "text": item["text"],
                "score": float(distance)
            }
        )

    return matched_chunks



















'''
import math

from services.embedding_service import get_embedding

def cosine_similarity(vector1: list[float], vector2: list[float])-> float:
    dot_product = 0
    magnitude1 = 0
    magnitude2 = 0

    for a, b in zip(vector1, vector2):
        dot_product += a * b
        magnitude1 += a * a 
        magnitude2 += b * b

    magnitude1 = math.sqrt(magnitude1)
    magnitude2 = math.sqrt(magnitude2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)

def search_similar_chunks(question: str, knowledge_base: list[dict], top_k: int = 3) -> list[dict]:
    question_embedding = get_embedding(question)

    scored_chunks = []

    #for item in knowledge_base:
    for index, item in enumerate(knowledge_base, start=1):
        score = cosine_similarity(question_embedding, item["embedding"])

        scored_chunks.append(
            {
                "chunk_number": index,
                "text": item["text"],
                "score": score
            }
        )

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]

'''
