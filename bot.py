import os
import feedparser
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# GitHub Secrets'tan verileri al
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
CLIENT_ID = os.getenv('BLOGGER_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLOGGER_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('BLOGGER_REFRESH_TOKEN')

# ANAHTAR KONTROLÜ (Hata buradaysa bizi uyaracak)
if not all([GEMINI_KEY, BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    print("HATA: GitHub Secrets eksik veya okunamıyor!")
    print(f"Client ID mevcut mu?: {bool(CLIENT_ID)}")
    exit(1)

# Gemini Yapılandırması
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    if not creds.valid:
        creds.refresh(Request())
    return build('blogger', 'v3', credentials=creds)

def summarize(title, link):
    prompt = f"Haber Başlığı: {title}. Link: {link}. Bu haberi 3 maddede özetle ve HTML formatında ver."
    response = model.generate_content(prompt)
    return response.text

try:
    feed = feedparser.parse("https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr")
    service = get_blogger_service()
    item = feed.entries[0]
    summary_html = summarize(item.title, item.link)

    body = {
        "kind": "blogger#post",
        "title": item.title,
        "content": summary_html + f"<br><br><a href='{item.link}'>Kaynağa git</a>"
    }

    service.posts().insert(blogId=BLOG_ID, body=body).execute()
    print(f"BAŞARILI: {item.title} paylaşıldı!")
except Exception as e:
    print(f"HATA OLUŞTU: {e}")
