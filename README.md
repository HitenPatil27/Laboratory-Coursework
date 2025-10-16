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

```bash
pip install flask PyPDF2 sentence-transformers numpy scikit-learn groq streamlit serpapi datetime json
