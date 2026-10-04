import feedparser
import pandas as pd
from datetime import datetime

# Daftar sumber RSS Feed Berita Nasional yang stabil & gratis
NEWS_SOURCES = {
    "Antara News (Topik Utama)": "https://www.antaranews.com/rss/top-news.xml",
    "Republika (Terbaru)": "https://republika.co.id/rss",
    "CNN Indonesia (Teknologi)": "https://www.cnnindonesia.com/teknologi/rss",
    "CNBC Indonesia (Market)": "https://www.cnbcindonesia.com/market/rss"
}

def fetch_news_feed(limit_per_source=10):
    """
    Mengambil data RSS Feed dari berbagai sumber berita,
    membersihkannya, dan mengembalikan Pandas DataFrame yang terurut kronologis.
    """
    all_articles = []

    for source_name, rss_url in NEWS_SOURCES.items():
        try:
            # Parse feed menggunakan feedparser
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:limit_per_source]:
                # Ekstraksi komponen utama artikel
                title = entry.get("title", "Tanpa Judul")
                link = entry.get("link", "")
                
                # Mengambil ringkasan awal (summary/description)
                summary = entry.get("summary", entry.get("description", "Tidak ada ringkasan."))
                
                # Tanggal publikasi
                published = entry.get("published", entry.get("updated", "Waktu tidak diketahui"))
                
                all_articles.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "summary_raw": summary,
                    "published": published
                })
        except Exception as e:
            print(f"Gagal mengambil feed dari {source_name}: {e}")

    # Ubah list dictionary menjadi DataFrame
    df = pd.DataFrame(all_articles)
    return df

if __name__ == "__main__":
    # Pengujian mandiri Modul 1
    print("Mengambil berita terbaru dari RSS Feed...")
    news_df = fetch_news_feed(limit_per_source=3)
    
    print(f"\nBerhasil mengambil {len(news_df)} berita!\n")
    print(news_df[["source", "title", "published"]].to_string())
