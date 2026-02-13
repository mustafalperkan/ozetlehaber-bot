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
        kaynak_site = entry.source.get('title', 'Haber Kaynağı') if hasattr(entry, 'source') else "Haber Kaynağı"

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
                    target_model = m["name"]; break

        # 4. Gemini'den Özet ve İngilizce Anahtar Kelime İste
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        prompt = (
            f"Haber Başlığı: {baslik}. \n"
            "Görevlerin:\n"
            "1. Haberi profesyonel, merak uyandırıcı ve kısa bir dille özetle.\n"
            "2. Bu haberin ana konusunu temsil eden İngilizce TEK BİR KELİME yaz (Örn: 'business', 'cybersecurity', 'football', 'earthquake', 'space').\n"
            "Yanıtını şu formatta ver:\n"
            "ÖZET: [Buraya özet gelecek]\n"
            "ANAHTAR: [Buraya ingilizce kelime gelecek]"
        )
        
        res_data = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Yanıtı parçalayalım
        ozet_part = raw_text.split("ÖZET:")[1].split("ANAHTAR:")[0].strip()
        anahtar_kelime = raw_text.split("ANAHTAR:")[1].strip().lower()

        # 5. AKILLI RESİM SEÇİMİ
        # Unsplash üzerinden konuyla ilgili en iyi görseli çeker
        resim_url = f"https://source.unsplash.com/featured/800x450?{anahtar_kelime}"
        resim_html = f'<div style="text-align: center;"><img src="{resim_url}" width="100%" style="border-radius:12px; margin-bottom:20px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);"></div>'

        # 6. Blogger Paylaşım
        creds = Credentials(None, refresh_token=os.environ.get('BLOGGER_REFRESH_TOKEN'),
                            token_uri="https://oauth2.googleapis.com/token",
                            client_id=os.environ.get('BLOGGER_CLIENT_ID'),
                            client_secret=os.environ.get('BLOGGER_CLIENT_SECRET'))
        service = build('blogger', 'v3', credentials=creds)

        full_content = f"{resim_html}<div style='font-size: 1.1em; line-height: 1.8;'>{ozet_part}</div><br><br><b>Kaynak:</b> {kaynak_site}<br><a href='{link}' style='color: #d93025; text-decoration: none; font-weight: bold;'>Haberin Detayları İçin Tıklayın →</a>"

        service.posts().insert(blogId=blog_id, body={'title': baslik, 'content': full_content}).execute()

        with open("son_haber.txt", "w", encoding="utf-8") as f:
            f.write(baslik)
            
        print(f"BAŞARIYLA PAYLAŞILDI ({anahtar_kelime}): {baslik}")

    except Exception as e: print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
