# StyleMirror

**MVP Core** — Stage 1

A Telegram bot that mimics the communication style of any specific person using Grok API.

![Status](https://img.shields.io/badge/Status-MVP_Core-brightgreen)

---

# About the Project

**StyleMirror** is an intelligent Telegram bot that learns and replicates the unique speaking style of a chosen person — including tone, slang, emoji usage, message length, humor, and phrasing.

At this MVP stage, the bot successfully receives messages from Telegram, processes them through a FastAPI backend, and generates responses using **Grok API** (xAI) while following a custom system prompt.

### Tech Stack (MVP Core)

- **Python 3.11+**
- **FastAPI** — Backend API
- **aiogram 3.x** — Async Telegram Bot
- **Grok API** (xAI) via OpenAI SDK
- **httpx** — Async HTTP client
- **python-dotenv** — Environment variables

### Project Architecture

Telegram User → aiogram Bot → FastAPI Backend → OpenAI API (xAI)

# Quick Start

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd style-mirror
```

## 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

```bash
cp .env.example .env
```

Fill in the .env file with your credentials:

TELEGRAM_BOT_TOKEN | OPENAI_API_KEY

## 5. Run the application

Open two terminals:

### Terminal 1 — FastAPI server:

```bash
uvicorn src.main:app --reload --port 8000
```

### Terminal 2 — Telegram Bot:

```bash
python -m src.bot.bot
```

### How to Use

1. Make sure both services are running.
2. Open Telegram and send any message to your bot.
3. The bot will reply in the style of the predefined person.
