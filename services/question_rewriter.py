from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

#receive user question and converstion history from Redis
def rewrite_question(question: str, conversation_history: list [dict])-> str:
    history_text = ""

    #Load conversation hisotry from Redis for sending to OpenAI API
    for message in conversation_history:
        history_text += f"{message['role']}: {message['content']}\n"

    prompt = f"""
You rewrite follow-up questions into standalone questions.

Rules:
1. Use the conversation history only to resolve references like "they", "it", "that", "this".
2. Do not answer the question.
3. Do not add extra information.
4. Return only the rewritten question.

Conversation History:
{history_text}

Current Question:
{question}
"""
    
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = prompt
    )

    return response.output_text.strip()
