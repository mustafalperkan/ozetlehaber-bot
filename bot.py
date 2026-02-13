import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        blog_id = os.environ.get('BLOGGER_BLOG_ID')
        
        # 1. Google News Türkiye
        news_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
        feed = feedparser.parse(news_url)
        if not feed.entries: return

        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link
        
        # Kaynak ismini daha güvenli alalım
        kaynak_site = "Haber Kaynağı"
        if hasattr(entry, 'source'):
            kaynak_site = entry.source.get('title', 'Haber Kaynağı')

        # 2. Hafıza Kontrolü
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == baslik:
                    print(f"ATLANDI (Zaten paylaşıldı): {baslik}")
                    return

        # 3. Gemini Model Seçimi
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]
                    break

        # 4. Gemini ile Özet ve Resim
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = f"Haber Başlığı: {baslik}. Bu haberi profesyonel bir blog yazısı gibi özetle. En başa konuyla ilgili rastgele bir Unsplash resim linkini <img> etiketiyle koy."
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res_data = requests.post(gen_url, json=payload).json()
        
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Gemini yanıt veremedi.")
            return

        # 5. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        post_data = {
            'title': baslik,
            'content': f"{ozet}<br><br><b>Kaynak:</b> {kaynak_site}<br><a href='{link}'>Haberin Devamı</a>"
        }
        service.posts().insert(blogId=blog_id, body=post_data).execute()

        # 6. Hafızayı Yaz
        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"BAŞARIYLA PAYLAŞILDI: {baslik}")

    except Exception as e:
        print(f"BİR HATA OLDU: {e}")

if __name__ == "__main__":
    run_bot()
