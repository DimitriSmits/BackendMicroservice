"""
This module contains functions for performing the main app.

"""
from fastapi import FastAPI
import models
from routers import application_router
from routers import batch_router
from routers import organization_router
from routers import event_router
from routers import user_router
from database import engine
from database import Base
from services import SQSConsumer
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(application_router, prefix="/application", tags=["application"])
app.include_router(batch_router, prefix="/batch", tags=["batch"])
app.include_router(organization_router, prefix="/organization", tags=["organization"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(event_router, prefix="/event", tags=["event"])


consumer = SQSConsumer(
    queue_url="http://localhost:4566/000000000000/my-queue",
)
asyncio.create_task(consumer.run())


