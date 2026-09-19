# 🪶 Nocturne URL Shortener

> A lightweight, lightning-fast micro URL shortener and click analytics tracker built with **FastAPI**, **SQLite**, and **Pydantic**. Engineered for simplicity, precision, and ease of deployment.

---

## ⚡ Features

- **High-Performance Routing:** Built on FastAPI with asynchronous routing capabilities.
- **Persistent Storage:** Lightweight SQLite backend with automated schema initialization.
- **Real-Time Click Analytics:** Tracks cumulative visits for every generated short code dynamically.
- **Bulletproof Testing Suite:** Ships with a `pytest` suite achieving **95% code coverage**.

---

## 🛠️ Tech Stack

- **Python 3.14+**
- **FastAPI** & **Uvicorn**
- **SQLite3** (Built-in standard library)
- **Pydantic v2**
- **Pytest** & **HTTPX**

---

## 📂 Project Structure

```text
PythonProject1/
├── .venv/
├── app/
│   ├── __init__.py
│   ├── crud.py         # Database queries & core logic
│   ├── database.py     # SQLite connection & lifecycle management
│   ├── main.py         # FastAPI application endpoints
│   ├── schemas.py      # Pydantic data validation models
│   └── url_shortner.db # SQLite database file
├── .coverage           # Pytest code coverage report cache
├── ReadMe.md           # Project documentation
├── test_app.py         # Comprehensive pytest suite
└── url_shortner.db     # Root-level database reference