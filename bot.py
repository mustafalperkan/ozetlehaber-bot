import os
import feedparser
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        # Yeni Nesil Gemini Kurulumu
        client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
        model_id = "gemini-1.5-flash"

        # Haber Kaynağı (RSS)
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        if not feed.entries:
            print("Haber bulunamadı.")
            return

        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link

        # Yeni Nesil Gemini ile Özet Oluşturma
        prompt = f"Aşağıdaki haberi 30 saniyede okunacak şekilde özetle. Link: {link}\n\nİçerik: {entry.summary}"
        response = client.models.generate_content(model=model_id, contents=prompt)
        ozet = response.text

        # Blogger Bağlantısı
        creds = Credentials(
            None,
            refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'),
        )
        service = build('blogger', 'v3', credentials=creds)

        # Blogger'da Paylaşma
        post_data = {
            'title': baslik,
            'content': f"{ozet}<br><br>Kaynak: <a href='{link}'>{link}</a>"
        }

        service.posts().insert(blogId=os.environ.get('BLOGGER_BLOG_ID'), body=post_data).execute()
        print(f"BAŞARIYLA PAYLAŞILDI: {baslik}")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
