from typing import List
from fastapi import HTTPException
from sqlalchemy import func


from sqlalchemy.orm import Session
from datetime import datetime
from models import Event
from schemas import EventSchema, EventRequest
from models import NameCountModel

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
    
    def process_events(db:Session,event: List[EventSchema]):
        event_objects = [Event(**event.dict()) for event in event]
        db.add_all(event_objects)
        db.commit()
        return event_objects
    
    def get_eventscount_by_name_and_organization(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
        print("Voorbereiden verzenden data")
        print(eventrequest.application_id)
        print(eventrequest.startdate)
        print(eventrequest.enddate)
        print(eventrequest.organization_id)
        
        names = db.query(Event.name).filter(
                                Event.application_id == 1,
                                Event.organization_id == eventrequest.organization_id,
                                Event.created_date >= eventrequest.startdate,
                                Event.created_date <= eventrequest.enddate,
                                Event.user_id == 1
                            ).distinct().all()
        specific_names = [name[0] for name in names]



        name_count_list = []  # List to store NameCountModel instances
        count = 0
        try:
            for name in specific_names:
                    count = db.query(func.count(Event.name)).filter(
                    Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
                    Event.name == name
                ).scalar()

                    name_count = NameCountModel(name=name, count=count)
                    name_count_list.append(name_count)
            
            
                
        except Exception as e:
            # Handle any potential database errors
            print(f"Error: {str(e)}")
        for test in name_count_list:
            print(test)
        print(count)
        return name_count_list
    def get_events_by_name_and_organization(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
        print("Voorbereiden verzenden data details")
        print(eventrequest.application_id)
        print(eventrequest.name)
        print(eventrequest.organization_id)
        
        events = db.query(Event.name).filter(
                                Event.application_id == 1,
                                Event.organization_id == eventrequest.organization_id,
                                Event.user_id == 1,
                                Event.name == eventrequest.name,
                            )
        print(events)



        # name_count_list = []  # List to store NameCountModel instances
        # count = 0
        # try:
        #     for name in specific_names:
        #             count = db.query(func.count(Event.name)).filter(
        #             Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
        #             Event.name == name
        #         ).scalar()

        #             name_count = NameCountModel(name=name, count=count)
        #             name_count_list.append(name_count)
            
            
                
        # except Exception as e:
        #     # Handle any potential database errors
        #     print(f"Error: {str(e)}")
        # for test in name_count_list:
        #     print(test)
        # print(count)
        return events
    
    

        

