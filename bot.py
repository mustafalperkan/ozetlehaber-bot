import os
import feedparser
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# GitHub Secrets'tan verileri al
GEMINI_KEY = os.environ['GEMINI_API_KEY']
BLOG_ID = os.environ['BLOGGER_BLOG_ID']
CLIENT_ID = os.environ['BLOGGER_CLIENT_ID']
CLIENT_SECRET = os.environ['BLOGGER_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['BLOGGER_REFRESH_TOKEN']

# Gemini Yapılandırması
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_blogger_service():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    if not creds.valid:
        creds.refresh(Request())
    return build('blogger', 'v3', credentials=creds)

def summarize(title, link):
    prompt = f"Şu haberi 'Özetle' formatında hazırla. Başlık: {title}. Link: {link}. Format: Kısa başlık, 3 madde özet, 1 cümle 'Neden Önemli?' analizi. HTML formatında (<b>, <ul>, <li> kullanarak) ver."
    response = model.generate_content(prompt)
    return response.text

# Google News TR RSS
feed = feedparser.parse("https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr")
service = get_blogger_service()

# Sadece en son haberi paylaş (test için 1 tane)
item = feed.entries[0]
summary_html = summarize(item.title, item.link)

body = {
    "kind": "blogger#post",
    "title": item.title,
    "content": summary_html + f"<br><br><a href='{item.link}'>Kaynağa git</a>"
}

service.posts().insert(blogId=BLOG_ID, body=body).execute()
print(f"Başarıyla paylaşıldı: {item.title}")
