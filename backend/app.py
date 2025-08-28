# app.py
import os, json, traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
from pinecone_helper import init_pinecone, upsert_vectors, query_index
from embedder import get_embedding
from generator import generate_answer
from utils import student_to_text
from config import TOP_K, FLASK_HOST, FLASK_PORT

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

index = init_pinecone()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"}), 200

@app.route("/api/upload", methods=["POST"])
def upload_students():
    try:
        data = request.get_json() or {}
        students = data.get("students") if isinstance(data, dict) else data
        if not isinstance(students, list):
            return jsonify({"error":"students must be a list"}), 400

        vectors = []
        for idx, s in enumerate(students, start=1):
            sid = s.get("id") or f"student_{idx:04d}"
            text = student_to_text(s)
            emb = get_embedding(text)
            if len(emb) != 768:
                return jsonify({"error":"Embedding dimension mismatch"}), 500

            metadata = {
                "name": s.get("name"),
                "dob": s.get("dob"),
                "address": s.get("address"),
                "hobby": s.get("hobby"),
                "interest": s.get("interest"),
                "skill": s.get("skill"),
                "text": text
            }
            vectors.append((sid, emb, metadata))

            if len(vectors) >= 50:
                upsert_vectors(index, vectors)
                vectors = []

        if vectors:
            upsert_vectors(index, vectors)

        return jsonify({"status":"uploaded", "count": len(students)}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json() or {}
        question = (body.get("question") or "").strip()
        if not question:
            return jsonify({"error":"question is required"}), 400

        # =========================
        # 1️⃣ Tạo embedding và debug
        # =========================
        q_emb = get_embedding(question)
        print("DEBUG: question =", question)
        print("DEBUG: embedding length =", len(q_emb))
        print("DEBUG: embedding sample (first 10 dims) =", q_emb[:10])

        # =========================
        # 2️⃣ Query Pinecone và debug
        # =========================
        res = query_index(index, q_emb, top_k=TOP_K)
        print("DEBUG: raw Pinecone response =", res)

        matches = res.matches if hasattr(res, "matches") else res.get("matches", [])
        print("DEBUG: matches found =", len(matches))

        if not matches:
            return jsonify({"answer": "Không có thông tin.", "related": []}), 200

        # =========================
        # 3️⃣ Chuẩn bị dữ liệu trả về
        # =========================
        docs = []
        related = []
        for m in matches:
            md = m.metadata if hasattr(m, "metadata") else m.get("metadata", {})
            s = {
                "id": getattr(m, "id", m.get("id")),
                "score": getattr(m, "score", m.get("score")),
                "name": md.get("name"),
                "dob": md.get("dob"),
                "address": md.get("address"),
                "hobby": md.get("hobby"),
                "interest": md.get("interest"),
                "skill": md.get("skill")
            }
            related.append(s)
            line = f"{s['name']}, DOB: {s['dob']}, Address: {s['address']}, Hobby: {s['hobby']}, Skill: {s['skill']}"
            docs.append(line)

        documents_text = "\n".join(f"- {d}" for d in docs)
        answer = generate_answer(documents_text, question)
        return jsonify({"answer": answer, "related": related}), 200

    except Exception as e:
        # =========================
        # 4️⃣ In stack trace + lỗi chi tiết
        # =========================
        traceback.print_exc()
        return jsonify({"error":"Server error", "exception": str(e)}), 500


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
