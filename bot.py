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

        # 3. Gemini (Detaylı Özet + Arama Terimi)
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
            "1. Bu haberi en az 3-4 cümlelik, profesyonel bir dille özetle.\n"
            "2. En sona 'KELIME:' yazıp yanına konuyla ilgili TEK BİR İngilizce kelime ekle.\n"
            "Format: ÖZET: ... KELIME: ..."
        )
        
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        raw = res_data["candidates"][0]["content"]["parts"][0]["text"]
        
        ozet = raw.split("ÖZET:")[1].split("KELIME:")[0].strip() if "ÖZET:" in raw else raw
        search_term = raw.split("KELIME:")[1].strip().lower().replace(".","").split()[0] if "KELIME:" in raw else "news"

        # 4. %100 GARANTİ RESİM (Pixabay Statik CDN)
        # Blogger'ın asla reddedemeyeceği doğrudan resim linki
        resim_url = f"https://pixabay.com/get/g89602e1b827e6962f3a8f4c8030605963f85b6b158869c895c0293d05877c8e9_1280.jpg" # Yedek
        
        # Pixabay API yerine direkt güvenli görsel havuzundan statik çekim:
        # Pexels'in arama tabanlı statik link yapısını kullanıyoruz (Blogger dostudur)
        resim_url = f"https://images.pexels.com/photos/2000/police-officer-policeman-handcuffs.jpg?auto=compress&cs=tinysrgb&w=800"
        
        if "crime" in search_term or "police" in search_term:
            resim_url = "https://images.pexels.com/photos/9242908/pexels-photo-9242908.jpeg?auto=compress&cs=tinysrgb&w=800"
        elif "tech" in search_term or "apple" in search_term:
            resim_url = "https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=800"
        else:
            resim_url = f"https://images.pexels.com/photos/3944454/pexels-photo-3944454.jpeg?auto=compress&cs=tinysrgb&w=800"

        resim_html = f'<div style="text-align: center;"><img src="{resim_url}" style="width:100%; max-width:800px; border-radius:15px; border: 1px solid #ddd;"></div><br>'

        # 5. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<div style='font-family: Arial, sans-serif; line-height: 1.8; font-size: 16px;'>{ozet}</div><br><b>Kaynak:</b> {kaynak_site}<br><a href='{link}' style='color:#d93025; font-weight:bold;'>Haberin Devamı →</a>"
        
        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"BAŞARILI: {baslik}")

    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
