from fastapi import FastAPI
import uvicorn

from agent import agent
from db import save_query
from memory import save_memory, get_memory

app = FastAPI()

@app.post("/ask")
async def ask(user: str, q: str):
    history = get_memory(user)
    full_input = f"History: {history}\nQuestion: {q}"

    response = agent.run(full_input)
    save_memory(user, q)
    save_memory(user, response)
    save_query(q, response)
    return {"answer": response}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)