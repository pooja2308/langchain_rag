from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

texts = [
    "Solar energy is renewable energy source that converts sunlight into electricity."
    "Wind energy is sustainable energy source that converts wind into electricity."
    "Coal is a fossil fuel that is used to generate electricity."
]

embeddings = FakeEmbeddings(size=384)
db = FAISS.from_texts(texts, embeddings)

retriever = db.as_retriever()
