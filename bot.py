import os
import feedparser
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
        
        # ELİNDEKİ MODELLERİ LİSTELE VE ÇALIŞANI SEÇ
        available_models = [m.name for m in client.models.list()]
        print(f"Erişilebilir modeller: {available_models}")
        
        # En güvenli modellerden birini seç (Listerden gelen isme göre)
        model_id = ""
        for m in ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]:
            # Model isminin başında 'models/' olup olmadığını kontrol ederek eşleştir
            if any(m in name for name in available_models):
                model_id = next(name for name in available_models if m in name)
                break
        
        if not model_id:
            print("Uygun model bulunamadı!")
            return

        print(f"Seçilen model: {model_id}")

        # Haber Kaynağı
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        entry = feed.entries[0]
        
        # Gemini ile Özet (Prompt kısmını çok sadeleştirdim)
        response = client.models.generate_content(
            model=model_id,
            contents=f"Özetle: {entry.title} - {entry.summary}"
        )
        ozet = response.text

        # Blogger
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
        print(f"BAŞARIYLA PAYLAŞILDI: {entry.title}")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
