import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        blog_id = os.environ.get('BLOGGER_BLOG_ID')
        
        # 1. Google News
        news_url = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"
        feed = feedparser.parse(news_url)
        if not feed.entries: return

        entry = feed.entries[0]
        baslik = entry.title
        link = entry.link
        kaynak_site = entry.source.get('title', 'Haber Kaynağı') if hasattr(entry, 'source') else "Haber Kaynağı"

        # 2. Hafıza (Test için gerekirse son_haber.txt dosyasını sil)
        if os.path.exists("son_haber.txt"):
            with open("son_haber.txt", "r", encoding="utf-8") as f:
                if f.read().strip() == baslik:
                    print(f"ATLANDI: {baslik}")
                    return

        # 3. Gemini Özet
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        target_model = "models/gemini-1.5-flash"
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]; break

        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = f"Şu haberi ilgi çekici ve kısa özetle: {baslik}. Yazı Türkçe olsun."
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        ozet = res_data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in res_data else "Haber detayı hazırlanıyor..."

        # 4. EN STABİL RESİM (Blogger'ın asla reddetmediği format)
        # Placeholder yerine gerçek bir görsel havuzundan statik link
        resim_url = f"https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80"
        resim_html = f'<div class="separator" style="clear: both; text-align: center;"><img border="0" src="{resim_url}" width="100%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/></div><br/>'

        # 5. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<p style='font-family: Arial, sans-serif; line-height: 1.6;'>{ozet}</p><br/><b>Kaynak:</b> {kaynak_site}<br/><a href='{link}'>Haberin Devamı için Tıklayın</a>"

        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"BAŞARIYLA PAYLAŞILDI: {baslik}")

    except Exception as e: print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
