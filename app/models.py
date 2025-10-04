from sqlalchemy import Column, Integer, String, Float, DateTime, func, UniqueConstraint
from app.database import Base
from datetime import datetime

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String, index=True)
    target_currency = Column(String, index=True)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    base_currency = Column(String, index=True)
    target_currency = Column(String, index=True)

    # Ensure no duplicates (user_id + base + target must be unique)
    __table_args__ = (
        UniqueConstraint("user_id", "base_currency", "target_currency", name="uq_user_subscription"),
    )
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True, nullable=False)  # store as string for safety
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("chat_id", name="uq_user_chat_id"),
    )