from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, database
from app.database import engine, init_db
from app.routers import currency

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(currency.router)

@app.get("/")
def root():
    return {"message": "Currency Bot API is running 🚀"}

@app.on_event("startup")
def on_startup():
    init_db()

# Subscribe endpoint
@app.post("/subscribe")
def subscribe(user_id: str, base: str, target: str, db: Session = Depends(database.get_db)):
    base = base.upper()
    target = target.upper()

    # Check if already exists
    existing = db.query(models.Subscription).filter_by(
        user_id=user_id,
        base_currency=base,
        target_currency=target
    ).first()

    if existing:
        return {"message": f"Already subscribed to {base}/{target}"}

    sub = models.Subscription(
        user_id=user_id,
        base_currency=base,
        target_currency=target,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return {
        "message": "Subscribed!",
        "subscription": {
            "id": sub.id,
            "user_id": sub.user_id,
            "base": sub.base_currency,
            "target": sub.target_currency,
        },
    }


@app.delete("/unsubscribe")
def unsubscribe(user_id: str, base: str, target: str, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subscription).filter_by(
        user_id=user_id,
        base_currency=base.upper(),
        target_currency=target.upper()
    ).first()

    if not sub:
        return {"message": "Subscription not found"}

    db.delete(sub)
    db.commit()
    return {"message": f"Unsubscribed from {base.upper()}/{target.upper()}"}

# List subscriptions
@app.get("/subscriptions/{user_id}")
def get_subscriptions(user_id: str, db: Session = Depends(database.get_db)):
    subs = (
        db.query(models.Subscription)
        .filter(models.Subscription.user_id == user_id)
        .all()
    )
    return {
        "subscriptions": [
            {
                "id": s.id,
                "user_id": s.user_id,
                "base": s.base_currency,
                "target": s.target_currency,
            }
            for s in subs
        ]
    }

@app.post("/register_user")
def register_user(chat_id: str, username: str | None = None, first_name: str | None = None,last_name: str | None = None, db: Session = Depends(database.get_db)):
    """
    Upsert a user by chat_id. Bot will call this on /start.
    """
    existing = db.query(models.User).filter(models.User.chat_id == str(chat_id)).first()
    if existing:
        # update metadata if changed
        existing.username = username or existing.username
        existing.first_name = first_name or existing.first_name
        existing.last_name = last_name or existing.last_name
        db.commit()
        db.refresh(existing)
        return {"message": "User updated", "user": {"chat_id": existing.chat_id}}
    user = models.User(
        chat_id=str(chat_id),
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user": {"chat_id": user.chat_id}}