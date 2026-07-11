from fastapi import FastAPI
from pydantic import BaseModel

from services.chroma_retriever import search_similar_chunks_chroma
from services.llm_service import generate_answer
from services.redis_memory_service import (
    add_message,
    get_conversation_history,
    clear_conversation_history
)
from services.question_rewriter import rewrite_question


app = FastAPI()


#Getter/Setter similar to C#
class QuestionRequest(BaseModel):
    session_id: str
    question: str


#From swagger user request comes here
@app.post("/ask")
def ask_policy_question(request: QuestionRequest):
    #Load conversation history from Redis
    history = get_conversation_history(request.session_id)

    #Rerwrite follow up question to standard using OpenAI API call
    standalone_question = rewrite_question(
        question=request.question,
        conversation_history=history
    )

    #From ChromaDB chroma_retriever get 3 chunk which match word "sick leave" from user question
    matched_chunks = search_similar_chunks_chroma(
        question=standalone_question,
        top_k=3
    )

    #To get answer we need to pass "question", "top 3 chunk from ChromaDB", "Question history from Redis"
    answer = generate_answer(
        question=standalone_question,
        context_chunks=matched_chunks,
        conversation_history=history
    )

    #Store user question and answer into Redis for conversation history
    add_message(request.session_id, "user", request.question)
    add_message(request.session_id, "assistant", answer)

    #This block just returing value just to what is happening. Like debugging.
    sources = []

    for chunk in matched_chunks:
        sources.append(
            {
                "chunk_number": chunk["chunk_number"],
                "score": chunk["score"]
            }
        )

    return {
        "answer": answer,
        "sources": sources,
        "standalone_question": standalone_question
    }
    #This block just returing value just to what is happening. Like debugging.

class ClearMemoryRequest(BaseModel):
    session_id: str


@app.post("/clear-memory")
def clear_memory(request: ClearMemoryRequest):
    clear_conversation_history(request.session_id)

    return {
        "message": "Conversation memory cleared."
    }