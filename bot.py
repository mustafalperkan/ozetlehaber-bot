import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        # 1. Ayarları Al
        api_key = os.environ.get('GEMINI_API_KEY')
        blog_id = os.environ.get('BLOGGER_BLOG_ID')
        
        # 2. Haber Kaynağını Oku (DonanımHaber)
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        if not feed.entries:
            print("Haber bulunamadı.")
            return
        
        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link
        icerik = entry.summary if hasattr(entry, 'summary') else baslik

        # 3. Gemini'ye Doğrudan İstek At (V1 Kararlı Sürüm)
        # v1beta yerine v1 kullanarak 404 hatasını bypass ediyoruz
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Aşağıdaki haberi profesyonel bir dille kısa özetle. Haberin linkini de belirt: {baslik}\n\nİçerik: {icerik}"}]
            }]
        }
        
        response = requests.post(url, json=payload)
        res_data = response.json()
        
        # Yanıt Kontrolü
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Eğer hala hata verirse ne olduğunu tam görelim
            print(f"Gemini Cevap Hatası: {res_data}")
            return

        # 4. Blogger Bağlantısı ve Paylaşım
        creds = Credentials(
            None,
            refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'),
        )
        service = build('blogger', 'v3', credentials=creds)

        post_data = {
            'title': baslik,
            'content': f"{ozet}<br><br>Kaynak: <a href='{link}'>{link}</a>"
        }

        service.posts().insert(blogId=blog_id, body=post_data).execute()
        print(f"MÜJDE! BAŞARIYLA PAYLAŞILDI: {baslik}")

    except Exception as e:
        print(f"SİSTEM HATASI: {e}")

if __name__ == "__main__":
    run_bot()
