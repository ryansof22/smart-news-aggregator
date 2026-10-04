import streamlit as st
from rss_parser import fetch_news_feed

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

# Sidebar untuk Filter
st.sidebar.header("⚙️ Pengaturan Feed")

# Mengambil data RSS Feed (Menggunakan Cache agar hemat request)
@st.cache_data(ttl=600)  # Refresh otomatis setiap 10 menit
def load_data():
    return fetch_news_feed(limit_per_source=10)

with st.spinner("Mengambil berita terbaru..."):
    df_news = load_data()

if not df_news.empty:
    # Filter Sumber Berita di Sidebar
    sources = ["Semua Sumber"] + list(df_news["source"].unique())
    selected_source = st.sidebar.selectbox("Pilih Sumber Berita:", sources)

    # Filter Data berdasarkan Pilihan
    if selected_source != "Semua Sumber":
        filtered_df = df_news[df_news["source"] == selected_source]
    else:
        filtered_df = df_news

    # Tombol Refresh Manual
    if st.sidebar.button("🔄 Refresh Berita"):
        st.cache_data.clear()
        st.rerun()

    st.subheader(f"Berita Terbaru ({len(filtered_df)} Artikel)")

    # Tampilan Kartu Berita (Grid 2 Kolom)
    cols = st.columns(2)
    for idx, row in filtered_df.iterrows():
        col_idx = idx % 2
        with cols[col_idx]:
            with st.container(border=True):
                st.caption(f"📌 **{row['source']}** | 🕒 {row['published']}")
                st.markdown(f"### {row['title']}")
                
                # Tampilkan deskripsi singkat (jika ada)
                clean_summary = row['summary_raw'][:150] + "..." if len(row['summary_raw']) > 150 else row['summary_raw']
                st.write(clean_summary)

                # Tombol Aksi
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.link_button("🌐 Baca Asli", row['link'], use_container_width=True)
                with c2:
                    if st.button("🤖 Ringkas AI", key=f"btn_{idx}", use_container_width=True):
                        st.info("Fitur Ringkasan AI akan dihubungkan di Modul 3!")

else:
    st.warning("Gagal mengambil feed berita. Periksa koneksi internet Anda.")
