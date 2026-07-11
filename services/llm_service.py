from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

#To get answer we need to pass "question", "top 3 chunk from ChromaDB", "Question history from Redis"
def generate_answer(
        question: str
        , context_chunks: list[dict]
        , conversation_history: list[dict]
        ) -> str:
    context_text = ""

    #Top 3 chunk we get from ChromaDB we only get the text that was from PDF
    for index, chunk in enumerate(context_chunks, start=1):
        context_text += f"\n--- Source Chunk {chunk['chunk_number']} ---\n"
        context_text += chunk["text"]

    history_text = ""

    #Load conversation history from Redis
    for message in conversation_history:
        history_text += f"{message['role']}: {message['content']}\n"
    
    #Use user question, matched chunk from PDF and conversation history.
    # Send it to OpenAI to reasoning and generate human readable answer.
    prompt = f"""
You are an employee Attendance and Leave Policy assistant.

Rules:
1. Answer using ONLY the policy context below.
2. Do not use outside knowledge.
3. If the answer is not clearly found in the context, say:
"I could not find this information in the policy document."
4. Keep the answer clear and concise.
5. Mention the relevant source chunk number when possible.

Policy COntext:
{context_text}

User Question:
{question}

Conversation History:
{history_text}
"""
    
    response = client.responses.create(
        model="gpt-4.1-mini",
        input = prompt
    )

    return response.output_text