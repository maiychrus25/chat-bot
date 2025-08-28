import os

# Flask settings
FLASK_ENV = os.getenv("FLASK_ENV", "development")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1-aws")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "students-index")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")

# Embedding / LLM
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini").lower()  # "gemini" hoặc "openai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Embedding dimension + top_k
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 768))
TOP_K = int(os.getenv("TOP_K", 5))
