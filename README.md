# LangChain RAG Demo (FastAPI + FAISS + Ollama)

This is a small demo project that:

- Builds a tiny **FAISS** vector store from a few sample texts (`rag.py`)
- Uses a tool-calling **LangChain agent** (`agent.py`) with a **local LLM via Ollama**
- Exposes an API endpoint with **FastAPI** (`main.py`)
- Optionally stores short conversation “memory” in **Redis** (`memory.py`)
- Stores Q/A logs in **PostgreSQL** (`db.py`)

## Requirements

- Python (project has been run with a local `.venv`)
- Optional but recommended:
  - **Ollama** for a free/local chat model
  - **PostgreSQL** (required by `db.py` as written)
  - **Redis** (optional; app still runs if Redis is down)

## Setup (local)

Create + activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

## Run a local/free model (Ollama)

1) Install Ollama: `https://ollama.com/download`

2) Pull a model (recommended small model for CPU Macs):

```bash
ollama pull llama3.2:3b
```

This project currently uses:

- `llama3.1:8b` in `agent.py` (better quality, slower)

You can change the model string in `agent.py`:

- `ChatOllama(model="llama3.2:3b", temperature=0)`

## Start PostgreSQL (required for logging)

`db.py` connects on import to:

- host: `localhost`
- port: `5432`
- db: `mydb`
- user: `user`
- password: xxxxx

### Option A: Homebrew

```bash
brew install postgresql@16
brew services start postgresql@16
```

Create role + database + table:

```bash
psql postgres
```

```sql
CREATE ROLE "user" WITH LOGIN PASSWORD 'password';
CREATE DATABASE mydb OWNER "user";
\q
```

```bash
psql -d mydb -U user -h localhost
```

```sql
CREATE TABLE IF NOT EXISTS logs (
  id SERIAL PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
\q
```

## Redis (optional)

`memory.py` uses Redis at `localhost:6379`. If Redis isn’t running, memory becomes ephemeral and the API still works.

To start Redis with Homebrew:

```bash
brew install redis
brew services start redis
```

## Run the API

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

Open interactive docs:

- `http://127.0.0.1:8000/docs`

### Call the endpoint

`/ask` is **POST** (not GET):

```bash
curl -X POST "http://127.0.0.1:8000/ask?user=test&q=What%20is%20renewable%20energy%3F"
```

Response:

```json
{"answer":"..."}
```

## Files

- **`rag.py`**: creates FAISS vector store + `retriever`
- **`agent.py`**: LangChain agent wired to a `Document Search` tool (uses `retriever.invoke`)
- **`main.py`**: FastAPI app exposing `POST /ask`
- **`memory.py`**: Redis-backed recent message list per user (fails open if Redis is down)
- **`db.py`**: PostgreSQL logging of Q/A to `logs` table

## Notes / troubleshooting

- **405 Method Not Allowed**: you used GET on `/ask`. Use POST or `/docs`.
- **`ModuleNotFoundError`**: make sure you’re running with `.venv` activated.
- **Postgres “connection refused”**: Postgres isn’t running on `localhost:5432`.
- **Redis “connection refused”**: Redis isn’t running on `localhost:6379` (safe to ignore; memory just won’t persist).