import os
import requests
from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import CurrencyRate, Subscription

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

celery = Celery("worker", broker=REDIS_URL, backend=REDIS_URL,include=["tasks.worker", "tasks.scheduler"])

API_URL = "https://api.frankfurter.app/latest"  # Frankfurter API endpoint


@celery.task
def fetch_rate(base="USD", target="EUR"):
    """Fetch a rate from Frankfurter and store it in DB."""
    db: Session = SessionLocal()
    try:
        # Add logging
        print(f"Fetching rate for {base}/{target}")
        
        response = requests.get(f"{API_URL}?from={base}&to={target}")
        response.raise_for_status()  # Raise exception for bad status codes

        data = response.json()
        # Check if the target currency is in the response
        if "rates" not in data or target not in data["rates"]:
            print(f"Rate not found in response: {data}")
            raise Exception(f"Rate for {base}/{target} not found in API response")

        rate = data["rates"][target]
        print(f"Got rate {rate} for {base}/{target}")

        new_rate = CurrencyRate(
            base_currency=base,
            target_currency=target,
            rate=rate,
        )
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)

        return {"base": base, "target": target, "rate": rate}
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise
    except Exception as e:
        print(f"Error fetching rate: {e}")
        raise
    finally:
        db.close()


@celery.task
    
def notify_subscribers():
    """Check subscriptions and push Telegram updates."""
    db: Session = SessionLocal()
    try:
        subs = db.query(Subscription).all()
        for sub in subs:
            # Get latest rate from DB
            rate_entry = (
                db.query(CurrencyRate)
                .filter(
                    CurrencyRate.base_currency == sub.base_currency,
                    CurrencyRate.target_currency == sub.target_currency,
                )
                .order_by(CurrencyRate.timestamp.desc())
                .first()
            )

            if not rate_entry:
                continue

            msg = f"📢 Update: 1 {sub.base_currency} = {rate_entry.rate} {sub.target_currency}"
            requests.post(TELEGRAM_API, data={"chat_id": sub.user_id, "text": msg})

        return f"Notified {len(subs)} subscribers"
    finally:
        db.close()


# Celery beat schedule
celery.conf.beat_schedule = {
    "fetch-eur-usd-every-minute": {
        "task": "tasks.worker.fetch_rate",
        "schedule": crontab(minute="*/1"),
        "args": ("EUR", "USD"),
    },
    "fetch-eur-gbp-every-minute": {
        "task": "tasks.worker.fetch_rate",
        "schedule": crontab(minute="*/1"),
        "args": ("EUR", "GBP"),
    },
    "notify-subscribers-every-minute": {
        "task": "tasks.worker.notify_subscribers",
        "schedule": crontab(minute="*/1"),
    },
}

