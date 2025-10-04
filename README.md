# EuroRate Currency Bot

## ⚙️ Features (Currently only EUR-USD \ EUR-GBP) 
- ✅ Get real-time exchange rates (via [Frankfurter API](https://www.frankfurter.app/))  
- 🔎 Query rates on demand (`/rate EUR USD`)
- 📩 Subscribe to live currency exchange rate updates (e.g. EUR/USD, EUR/GBP)  
- ⚙️ Manage subscriptions (`/subscribe`, `/unsubscribe`, `/subscriptions`)  
- ⏰ Automatically receive daily updates at **9:00 AM** (configurable)  
---
## Usage  
### 💬 Bot commands:
| Command | Description |
|----------|-------------|
| `/start` | Initiation & Show help menu |
| `/rate EUR USD` | Get latest exchange rate |
| `/subscribe EUR USD` | Subscribe to updates |
| `/subscriptions` | List active subscriptions |
| `/unsubscribe EUR USD` | Remove subscription |
---
## Architecture
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-%2300C853.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot_API-0088CC?style=for-the-badge&logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- **FastAPI** – backend REST API for currency rates and subscriptions  
- **PostgreSQL** – stores subscriptions and exchange rate history  
- **Redis** – broker for Celery tasks  
- **Celery Worker** – fetches rates from [Frankfurter API](https://www.frankfurter.app/)  
- **Celery Beat** – schedules periodic jobs (fetch rates + notify subscribers)  
- **Telegram Bot** – user interface via chat commands  
- **Docker Compose** – orchestrates services  
```
User ↔ Telegram Bot ↔ FastAPI ↔ PostgreSQL
↕
Celery Worker + Beat ↔ Redis
```

---

## Local Development

### Prerequisites
- Docker & Docker Compose installed  
- Python 3.10+ (if running outside Docker)  
- A **Telegram bot token** (create via [@BotFather](https://t.me/BotFather))  

## ⚙️ Setup

Clone this repo:
```bash
git clone https://github.com/<your-username>/EuroRate-Currency-Bot.git
cd currency-subscription-bot
```

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

This will spin up:

- web (FastAPI app)
- db (Postgres database)
- redis (Celery broker)
- worker (Celery worker)
- beat (Celery scheduler)
- bot (Telegram bot)
