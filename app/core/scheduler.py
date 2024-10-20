from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends
from app.domain.services.automatic_purchase_service import AutomaticPurchaseService
from app.domain.services.category_service import CategoryService
from app.infrastructure.database.db import SessionLocal, get_db
from sqlalchemy.orm import Session

def reset_monthly_categories():
    db: Session = SessionLocal()
    try:
        category_service = CategoryService(db)
        category_service.reset_monthly_categories()
    finally:
        db.close()

def reset_weekly_categories():
    db: Session = SessionLocal()
    try:
        category_service = CategoryService(db)
        category_service.reset_weekly_categories()
    finally:
        db.close()

def process_scheduled_purchases(db: Session = Depends(get_db)):
    automatic_purchase_service = AutomaticPurchaseService(db)
    automatic_purchase_service.process_automatic_purchases()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_scheduled_purchases, 'interval', days=1)
    scheduler.add_job(reset_monthly_categories, 'cron', day=1, hour=0, minute=0)
    scheduler.add_job(reset_weekly_categories, 'cron', day_of_week='mon', hour=0, minute=0)
    scheduler.start()
    return scheduler
