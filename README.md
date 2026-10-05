# 📰 Smart News Aggregator & Single-Source AI Summarizer

A Streamlit-based web application that aggregates real-time news feeds from major Indonesian news portals and provides single-source AI-powered summaries using the Google Gemini API.

## 🌟 Key Features
- **Real-Time News Aggregation**: Pulls updated news feeds from multiple sources (Antara News, Republika, CNN Indonesia, CNBC Indonesia) via RSS feeds.
- **Chronological & Categorized View**: Displays clean news cards with filters by source.
- **Single-Source AI Summarization**: Uses Gemini 2.5 Flash to generate concise key takeaways exclusively from the selected article, preventing cross-source hallucination.
- **Direct Source Links**: Includes quick navigation buttons to original full articles.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Frontend / Framework**: Streamlit
- **Data Ingestion**: Feedparser, BeautifulSoup4, Requests
- **Data Manipulation**: Pandas
- **AI Integration**: Google GenAI SDK (Gemini 2.5 Flash Model)

## 🚀 How to Run Locally

Try In Streamlit : https://smart-news-aggregator.streamlit.app/

