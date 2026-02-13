import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        blog_id = os.environ.get('BLOGGER_BLOG_ID')
        
        # 1. Haberleri Çek
        news_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
        feed = feedparser.parse(news_url)
        if not feed.entries: return
        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link
        kaynak_site = entry.source.get('title', 'Haber Kaynağı') if hasattr(entry, 'source') else "Haber Kaynağı"

        # 2. Hafıza Kontrolü
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == baslik:
                    print(f"ATLANDI: {baslik}")
                    return

        # 3. Gemini Model Seçimi
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]; break

        # 4. Gemini'den Özet ve İngilizce Anahtar Kelime Al
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = f"Şu haberi kısa ve etkileyici özetle: {baslik}. En sona 'KEY:' yazıp yanına konuyla ilgili tek bir ingilizce kelime ekle."
        
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Ayıklama
        anahtar = "news"
        if "KEY:" in raw_text:
            ozet_part = raw_text.split("KEY:")[0].strip()
            anahtar = raw_text.split("KEY:")[1].strip().replace("*","").lower()
        else:
            ozet_part = raw_text

        # 5. GARANTİ RESİM YOLU (Blogger'ın En Sevdiği Format)
        # Unsplash'in doğrudan CDN linkini kullanıyoruz
        resim_url = f"https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80" # Varsayılan
        if anahtar:
            resim_url = f"https://source.unsplash.com/featured/800x450?{anahtar}"
            # Blogger yönlendirmeyi sevmediği için linki bir kez çözüyoruz
            try:
                r = requests.get(resim_url, timeout=5)
                if r.status_code == 200:
                    resim_url = r.url # Yönlendirilmiş gerçek resim linkini al
            except: pass

        resim_html = f'<div style="text-align: center; margin-bottom: 20px;"><img src="{resim_url}" style="width: 100%; max-width: 800px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"></div>'

        # 6. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<p style='font-size: 1.1em; line-height: 1.6;'>{ozet_part}</p><br><b>Kaynak:</b> {kaynak_site}<br><a href='{link}' style='color: #d93025; font-weight: bold;'>Haberin Devamı →</a>"
        
        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"PAYLAŞILDI: {baslik} (Kategori: {anahtar})")

    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
