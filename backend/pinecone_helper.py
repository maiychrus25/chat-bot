# pinecone_helper.py
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_ENV, EMBEDDING_DIM

def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Nếu index chưa tồn tại, tạo mới dimension chuẩn 768
    if PINECONE_INDEX not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIM,  # EMBEDDING_DIM = 768
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
        )

    return pc.Index(PINECONE_INDEX)

def upsert_vectors(index, vectors):
    """ vectors = list of tuples (id, vector, metadata) """
    index.upsert(vectors=vectors)

def query_index(index, vector, top_k=5):
    res = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        include_values=False
    )
    return res
