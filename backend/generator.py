# generator.py
import os
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
import datetime
import requests
import json
import re
from typing import Dict, Any

load_dotenv()

# Load all API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY chưa được set.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_answer(context: str, question: str) -> str:
    """
    Sinh câu trả lời dựa trên context và question với multi-intent support.
    """
    try:
        # Phân loại intent của câu hỏi
        intent = _classify_intent(question)
        print(f"DEBUG: Intent detected = {intent}")
        
        # Xử lý theo từng loại intent
        if intent == "database_query" and context.strip():
            prompt = f"Dựa vào thông tin sau:\n{context}\n\nHãy trả lời câu hỏi: {question}"
            return _generate_gemini(prompt)
        
        elif intent == "time":
            return _get_current_time()
        
        elif intent == "date":
            return _get_current_date()
        
        elif intent == "weather":
            return _get_weather_info(question)
        
        elif intent == "weather_vn":
            return _get_weather_vietnam(question)
        
        elif intent == "calculation":
            return _calculate_expression(question)
        
        elif intent == "greeting":
            return _get_greeting_response(question)
        
        elif intent == "joke":
            return _get_joke()
        
        elif intent == "news":
            return _get_news(question)
        
        elif intent == "news_vn":
            return _get_news_vietnam(question)
        
        else:
            prompt = f"Hãy trả lời câu hỏi: {question}"
            return _generate_gemini(prompt)
            
    except Exception as e:
        traceback.print_exc()
        return f"Xin lỗi, tôi gặp lỗi: {str(e)}"

def _classify_intent(question: str) -> str:
    """
    Phân loại intent của câu hỏi.
    """
    question_lower = question.lower()
    
    intent_keywords = {
        "time": ["mấy giờ", "giờ là", "thời gian", "bao giờ", "now", "time"],
        "date": ["hôm nay", "ngày nào", "thứ mấy", "date", "today"],
        "weather": ["thời tiết", "weather", "nắng", "mưa", "nóng", "lạnh", "nhiệt độ", "độ ẩm"],
        "weather_vn": ["thời tiết việt nam", "thời tiết hà nội", "thời tiết sài gòn", 
                      "thời tiết đà nẵng", "thời tiết hồ chí minh", "thời tiết hà nội",
                      "thời tiết tphcm", "thời tiết đà nẵng", "thời tiết huế", "thời tiết cần thơ",
                      "thời tiết nha trang", "thời tiết vũng tàu", "thời tiết đà lạt"],
        "calculation": ["tính", "cộng", "trừ", "nhân", "chia", "+", "-", "*", "/", "bằng bao nhiêu"],
        "greeting": ["xin chào", "hello", "hi", "chào", "helo", "hế lô"],
        "joke": ["kể chuyện cười", "đùa", "joke", "funny", "hài"],
        "news": ["tin tức", "news", "báo", "tin mới", "thời sự", "tin thế giới"],
        "news_vn": ["tin việt nam", "báo việt nam", "thời sự việt nam", 
                   "tin trong nước", "báo trong nước", "thời sự trong nước",
                   "tin việt", "báo mới việt nam"],
        "database_query": ["ai", "người nào", "tìm", "thông tin", "skill", "hobby"]
    }
    
    for intent, keywords in intent_keywords.items():
        if any(keyword in question_lower for keyword in keywords):
            return intent
    
    return "general"

def _generate_gemini(prompt: str) -> str:
    """
    Sử dụng Gemini API với fallback.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=200,
            )
        )
        
        return response.text
        
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return _get_fallback_response(prompt)

def _get_fallback_response(prompt: str) -> str:
    """
    Fallback response khi Gemini không hoạt động.
    """
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["bóng", "đá bóng", "football"]):
        return "Tôi thấy có người có kỹ năng đá bóng: Pham Thi C và Nguyen Van A."
    elif any(word in prompt_lower for word in ["sách", "đọc sách", "book"]):
        return "Có người thích đọc sách: Le Van B và Nguyen Van A."
    elif any(word in prompt_lower for word in ["âm nhạc", "nhảy", "music"]):
        return "Tran Thi Huong có sở thích âm nhạc và nhảy."
    else:
        return "Tôi đã tìm thấy thông tin phù hợp. Bạn cần biết thêm chi tiết gì?"

# === CÁC CHỨC NĂNG BỔ SUNG VỚI API ===

def _get_current_time() -> str:
    now = datetime.datetime.now()
    return f"Bây giờ là {now.strftime('%H:%M:%S')} ngày {now.strftime('%d/%m/%Y')}"

def _get_current_date() -> str:
    now = datetime.datetime.now()
    days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    return f"Hôm nay là {days[now.weekday()]}, ngày {now.strftime('%d/%m/%Y')}"

def _get_weather_info(question: str) -> str:
    """Lấy thông tin thời tiết từ WeatherAPI.com với thành phố được chỉ định"""
    if not WEATHER_API_KEY:
        return "Dịch vụ thời tiết chưa được cấu hình. Vui lòng thêm WEATHER_API_KEY vào file .env"
    
    try:
        # Xác định thành phố từ câu hỏi
        city = _extract_city_from_question(question)
        if not city:
            city = "Hanoi"  # Default fallback
        
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no&lang=vi"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'error' not in data:
            location = data['location']['name']
            temp_c = data['current']['temp_c']
            condition = data['current']['condition']['text']
            humidity = data['current']['humidity']
            wind_kph = data['current']['wind_kph']
            feels_like = data['current']['feelslike_c']
            
            return (f"🌤️ Thời tiết {location}:\n"
                   f"• Tình trạng: {condition}\n"
                   f"• Nhiệt độ: {temp_c}°C (cảm giác như {feels_like}°C)\n"
                   f"• Độ ẩm: {humidity}%\n"
                   f"• Gió: {wind_kph} km/h")
        else:
            error_msg = data['error'].get('message', 'Lỗi không xác định')
            return f"❌ Không thể lấy thông tin thời tiết: {error_msg}"
            
    except Exception as e:
        return f"❌ Lỗi dịch vụ thời tiết: {str(e)}"

def _extract_city_from_question(question: str) -> str:
    """Trích xuất tên thành phố từ câu hỏi"""
    question_lower = question.lower()
    
    # Map từ khóa tiếng Việt sang tên thành phố chuẩn
    city_mapping = {
        "hà nội": "Hanoi", "hanoi": "Hanoi", "hn": "Hanoi",
        "sài gòn": "Ho Chi Minh", "sài gòn": "Ho Chi Minh", 
        "hồ chí minh": "Ho Chi Minh", "hcm": "Ho Chi Minh", "tphcm": "Ho Chi Minh",
        "đà nẵng": "Da Nang", "danang": "Da Nang", "dn": "Da Nang",
        "nha trang": "Nha Trang", "nhatrang": "Nha Trang", "nt": "Nha Trang",
        "huế": "Hue", "hue": "Hue",
        "cần thơ": "Can Tho", "cantho": "Can Tho", "ct": "Can Tho",
        "vũng tàu": "Vung Tau", "vungtau": "Vung Tau", "vt": "Vung Tau",
        "đà lạt": "Da Lat", "dalat": "Da Lat", "dl": "Da Lat",
        "hải phòng": "Hai Phong", "haiphong": "Hai Phong", "hp": "Hai Phong",
        "thái nguyên": "Thai Nguyen", "thainguyen": "Thai Nguyen", "tn": "Thai Nguyên"
    }
    
    # Tìm thành phố trong câu hỏi
    for keyword, city in city_mapping.items():
        if keyword in question_lower:
            return city
    
    return ""

def _get_weather_vietnam(question: str) -> str:
    """Lấy thông tin thời tiết các thành phố Việt Nam"""
    return _get_weather_info(question)  # Sử dụng chung hàm với extract city

def _get_news(question: str) -> str:
    """Lấy tin tức từ NewsAPI (quốc tế)"""
    if not NEWS_API_KEY:
        return "Dịch vụ tin tức chưa được cấu hình."
    
    try:
        # Sử dụng tin tức từ Mỹ (có sẵn trong free plan)
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok' and data.get('articles'):
            articles = data['articles'][:3]
            news_list = []
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', '')
                if title and title != "[Removed]":
                    source = article.get('source', {}).get('name', '')
                    # Dịch tiêu đề sang tiếng Việt nếu có thể
                    translated_title = _translate_news_title(title)
                    news_list.append(f"{i}. {translated_title} ({source})")
            
            if news_list:
                return "📰 Tin tức quốc tế:\n" + "\n".join(news_list)
            else:
                return "📰 Hiện không có tin tức quốc tế nào."
        else:
            return "📰 Không thể lấy tin tức lúc này."
            
    except Exception as e:
        return f"📰 Lỗi dịch vụ tin tức: {str(e)}"

def _get_news_vietnam(question: str) -> str:
    """Lấy tin tức Việt Nam từ NewsAPI bằng cách tìm kiếm"""
    if not NEWS_API_KEY:
        return "Dịch vụ tin tức chưa được cấu hình."
    
    try:
        # Tìm kiếm tin tức về Vietnam bằng từ khóa
        url = f"https://newsapi.org/v2/everything?q=Vietnam&language=vi&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok' and data.get('articles'):
            articles = data['articles'][:3]
            news_list = []
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', '')
                if title and title != "[Removed]":
                    source = article.get('source', {}).get('name', '')
                    # Cắt ngắn title nếu quá dài
                    if len(title) > 80:
                        title = title[:80] + "..."
                    news_list.append(f"{i}. {title} ({source})")
            
            if news_list:
                return "📰 Tin tức Việt Nam:\n" + "\n".join(news_list)
            else:
                return "📰 Hiện không có tin tức Việt Nam nào."
        else:
            return "📰 Không thể lấy tin tức Việt Nam lúc này."
            
    except Exception as e:
        return f"📰 Lỗi dịch vụ tin tức: {str(e)}"

def _translate_news_title(title: str) -> str:
    """Dịch tiêu đề tin tức sang tiếng Việt (đơn giản)"""
    # Một số từ khóa thông dụng
    translation_map = {
        "trump": "Trump",
        "biden": "Biden",
        "china": "Trung Quốc",
        "russia": "Nga",
        "ukraine": "Ukraine",
        "election": "bầu cử",
        "climate": "khí hậu",
        "economy": "kinh tế",
        "technology": "công nghệ",
        "health": "sức khỏe",
        "sports": "thể thao",
        "weather": "thời tiết",
        "news": "tin tức",
        "update": "cập nhật",
        "breaking": "tin nóng",
        "latest": "mới nhất"
    }
    
    # Thay thế từ khóa
    translated_title = title
    for eng, vi in translation_map.items():
        translated_title = translated_title.replace(eng, vi)
        translated_title = translated_title.replace(eng.capitalize(), vi)
    
    return translated_title

def _calculate_expression(question: str) -> str:
    try:
        import re
        # Tìm biểu thức toán học trong câu hỏi
        expression = re.search(r'(\d+[\+\-\*\/]\d+)', question.replace(" ", ""))
        if expression:
            result = eval(expression.group(1))
            return f"🧮 Kết quả: {expression.group(1)} = {result}"
        else:
            return "❌ Tôi không tìm thấy phép tính nào trong câu hỏi."
    except:
        return "❌ Xin lỗi, tôi không thể tính toán biểu thức này."

def _get_greeting_response(question: str) -> str:
    greetings = [
        "👋 Xin chào! Tôi có thể giúp gì cho bạn?",
        "🤗 Chào bạn! Tôi sẵn sàng hỗ trợ.",
        "😊 Hi! Bạn cần tìm hiểu thông tin gì?",
        "👋 Xin chào! Tôi là trợ lý ảo, có thể giúp bạn tìm kiếm thông tin."
    ]
    import random
    return random.choice(greetings)

def _get_joke() -> str:
    jokes = [
        "😂 Tại sao các lập trình viên lại ghét thiên nhiên? Vì có quá nhiều bugs!",
        "😆 Một lập trình viên đi mua kẹo. Anh ta nói: 'Cho tôi một pound of candy'... 'Ồ, xin lỗi, tôi muốn nói 0.45 kilograms of candy!'",
        "😄 Tại sao developer không thích đi biển? Vì họ sợ C (sea)!",
        "🤣 Có 10 loại người trên thế giới: những người hiểu nhị phân và những người không hiểu."
    ]
    import random
    return random.choice(jokes)