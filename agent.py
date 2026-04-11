from langchain_classic.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOllama
from rag import retriever
import os

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    base_url="http://ollama:11434" if os.getenv("PROFILE") == "docker" else "http://localhost:11434"
)


# Tool 1: RAG search
def search_docs(query: str) -> str:
    """Search energy related documents"""
    docs = retriever.invoke(query)
    return " ".join([doc.page_content for doc in docs])


tools = [Tool(name="Document Search", func=search_docs, description="Search energy related documents")]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
