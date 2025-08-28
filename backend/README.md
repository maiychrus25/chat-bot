# Student RAG Chatbot

This project is a simple RAG (Retrieval-Augmented Generation) chatbot that helps answer questions about students in a class.
It uses:
- **Flask** as the backend framework
- **Pinecone** for vector database
- **Gemini API** for embeddings and answer generation
- **Simple HTML/JS frontend** for chat UI

---

## Features
- Upload student data (CSV/JSON) to Pinecone with embeddings
- Ask natural language questions about students (hobbies, skills, etc.)
- Retrieve relevant students using semantic search
- Generate natural responses with Gemini

---

## Installation

### 1. Clone repository
```bash
git clone https://github.com/your-username/student-rag-chatbot.git
cd student-rag-chatbot
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup environment variables
Create a `.env` file in the project root with:
```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_env
GEMINI_API_KEY=your_gemini_key
```

### 4. Run Flask server
```bash
python app.py
```
Backend will start at: `http://127.0.0.1:5000`

### 5. Open frontend
Open `frontend/index.html` in your browser.  
Type a question in the chatbox and get responses from the chatbot.

---

## Project Structure
```
student-rag-chatbot/
│── app.py              # Flask backend API
│── requirements.txt    # Dependencies
│── .env                # API keys (ignored by git)
│── frontend/
│    └── index.html     # Simple chat UI
│── README.md
```

---

## API Endpoints

### `POST /api/upload`
Upload student data.
```json
[
  {
    "id": "1",
    "name": "Nguyen Van A",
    "dob": "2001-05-20",
    "address": "Hanoi",
    "hobby": "Reading",
    "skill": "Football"
  }
]
```

### `POST /api/chat`
Ask chatbot a question.
```json
{ "question": "Ai trong lớp biết đá bóng?" }
```

Response:
```json
{ "answer": "Nguyen Van A biết đá bóng." }
```

---

## Notes
- Gemini is used for both embeddings and generating answers
- Pinecone is used for vector similarity search
- If no match is found, chatbot will answer: *"Không có thông tin."*

---

## License
MIT License
