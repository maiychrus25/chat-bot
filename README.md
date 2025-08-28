#                                                   🎓 Student RAG Chatbot

This project is a simple **RAG (Retrieval-Augmented Generation) chatbot** that helps answer questions about students in a class, with enhanced capabilities including **weather information** and **news updates**.

---

## 🌟 Enhanced Features
- **Student Information Retrieval**: Ask about student skills, hobbies, and information  
- **Weather Information**: Get current weather data for various locations using [WeatherAPI.com](https://www.weatherapi.com/)  
- **News Updates**: Fetch latest news (international and Vietnam-specific) using [NewsAPI.org](https://newsapi.org/)  
- **Multi-intent Recognition**: Automatically detects question types (weather, news, calculation, etc.)  
- **Natural Language Processing**: Powered by **Google's Gemini AI** for intelligent responses  
- **Simple Web Interface**: Clean chat UI with emoji support  

---

## 🛠️ Technology Stack
- **Backend**: Flask (Python web framework)  
- **Frontend**: HTML, JavaScript, CSS  
- **Vector Database**: Pinecone for semantic search  
- **AI/ML**: Google Gemini API for embeddings and generation  
- **APIs**:
  - WeatherAPI.com (weather data)  
  - NewsAPI (news feeds)  
- **Environment Management**: python-dotenv  

---

## 📋 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/maiychrus25/chat-bot.git
cd student-rag-chatbot
```

### 2. Create and activate virtual environment
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root with your API keys:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_weatherapi_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### 5. Get API Keys
- **Gemini API Key**: Visit [Google AI Studio](https://aistudio.google.com/) → create new key → add to `.env`  
- **WeatherAPI.com Key**: Sign up at [WeatherAPI.com](https://www.weatherapi.com/) → get key → add to `.env`  
- **NewsAPI Key**: Register at [NewsAPI.org](https://newsapi.org/) → get free key → add to `.env`  
- **Pinecone Setup**: Sign up at [Pinecone.io](https://www.pinecone.io/) → create project + index → add API key & env to `.env`  

---

## 🚀 Running the Application

### Option 1: Run Backend Only
```bash
python app.py
```

### Option 2: Run with Live Frontend Server
```bash
# Terminal 1: Start Flask backend
python app.py

# Terminal 2: Start HTTP server for frontend
cd frontend
python -m http.server 3000
```

Or use **Live Server** extension in VSCode → right-click `index.html` → *Open with Live Server*  

**Access the Application**  
- Backend API: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
- Frontend: [http://127.0.0.1:3000](http://127.0.0.1:3000)  

---

## 📁 Project Structure
```
student-rag-chatbot/
│
├── app.py                 # Flask backend API
├── generator.py           # Enhanced response generator with multi-API support
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (ignored by git)
├── .gitignore             # Git ignore rules
│
├── frontend/
│   ├── index.html         # Chat interface
│   ├── style.css          # Styling
│   └── script.js          # Frontend functionality
│
└── README.md              # Project documentation
```

---

## 🔌 API Endpoints

### `POST /api/upload`
Upload student data to Pinecone vector database.  

**Request Body**:
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
Ask the chatbot a question.  

**Request Body**:
```json
{
  "question": "Ai trong lớp biết đá bóng?",
  "context": "Optional context for better answers"
}
```

**Response**:
```json
{
  "answer": "Nguyen Van A biết đá bóng."
}
```

---

## 💬 Example Questions

### Student Information
- "Ai có kỹ năng đá bóng?"  
- "Những ai thích đọc sách?"  
- "Tìm học sinh có sở thích âm nhạc"  

### Weather Questions
- "Thời tiết Hà Nội thế nào?"  
- "Thời tiết Sài Gòn"  
- "Nhiệt độ Đà Nẵng bao nhiêu?"  

### News Questions
- "Tin tức mới nhất"  
- "Tin Việt Nam hôm nay"  
- "Báo mới"  

### General Questions
- "Mấy giờ rồi?"  
- "Hôm nay thứ mấy?"  
- "Tính 15 + 20"  
- "Kể chuyện cười"  

---

## 🐛 Troubleshooting

### Common Issues
- **API Keys Not Working**:
  - Ensure keys are in `.env` file  
  - WeatherAPI keys may take a few hours to activate  
  - NewsAPI free tier only works on localhost  

- **Module Not Found Errors**:
  - Ensure virtual environment is activated  
  - Run `pip install -r requirements.txt` again  

- **CORS Errors**:
  - Ensure you run frontend via HTTP server (not from file system)  

- **Port Already in Use**:
  - Change ports in code or run:  
    ```bash
    lsof -ti:5000 | xargs kill
    ```

### Debug Mode
Enable debug prints in `generator.py` by uncommenting print statements.

---

## 📝 License
MIT License – feel free to use this project for learning and development purposes.  

---

## 🤝 Contributing
1. Fork the repository  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add some amazing feature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request  

---

## 📞 Support
If you have any questions or issues, please create an issue in the GitHub repository or contact the development team.  

---

✨ Happy Coding! 🚀
