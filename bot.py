import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        # 1. Gemini'ye Kütüphanesiz, Doğrudan İstek Atıyoruz (En Garanti Yol)
        api_key = os.environ.get('GEMINI_API_KEY')
        
        # Haber Kaynağı
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        entry = feed.entries[0]
        
        # Saf HTTP isteği ile Gemini'den özet alalım
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": f"Aşağıdaki haberi profesyonelce özetle: {entry.title}\n\n{entry.summary}"}]
            }]
        }
        
        response = requests.post(url, json=payload)
        res_data = response.json()
        
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Gemini Hatası: {res_data}")
            return

        # 2. Blogger Bağlantısı
        creds = Credentials(
            None,
            refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'),
        )
        service = build('blogger', 'v3', credentials=creds)

        post_data = {
            'title': entry.title,
            'content': f"{ozet}<br><br>Kaynak: <a href='{entry.link}'>{entry.link}</a>"
        }

        service.posts().insert(blogId=os.environ.get('BLOGGER_BLOG_ID'), body=post_data).execute()
        print(f"MÜJDE! BAŞARIYLA PAYLAŞILDI: {entry.title}")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
