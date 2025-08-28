# ingest.py
import json
import os
from dotenv import load_dotenv
from pinecone_helper import init_pinecone, upsert_vectors
from embeddings import get_embedding

# Load biến môi trường từ .env
load_dotenv()

PINECONE_INDEX = os.getenv("PINECONE_INDEX", "students-index")
DATA_FILE = "data_students.json"

def load_data(file_path):
    """Đọc dữ liệu từ JSON"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_vectors(data):
    """Tạo vectors (id, embedding, metadata)"""
    vectors = []
    for i, student in enumerate(data, start=1):
        # Ghép các trường làm input cho embedding
        text = f"{student['name']} - {student['id']} - {student['dob']} - {student['address']} - {student['hobby']} - {student['interest']} - {student['skill']}"
        embedding = get_embedding(text)

        metadata = {
            "id": student["id"],
            "name": student["name"],
            "dob": student["dob"],
            "address": student["address"],
            "hobby": student["hobby"],
            "interest": student["interest"],
            "skill": student["skill"]
        }

        vectors.append((str(i), embedding, metadata))
    return vectors

if __name__ == "__main__":
    print("🚀 Bắt đầu ingest dữ liệu vào Pinecone...")

    # Khởi tạo Pinecone
    index = init_pinecone()

    # Load data từ file JSON
    data = load_data(DATA_FILE)
    print(f"📂 Đã đọc {len(data)} bản ghi từ {DATA_FILE}")

    # Chuẩn bị vectors
    vectors = prepare_vectors(data)

    # Upsert vào Pinecone
    upsert_vectors(index, vectors)

    print(f"✅ Đã ingest {len(vectors)} bản ghi vào Pinecone ({PINECONE_INDEX}) thành công!")
