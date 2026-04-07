from langchain_classic.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOllama
from rag import retriever

llm = ChatOllama(model="llama3.1:8b", temperature=0)

# Tool 1: RAG serach
def search_docs(query: str) -> str:
    """Search energy related documents"""
    docs = retriever.invoke(query)
    return " ".join([doc.page_content for doc in docs])

tools = [Tool(name="Document Search", func=search_docs, description="Search energy realted documents")]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)