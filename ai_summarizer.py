import os
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# 1. Inisialisasi Gemini Client
# Pastikan kamu sudah menyimpan GEMINI_API_KEY di Environment Variables
def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

# 2. Ekstraktor Konten Artikel dari URL (Scraper Sederhana)
def extract_article_content(url):
    """
    Mengambil paragraf teks dari halaman web artikel berita.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Mengambil semua tag <p> (paragraf) dari halaman artikel
        paragraphs = soup.find_all("p")
        article_text = "\n".join([p.get_text().strip() for p None in paragraphs if len(p.get_text().strip()) > 30])
        
        # Ambil maksimal 4000 karakter agar hemat token & cepat
        return article_text[:4000] if article_text else None
    except Exception as e:
        print(f"Error extracting content: {e}")
        return None

# 3. Fungsi Utama AI Summarizer (Single-Source)
def summarize_news_article(url, raw_summary=""):
    """
    Meringkas 1 artikel spesifik dari sumbernya menggunakan Gemini API.
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ **Error:** API Key Gemini tidak ditemukan. Harap atur GEMINI_API_KEY di environment variable Anda."

    # Ambil konten teks asli artikel
    full_text = extract_article_content(url)
    
    # Jika gagal scraping teks utuh, gunakan ringkasan bawaan dari RSS Feed
    text_to_analyze = full_text if full_text else raw_summary
    
    if not text_to_analyze:
        return "⚠️️ Gagal mengekstrak isi artikel untuk diringkas."

    # Prompt Engineering Khusus Single-Source Summarizer
    prompt = f"""
    Kamu adalah asisten analis berita profesional. Tugasmu adalah membuat ringkasan tajam dan mudah dipahami dari HANYA SATU ARTIKEL BERITA berikut.

    ISI ARTIKEL:
    {text_to_analyze}

    PETUNJUK FORMAT OUTPUT:
    1. **Ringkasan Inti (1-2 Kalimat)**: Jelaskan fenomena/peristiwa utama.
    2. **Poin-Poin Kunci (Key Takeaways)**: Gunakan bullet points (maksimal 3-4 poin).
    3. **Konteks/Dampak**: Catatan singkat mengenai implikasi berita ini.
    
    Gunakan Bahasa Indonesia yang lugas, profesional, dan mudah dipahami.
    """

    try:
        # Menggunakan model gemini-2.5-flash yang cepat & hemat token
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3, # Low temperature agar konsisten & faktual
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ Terjadi kesalahan saat memproses AI Summarizer: {str(e)}"
