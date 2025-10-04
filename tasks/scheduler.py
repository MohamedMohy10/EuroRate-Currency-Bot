import os
import requests
import logging
from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session
from app import database, models

# Celery config
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("scheduler", broker=REDIS_URL)

# Telegram API
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

API_BASE = "http://web:8000"

logging.basicConfig(level=logging.INFO)


@app.task
def send_daily_updates():
    """Fetch latest rates for all subscriptions and notify users."""
    db: Session = next(database.get_db())

    subs = db.query(models.Subscription).all()
    logging.info(f"Found {len(subs)} subscriptions to process.")

    for sub in subs:
        try:
            # Fetch latest rate from FastAPI service
            url = f"{API_BASE}/currency/{sub.base_currency}/{sub.target_currency}"
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                rate = data.get("rate")

                if rate:
                    message = f"Daily Update:\n1 {sub.base_currency} = {rate} {sub.target_currency}"
                    logging.info(f"Sending to {sub.user_id}: {message}")

                    # Send via Telegram API
                    tg_resp = requests.post(
                        TELEGRAM_API,
                        data={"chat_id": sub.user_id, "text": message},
                        timeout=10
                    )

                    if tg_resp.ok:
                        logging.info(f"Sent to {sub.user_id} | Telegram response: {tg_resp.json()}")
                    else:
                        logging.error(f"Telegram error for {sub.user_id}: {tg_resp.text}")
                else:
                    logging.warning(f"No rate found for {sub.base_currency}/{sub.target_currency}")
            else:
                logging.warning(f"Failed to fetch rate for {sub.base_currency}/{sub.target_currency}")
        except Exception as e:
            logging.error(f"Error processing subscription {sub.id}: {e}")


# Run every minute (for testing)
app.conf.beat_schedule = {
    "send-daily-updates-every-minute": {
        "task": "tasks.scheduler.send_daily_updates",
        "schedule": crontab(hour=9, minute=0),
    },
}

app.conf.timezone = "Europe/Vienna"
