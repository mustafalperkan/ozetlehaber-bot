import os
import feedparser
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def run_bot():
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        
        # 1. Google'a soruyoruz: "Bana hangi modelleri kullanma izni verdin?"
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_res = requests.get(list_url).json()
        
        # 2. Listeden çalışan ilk modeli bulalım (Hata payını sıfırlıyoruz)
        target_model = ""
        if "models" in list_res:
            for m in list_res["models"]:
                if "generateContent" in m["supportedGenerationMethods"]:
                    target_model = m["name"]
                    break
        
        if not target_model:
            print("Uygun model bulunamadı, liste:", list_res)
            return

        print(f"Sistem senin için en uygun modeli buldu ve seçti: {target_model}")

        # 3. Haber Kaynağı
        feed = feedparser.parse("https://www.donanimhaber.com/rss/tum/")
        entry = feed.entries[0]
        
        # 4. Özet İsteği
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"Aşağıdaki haberi özetle: {entry.title}\n\n{entry.summary}"}]}]
        }
        
        response = requests.post(gen_url, json=payload)
        res_data = response.json()
        
        if "candidates" in res_data:
            ozet = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Gemini Hatası: {res_data}")
            return

        # 5. Blogger Paylaşım
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
        print(f"ZAFER! BAŞARIYLA PAYLAŞILDI: {entry.title}")

    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    run_bot()
