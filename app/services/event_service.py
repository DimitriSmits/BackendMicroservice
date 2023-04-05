from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import EventSchema

from repositories import EventRepository

class EventService:

    def get_events(db: Session, skip: int = 0, limit: int = 100):

        return EventRepository.get_events(db)

    def create_event(db:Session, event: EventSchema):
        return EventRepository.create_event(db, event)

