import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        blog_id = os.environ.get('BLOGGER_BLOG_ID')
        
        # 1. Haber Çek
        news_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
        feed = feedparser.parse(news_url)
        if not feed.entries: return
        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link
        kaynak_site = entry.source.get('title', 'Haber Kaynağı') if hasattr(entry, 'source') else "Haber Kaynağı"

        # 2. Hafıza
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == baslik:
                    print(f"ATLANDI: {baslik}")
                    return

        # 3. Gemini
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]; break

        # 4. Özet
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = f"Şu haberi kısa özetle: {baslik}. Türkçe olsun."
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        ozet = res_data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in res_data else "Haber özeti hazırlanıyor..."

        # 5. GARANTİ GÖRSEL (Blogger ve Google dostu yüksek kaliteli statik link)
        # Yönlendirme olmayan, doğrudan CDN linki kullanıyoruz.
        resim_url = "https://images.pexels.com/photos/3944454/pexels-photo-3944454.jpeg?auto=compress&cs=tinysrgb&w=800"
        
        # Eğer haberde "operasyon, polis, gözaltı" gibi kelimeler varsa daha uygun bir resim seçelim
        if any(word in baslik.lower() for word in ["operasyon", "polis", "gözaltı", "şüpheli"]):
            resim_url = "https://images.pexels.com/photos/9242908/pexels-photo-9242908.jpeg?auto=compress&cs=tinysrgb&w=800"

        resim_html = f'<div style="text-align: center; margin-bottom: 20px;"><img src="{resim_url}" border="0" width="100%" style="border-radius:12px; max-width:800px;"></div>'

        # 6. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<p style='font-family: sans-serif; font-size: 1.1em;'>{ozet}</p><br><b>Kaynak:</b> {kaynak_site}<br><a href='{link}' style='color: #d93025;'>Haberin Devamı →</a>"
        
        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"PAYLAŞILDI: {baslik}")

    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
