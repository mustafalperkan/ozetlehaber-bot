import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        
        # 1. Hangi modele iznimiz olduğunu otomatik bulalım
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        
        # Listeden 'flash' içeren en güncel modeli seç
        target_model = "models/gemini-1.5-flash" # Varsayılan
        if "models" in list_res:
            flash_models = [m["name"] for m in list_res["models"] if "flash" in m["name"].lower()]
            if flash_models:
                # En uzun isimli olan genelde en güncelidir (ör: flash-latest)
                target_model = sorted(flash_models, key=len, reverse=True)[0]
        
        print(f"Sistem tarafından seçilen model: {target_model}")

        # 2. Haber Kaynağı
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        entry = feed.entries[0]
        
        # 3. Özet İsteği (Artık model ismini dinamik gönderiyoruz)
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": f"Aşağıdaki haberi özetle: {entry.title}\n\n{entry.summary}"}]
            }]
        }
        
        response = requests.post(gen_url, json=payload)
        res_data = response.json()
        
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Gemini Hatası: {res_data}")
            return

        # 4. Blogger Paylaşım
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
        print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
