from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Event
from schemas import EventSchema

class EventRepository:
    def __init__(self, db):
        self.db = db

    def get_events(db: Session, skip: int = 0, limit: int = 100):

        return db.query(Event).offset(skip).limit(limit).all()

    def create_event(db: Session, event: EventSchema):

        _event = Event(**event.dict())
        db.add(_event)
        db.commit()
        db.refresh(_event)
        return _event

