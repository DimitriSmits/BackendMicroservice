"""
This module contains functions for performing the main app.

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from routers import application_router
from routers import batch_router
from routers import organization_router
from routers import event_router
from routers import user_router
from database import engine
from database import Base
from services import SQSConsumer
from services import SQSEventConsumer
from exceptions import InvalidQueueUrlError
from services import EventService
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    os.getenv('POWERSUITE_URL'),  # Replace with the URL of your Vue.js application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(application_router, prefix="/application", tags=["application"])
app.include_router(batch_router, prefix="/batch", tags=["batch"])
app.include_router(organization_router, prefix="/organization", tags=["organization"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(event_router, prefix="/event", tags=["event"])

#Start consuming messages from the message queue

try:

    consumer = SQSConsumer()
    asyncio.create_task(consumer.run())
    eventconsumer = SQSEventConsumer()
    asyncio.create_task(eventconsumer.run())
except InvalidQueueUrlError as e:
    # Return error response indicating that the queue URL is invalid
    print(str(e))
