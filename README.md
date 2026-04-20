# StyleMirror

**MVP Core** — Stage 1

A Telegram bot that mimics the communication style of any specific person using Grok API.

![Status](https://img.shields.io/badge/Status-MVP_Core-brightgreen)

---

### About the Project

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

### Quick Start

#### 1. Clone the repository

```bash
git clone <your-repository-url>
cd style-mirror

#### 2. Create and activate virtual environment
```
