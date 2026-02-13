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

        # 2. Hafıza (Test için gerekirse son_haber.txt dosyasını manuel sil)
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == baslik:
                    print(f"ATLANDI: {baslik}")
                    return

        # 3. Gemini (Detaylı Özet + Tek Kelime)
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]; break

        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = (
            f"Haber: {baslik}. \n"
            "GÖREV: \n"
            "1. Bu haberi en az 3-4 cümlelik, detaylı ve profesyonel bir dille özetle.\n"
            "2. En sona 'KELIME:' yazıp yanına konuyla ilgili TEK BİR İngilizce kelime ekle (Örn: crime, tech, car).\n"
            "Yanıtın mutlaka 'ÖZET:' ile başlasın."
        )
        
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        raw = res_data["candidates"][0]["content"]["parts"][0]["text"]
        
        ozet = raw.split("ÖZET:")[1].split("KELIME:")[0].strip() if "ÖZET:" in raw else raw
        search_term = raw.split("KELIME:")[1].strip().lower().replace(".","").split()[0] if "KELIME:" in raw else "news"

        # 4. GARANTİ RESİM (Unsplash Direct Link)
        # Blogger'ın sevdiği doğrudan CDN formatı
        resim_url = f"https://images.unsplash.com/photo-1585007600263-ad1f301f2c27?auto=format&fit=crop&w=800&q=80" # Genel Haber Resmi
        
        # Kelimeye göre Unsplash'ten rastgele ama doğrudan link çekmeye çalışalım
        if search_term:
            resim_url = f"https://loremflickr.com/800/450/{search_term}/all.jpg"

        resim_html = f'<div class="separator" style="clear: both; text-align: center;"><img border="0" src="{resim_url}" width="100%" style="border-radius:12px; max-width:800px;"/></div><br/>'

        # 5. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<div style='font-family: Arial, sans-serif; line-height: 1.8; font-size: 16px;'>{ozet}</div><br/><b>Kaynak:</b> {kaynak_site}<br/><a href='{link}' style='color:#d93025; font-weight:bold;'>Haberin Devamı İçin Tıklayın...</a>"
        
        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"İŞLEM TAMAM: {baslik} (Kelime: {search_term})")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
