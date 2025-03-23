# AI-Powered News Summarization & Company Insight System

This project is an end-to-end AI pipeline that scrapes the latest news from top global sources, generates summaries, and provides company-specific insights using NLP and embeddings.

---

## Features

**Scrapes News** from 6 popular websites (like BBC, Al Jazeera, Weird News, etc.) using **BeautifulSoup4** and **LangChain**.
**Embeddings** generated via `all-minilm:33m` model using **Ollama** for efficient semantic search.
Uses **ChromaDB** as vector storage for fast & accurate document retrieval.
Backend API built with **Flask** (`api.py`) to process POST requests and return AI-based insights.
Frontend built with **Streamlit** (`app.py`) for interactive UI.
**CloudGro API** is used to form output using structured prompts.
Supports company name input and returns relevant news-based analysis.

---

## How It Works

1. **News Scraping**  
   News articles are collected from selected websites via `BeautifulSoup` and LangChain web tools.

2. **Embedding Creation**  
   Articles are converted into vector embeddings using `all-minilm:33m` via **Ollama**, and stored in **ChromaDB**.

3. **API Interaction**  
   - Backend Flask API (`api.py`) exposes a `/get-summaries_of_article` POST endpoint.
   - You must run this first:  
     ```bash
     python api.py
     ```

4. **Streamlit Frontend**  
   The frontend (`app.py`) sends company names to the API and displays summary-based analysis.
   - Run Streamlit like this:  
     ```bash
     streamlit run app.py
     ```

---

## API Usage

- **Endpoint:** `http://127.0.0.1:5000/get-summaries_of_article`
- **Method:** `POST`
- **Request (JSON):**
```json
{
  "user_input": "Google"
}
