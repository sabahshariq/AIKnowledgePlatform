import json
import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

SESSION_TTL_SECONDS = 3600


def get_session_key(session_id: str) -> str:
    return f"chat:{session_id}"


def add_message(session_id: str, role: str, content: str) -> None:
    key = get_session_key(session_id)

    message = {
        "role": role,
        "content": content
    }

    redis_client.rpush(key, json.dumps(message))
    redis_client.expire(key, SESSION_TTL_SECONDS)

def get_conversation_history(session_id: str, limit: int = 10) -> list[dict]:
    key = get_session_key(session_id) #Ex. chat: 123

    #Based on session id (chat: 123) retreive last 10 message
    messages = redis_client.lrange(key, -limit, -1)

    return [json.loads(message) for message in messages]

'''
def get_conversation_history(session_id: str) -> list[dict]:
    key = get_session_key(session_id)

    messages = redis_client.lrange(key, 0, -1)

    return [json.loads(message) for message in messages]
    '''


def clear_conversation_history(session_id: str) -> None:
    key = get_session_key(session_id)

    redis_client.delete(key)