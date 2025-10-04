📊 Currency Subscription Bot

A Telegram bot + FastAPI backend that lets users:

Subscribe to live currency exchange rate updates (e.g. EUR/USD, EUR/GBP).

Query rates on demand (/rate EUR USD).

Manage subscriptions (/subscribe, /unsubscribe, /list).

Automatically receive daily updates at 9:00 AM (configurable).

The project is built using FastAPI, Celery, Redis, PostgreSQL, and Docker.

⚙️ Features

✅ Subscribe/unsubscribe to currency pairs
✅ Get real-time exchange rates (via Frankfurter API
)
✅ Automatic daily updates via Celery Beat
✅ Persistence with PostgreSQL
✅ Redis as Celery broker
✅ Fully containerized with Docker Compose

🏗️ Architecture

FastAPI (web) → Handles subscriptions & REST API

Telegram Bot → Interacts with users (/subscribe, /rate, etc.)

Celery Worker → Fetches currency rates and processes background jobs

Celery Beat Scheduler → Schedules periodic tasks (daily updates)

PostgreSQL → Stores user subscriptions & rates

Redis → Message broker for Celery

User ↔ Telegram Bot ↔ FastAPI ↔ PostgreSQL
                          ↕
                   Celery Worker + Beat ↔ Redis

🚀 Local Development
Prerequisites

Docker & Docker Compose installed

Python 3.10+ (if running outside Docker)

A Telegram bot token (create via @BotFather)

Setup

Clone this repo:

git clone https://github.com/<your-username>/currency-subscription-bot.git
cd currency-subscription-bot


Create a .env file:

TELEGRAM_BOT_TOKEN=your_bot_token_here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=currencydb
REDIS_URL=redis://redis:6379/0


Start services:

docker-compose up --build


Interact with the bot in Telegram:

/subscribe EUR USD

/rate EUR GBP

/list

📬 Deployment

Containerized with Docker → ready for Fly.io, Railway, or AWS ECS

Managed DB/Redis recommended for production

Secrets handled via provider’s environment variables

📌 Roadmap

 Basic bot commands

 Subscription management

 Scheduled daily updates

 Cloud deployment (next step 🚀)

 User timezones for updates

🛠️ Tech Stack

FastAPI – Web framework

Celery – Task queue

Redis – Message broker

PostgreSQL – Database

Docker Compose – Orchestration

Telegram Bot API – Messaging

📜 License

MIT License.