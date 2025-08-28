import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

load_dotenv()

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---- Gemini setup ----
if EMBEDDING_PROVIDER == "gemini" and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ---- OpenAI setup ----
if EMBEDDING_PROVIDER == "openai" and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str):
    """
    Lấy embedding từ Gemini hoặc OpenAI
    """
    if EMBEDDING_PROVIDER == "gemini":
        # Gemini embedding -> 1536 dimensions
        model = "models/embedding-001"
        result = genai.embed_content(model=model, content=text)
        return result["embedding"]

    elif EMBEDDING_PROVIDER == "openai":
        # OpenAI text-embedding-3-small -> 1536 dimensions
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    else:
        raise ValueError(f"❌ EMBEDDING_PROVIDER {EMBEDDING_PROVIDER} không hợp lệ.")


def get_embedding_dim() -> int:
    """
    Trả về dimension phù hợp với provider
    """
    if EMBEDDING_PROVIDER == "gemini":
        return 1536
    elif EMBEDDING_PROVIDER == "openai":
        return 1536
    else:
        raise ValueError("❌ Chưa định nghĩa dimension cho provider này.")
