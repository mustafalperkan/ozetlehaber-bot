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
        kaynak_site = entry.source.text if hasattr(entry, 'source') else "Haber Kaynağı"

        # 2. Hafıza Kontrolü (Aynı haberi tekrar paylaşmamak için)
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r") as f:
                if f.read().strip() == baslik:
                    print(f"BU HABER ZATEN PAYLAŞILDI: {baslik}")
                    return

        # 3. Gemini Modelini Seç
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]; break

        # 4. Gemini ile İçerik ve Resim Linki Oluşturma
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = f"Haber: {baslik}. Bu haberi profesyonel özetle. Ayrıca haberle ilgili konuyu temsil eden geniş bir görselin Unsplash linkini (örneğin teknoloji ise https://images.unsplash.com/photo-1518770660439-4636190af475) içeriğin en başına <img> etiketiyle ekle."
        
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else: return

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

        # 6. Hafızaya Kaydet
        with open("son_haber.txt", "w") as f:
            f.write(baslik)
            
        print(f"RESİMLİ HABER PAYLAŞILDI: {baslik}")

    except Exception as e: print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
