from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import EventSchema, EventRequest

from repositories import EventRepository

class EventService:

    def get_events(db: Session, skip: int = 0, limit: int = 100):

        return EventRepository.get_events(db)

    def create_event(db:Session, event: EventSchema):
        return EventRepository.create_event(db, event)
    
    def process_events(db:Session,event: List[EventSchema]):
        return EventRepository.process_events(db, event)
    
    def get_eventscount_by_name_and_organization(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
  
        testjelist = EventRepository.get_eventscount_by_name_and_organization(db, eventrequest)
        return testjelist
    
    def get_events_by_name_and_organization(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
  
        testjelist = EventRepository.get_events_by_name_and_organization(db, eventrequest)
        return testjelist
    
    def get_events_by_month(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
  
        testjelist = EventRepository.get_events_by_month(db, eventrequest)
        return testjelist