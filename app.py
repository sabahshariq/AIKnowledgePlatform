import json


from storage.vector_store import load_embeddings
from services.retriever import search_similar_chunks
from services.llm_service import generate_answer


knowledge_base = load_embeddings("data/knowledge_base.json")
question = input("Ask a question: ")

matched_chunks = search_similar_chunks(
    question = question,
    knowledge_base = knowledge_base,
    top_k= 3
)

answer = generate_answer(question, matched_chunks)

print("\nAnswer:\n")
print(answer)

print("\nSources:\n")

for chunk in matched_chunks:
    print(f"Chunk: {chunk['chunk_number']}")
    print(f"Score: {chunk['score']}")
    print("-" * 80)

