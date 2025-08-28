# embedder.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_DIM = 768  # chiều embedding target

def get_embedding(text: str):
    """Lấy embedding cho text từ Gemini, trả về vector dimension 768"""
    return _get_gemini_embedding(text)

def _get_gemini_embedding(text: str):
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError("Cần cài `google-generativeai` để dùng Gemini embeddings.")
    
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY chưa được set.")
    
    genai.configure(api_key=GEMINI_API_KEY)

    model = "models/gemini-embedding-001"  # model Gemini

    result = genai.embed_content(model=model, content=text)
    embedding = result["embedding"]

    if len(embedding) != EMBEDDING_DIM:
        # Nếu model trả ra không đúng chiều, bạn có thể giảm dimension bằng PCA hoặc cắt
        embedding = embedding[:EMBEDDING_DIM]

    return embedding
