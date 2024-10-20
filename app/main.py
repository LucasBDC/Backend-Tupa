from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import automatic_purchase, debt, subscription, user, purchase, category, installment, auth
from app.core.scheduler import start_scheduler
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    try:
        yield
    finally:
        logging.info("Shutting down scheduler...")
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router, tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(purchase.router, tags=["Purchases"])
app.include_router(category.router, tags=["Categories"])
app.include_router(installment.router, tags=["Installments"])
app.include_router(debt.router, tags=["Debt"])
app.include_router(automatic_purchase.router, tags=["Automatic Purchases"])
app.include_router(subscription.router, tags=["Subscription"])
