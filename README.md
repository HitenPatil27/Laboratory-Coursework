# AI Agents & Apps with Groq API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Groq API](https://img.shields.io/badge/Groq-API-orange)](https://console.groq.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-green)](https://streamlit.io/)

## Overview

This repository showcases a collection of Python-based AI agents and web applications built using the **Groq API** for fast, efficient LLM inference. The projects demonstrate practical use cases like retrieval-augmented generation (RAG), appointment scheduling, product information retrieval, web search integration, and LLM prompt engineering comparisons.

Key themes:
- **Rapid prototyping** with Groq's high-speed models (e.g., Llama 3, GPT-OSS-20B).
- **Streamlit** for interactive UIs.
- **Modular agents** for tasks like search, data extraction, and scheduling.
- **Integration** with tools like Sentence Transformers, SerpAPI, and PyPDF2.

**Note on API Keys**: API keys are hardcoded in the scripts for demo purposes (e.g., Groq and SerpAPI). In production, use environment variables (e.g., `os.environ["GROQ_API_KEY"]`) and never commit them to Git. Obtain your free Groq API key from [console.groq.com](https://console.groq.com/keys).

## Features

- **PDF RAG**: Upload and query PDFs with semantic search and Groq-powered responses.
- **Appointment Scheduler**: Interactive booking app with AI confirmation.
- **Product Info Agent**: JSON-structured product details from natural language queries.
- **Web Search Agent**: Real-time search with SerpAPI and Groq summarization.
- **LLM Prompt Comparator**: Side-by-side comparison of prompts with/without system instructions.

## Prerequisites

- Python 3.8+
- Git (to clone the repo)

Install dependencies via pip (run in a virtual environment):

# Projects

## 1. PDF RAG Application (RAG.py)

A Flask-based web app for Retrieval-Augmented Generation (RAG) on PDFs. Extracts text, chunks it, embeds with Sentence Transformers, retrieves relevant chunks via cosine similarity, and generates answers using Groq's Llama 3 model.

### Setup & Run

* Ensure Flask and dependencies are installed.
* Run: `python RAG.py`
* Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
* Upload a PDF via `/upload`, then query it via `/query` (POST JSON with `{"query": "your question"}`).

### Features

* Text extraction and chunking (500-word chunks).
* Semantic retrieval (top-3 matches).
* Groq-powered response generation.
* Logging for debugging.

### Example Usage

* Upload: `curl -F "pdf=@your_file.pdf" http://127.0.0.1:5000/upload`
* Query: `curl -X POST -H "Content-Type: application/json" -d '{"query": "What is the main topic?"}' http://127.0.0.1:5000/query`

---

## 2. AI Appointment Scheduler (Booking_Agent.py)

A Streamlit app for booking appointments with AI confirmation. Users input details, and Groq generates a professional summary/email-style response.

### Setup & Run

* Install Streamlit: `pip install streamlit groq`.
* Run: `streamlit run Booking_Agent.py`
* Open the provided local URL.

### Features

* Dark-themed UI with input fields (name, email, date, time, type, notes).
* Groq integration for natural language confirmation.
* Expandable summary section.
* Responsive design for mobile/desktop.

### Example

Enter details and click "Confirm Booking" to see AI-generated confirmation like: `Your consultation is booked for John Doe on 2025-10-16 at 2:00 PM.`

---

## 3. Product Info Agent (1_Agent.py)

A simple console script that queries Groq for product details (e.g., iPhone 15) and returns structured JSON (name, price, availability, rating).

### Setup & Run

* Install: `pip install groq`.
* Run: `python 1_Agent.py`
* Modify the `get_product_info()` call for other products.

### Features

* JSON output for easy parsing/integration.
* Low-temperature generation for factual responses.
* Error handling for JSON parsing.

### Example Output

```json
{
  "product_name": "iPhone 15",
  "price": "$799",
  "availability": "In stock",
  "rating": "4.8/5"
}
```

---

## 4. Web Search Agent (3_WebSearch_Agent.py)

A console-based agent that performs Google searches via SerpAPI, summarizes top results, and generates insightful responses with Groq.

### Setup & Run

* Install: `pip install groq google-search-results` (SerpAPI wrapper).
* Set `serpapi_key` in the script (or environment variable).
* Run: `python 3_WebSearch_Agent.py`
* Enter a query when prompted (e.g., "latest AI news").

### Features

* Top-5 search snippets for context.
* Concise Groq responses with citations.
* Handles unrelated results gracefully.

### Example

Query: `Groq API updates` → Response: `Recent updates include faster inference speeds...`

---

## 5. LLM Prompt Comparator (2_Task.py)

A Streamlit app comparing LLM outputs: one with just a user prompt, another with a system + user prompt. Highlights how system prompts improve structure and accuracy.

### Setup & Run

* Install: `pip install streamlit groq`.
* Run: `streamlit run 2_Task.py`
* Enter a prompt (e.g., "Explain SIP vs mutual funds") and click "Run Comparison".

### Features

* Side-by-side text areas for responses.
* Uses GPT-OSS-20B model.
* Educational tool for prompt engineering.

### Example

* Without System: Casual explanation.
* With System: Structured bullet points as an "expert."

---

## Contributing

* Fork the repo.
* Create a feature branch: `git checkout -b feature/amazing-agent`.
* Commit changes: `git commit -m 'Add new agent'`.
* Push: `git push origin feature/amazing-agent`.
* Open a Pull Request.

## Security & Best Practices

* **API Keys:** Replace hardcoded keys with dotenv or environment variables.
* **Rate Limits:** Groq has usage quotas; monitor via their dashboard.
* **Dependencies:** Pin versions in `requirements.txt` for reproducibility.
* **Testing:** Add unit tests for agents (e.g., with `pytest`).
