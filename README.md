# 📊 Currency Subscription Bot

A Telegram bot + FastAPI backend that lets users:

- 📩 Subscribe to live currency exchange rate updates (e.g. EUR/USD, EUR/GBP)  
- 🔎 Query rates on demand (`/rate EUR USD`)  
- ⚙️ Manage subscriptions (`/subscribe`, `/unsubscribe`, `/subscriptions`)  
- ⏰ Automatically receive daily updates at **9:00 AM** (configurable)  

The project is built using **FastAPI, Celery, Redis, PostgreSQL, and Docker**.

---

## ⚙️ Features

- ✅ Subscribe/unsubscribe to currency pairs  
- ✅ Get real-time exchange rates (via [Frankfurter API](https://www.frankfurter.app/))  
- ✅ Automatic daily updates via Celery Beat  
- ✅ Persistence with PostgreSQL  
- ✅ Redis as Celery broker  
- ✅ Fully containerized with Docker Compose  

---

## 🏗️ Architecture

- **FastAPI (web)** → Handles subscriptions & REST API  
- **Telegram Bot** → Interacts with users (`/subscribe`, `/rate`, etc.)  
- **Celery Worker** → Fetches currency rates and processes background jobs  
- **Celery Beat Scheduler** → Schedules periodic tasks (daily updates)  
- **PostgreSQL** → Stores user subscriptions & rates  
- **Redis** → Message broker for Celery  

User ↔ Telegram Bot ↔ FastAPI ↔ PostgreSQL
↕
Celery Worker + Beat ↔ Redis


---

## 🚀 Local Development

### Prerequisites
- Docker & Docker Compose installed  
- Python 3.10+ (if running outside Docker)  
- A **Telegram bot token** (create via [@BotFather](https://t.me/BotFather))  

### Setup

Clone this repo:
```bash
git clone https://github.com/<your-username>/EuroRate-Currency-Bot.git
cd currency-subscription-bot
```

## ⚙️ Setup

Create a `.env` file in the root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=currencydb
REDIS_URL=redis://redis:6379/0
```
start services
```bash
docker-compose up --build
```

## 📬 Deployment

🐳 **Containerized with Docker** → ready for **Fly.io**, **Railway**, **Render**, or **AWS ECS**

📦 **Use managed PostgreSQL/Redis** for production

---

## 🛠️ Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-%2300C853.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot_API-0088CC?style=for-the-badge&logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- **FastAPI** – Web framework  
- **Celery** – Task queue  
- **Redis** – Message broker  
- **PostgreSQL** – Database  
- **Docker Compose** – Service orchestration  
- **Telegram Bot API** – Messaging
