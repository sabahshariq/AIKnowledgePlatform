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


'''
results = search_similar_chunks(question, knowledge_base)

print("\nTop matching chunks:\n")

for result in results:
    print("=" * 80)
    print(f"Score: {result['score']}")
    print(result["text"])
'''


'''
def search_chunks(question: str, chunks: list[str]) -> list[str]:
    question = question.lower()

    matching_chunks = []

    for chunk in chunks:

        if question in chunk.lower():
            matching_chunks.append(chunk)

    return matching_chunks

results = search_chunks(question, chunks)

print("\nResults\n")

for result in results:
    print("=" * 80)
    print(result)

print(f"Total chunks created: {len(chunks)}")
#print("\nFirst chunk:\n")
#print(chunks[0])
#print(policy_text[:2000])
'''

