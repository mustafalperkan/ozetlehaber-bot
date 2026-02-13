import google.generativeai as genai
import os
import feedparser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# API Ayarları (GitHub Secrets'tan alır)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
BLOG_ID = os.environ.get('BLOGGER_BLOG_ID')
CLIENT_ID = os.environ.get('BLOGGER_CLIENT_ID')
CLIENT_SECRET = os.environ.get('BLOGGER_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('BLOGGER_REFRESH_TOKEN')

def run_bot():
    try:
        # Gemini Kurulumu
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')

        # Haber Kaynağı (RSS)
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        if not feed.entries:
            print("Haber bulunamadı.")
            return

        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link

        # Gemini ile Özet Oluşturma
        prompt = f"Aşağıdaki haberi 30 saniyede okunacak şekilde, dikkat çekici ve profesyonel bir dille özetle. Başlıkta mutlaka haberin ana konusunu kullan. Haberin linki: {link}"
        response = model.generate_content(prompt + entry.summary)
        ozet = response.text

        # Blogger Bağlantısı
        creds = Credentials(
            None,
            refresh_token=REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
        service = build('blogger', 'v3', credentials=creds)

        # Blogger'da Paylaşma
        post_data = {
            'title': baslik,
            'content': f"{ozet}<br><br>Kaynak: <a href='{link}'>{link}</a>"
        }

        service.posts().insert(blogId=BLOG_ID, body=post_data).execute()
        print(f"Başarıyla paylaşıldı: {baslik}")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
