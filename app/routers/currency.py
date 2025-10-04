from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import SessionLocal
from app import models, schemas
from tasks.worker import fetch_rate

# Add logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["Currency"])

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CurrencyRateResponse)
def create_currency_rate(rate: schemas.CurrencyRateCreate, db: Session = Depends(get_db)):
    db_rate = models.CurrencyRate(
        base_currency=rate.base_currency,
        target_currency=rate.target_currency,
        rate=rate.rate,
    )
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

@router.get("/{base}/{target}", response_model=schemas.CurrencyRateResponse)
def get_currency_rate(base: str, target: str, db: Session = Depends(get_db)):
    base = base.upper()
    target = target.upper()
    
    rate = db.query(models.CurrencyRate).filter(
        models.CurrencyRate.base_currency == base,
        models.CurrencyRate.target_currency == target
    ).order_by(models.CurrencyRate.timestamp.desc()).first()
    
    if not rate:
        logger.warning(f"Rate not found for {base}/{target}, triggering fetch")
        # Trigger a fetch when rate is not found
        try:
            fetch_rate.delay(base, target)
        except Exception as e:
            logger.error(f"Failed to trigger rate fetch: {e}")
        raise HTTPException(status_code=404, detail="Rate not found")
    
    logger.info(f"Found rate for {base}/{target}: {rate.rate}")
    return rate

@router.post("/fetch/{base}/{target}")
def trigger_fetch(base: str, target: str):
    task = fetch_rate.delay(base, target)
    return {"task_id": task.id, "status": "queued"}
