import streamlit as st
import os
from rss_parser import fetch_news_feed
from ai_summarizer import summarize_news_article

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Smart News Aggregator & AI Summarizer",
    page_icon="📰",
    layout="wide"
)

# Header Utama
st.title("📰 Smart News Aggregator")
st.caption("Agregator Berita Real-time & Ringkasan AI Single-Source")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Pengaturan Feed")

# Masukkan Gemini API Key di Sidebar jika belum ada di env
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password", help="Masukkan API Key Gemini Anda di sini jika belum diset di Environment Variable.")
if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

@st.cache_data(ttl=600)
def load_data():
    return fetch_news_feed(limit_per_source=10)

with st.spinner("Mengambil berita terbaru..."):
    df_news = load_data()

if not df_news.empty:
    sources = ["Semua Sumber"] + list(df_news["source"].unique())
    selected_source = st.sidebar.selectbox("Pilih Sumber Berita:", sources)

    if selected_source != "Semua Sumber":
        filtered_df = df_news[df_news["source"] == selected_source]
    else:
        filtered_df = df_news

    if st.sidebar.button("🔄 Refresh Berita"):
        st.cache_data.clear()
        st.rerun()

    st.subheader(f"Berita Terbaru ({len(filtered_df)} Artikel)")

    # Tampilkan Berita
    cols = st.columns(2)
    for idx, row in filtered_df.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            with st.container(border=True):
                st.caption(f"📌 **{row['source']}** | 🕒 {row['published']}")
                st.markdown(f"### {row['title']}")
                
                clean_summary = row['summary_raw'][:150] + "..." if len(row['summary_raw']) > 150 else row['summary_raw']
                st.write(clean_summary)

                c1, c2 = st.columns([1, 1])
                with c1:
                    st.link_button("🌐 Baca Asli", row['link'], use_container_width=True)
                with c2:
                    # Tombol Ringkas AI
                    if st.button("🤖 Ringkas AI", key=f"btn_{idx}", use_container_width=True):
                        with st.spinner("🤖 Gemini sedang menganalisis & meringkas artikel..."):
                            ai_summary = summarize_news_article(row['link'], row['summary_raw'])
                            st.markdown("---")
                            st.markdown("#### 📝 Ringkasan AI Single-Source:")
                            st.info(ai_summary)

else:
    st.warning("Gagal mengambil feed berita. Periksa koneksi internet Anda.")
