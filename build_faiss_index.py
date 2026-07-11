import faiss
import numpy as np

from storage.vector_store import load_embeddings

knowledge_base_path = "data/knowledge_base.json"
faiss_index_path = "data/policy_index.faiss"

knowledge_base = load_embeddings(knowledge_base_path)

embeddings = []

for item in knowledge_base:
    embeddings.append(
        item["embedding"]
    )

embedding_matrix = np.array(embeddings).astype("float32")
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)

faiss.write_index(index, faiss_index_path)

print("FAISS index created successfully.")
print(f"Total vectors added: {index.ntotal}")
print(f"Vector dimension: {dimension}")