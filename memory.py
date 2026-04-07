import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def _key(user: str) -> str:
    return f"memory:{user}"


def save_memory(user: str, message: str) -> None:
    try:
        r.lpush(_key(user), message)
    except redis.exceptions.ConnectionError:
        # Allow app to run without Redis (memory becomes ephemeral).
        return

def get_memory(user: str):
    try:
        return r.lrange(_key(user), 0, 5)
    except redis.exceptions.ConnectionError:
        return []