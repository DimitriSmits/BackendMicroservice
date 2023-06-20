from typing import List
from fastapi import HTTPException
from sqlalchemy import func, distinct
import json


from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Event
from schemas import EventSchema, EventRequest
from models import NameCountModel, EventCountModel
from fastapi import Response
from itertools import groupby
from dateutil.relativedelta import relativedelta


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
        #Method used for counting the events per month per organization
            
        query = db.query(Event.name).filter(
            Event.application_id == eventrequest.application_id,
            Event.created_date.between(eventrequest.startdate, eventrequest.enddate)
        )

        if eventrequest.organization_id != 0:
            query = query.filter(Event.organization_id == eventrequest.organization_id)

        names = query.distinct().all()
        specific_names = [name[0] for name in names]
        name_count_list = []

        try:
            for name in specific_names:
                count_query = db.query(func.count(Event.name)).filter(
                    Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
                    Event.name == name,
                    Event.application_id == eventrequest.application_id
                )

                if eventrequest.organization_id != 0:
                    count_query = count_query.filter(Event.organization_id == eventrequest.organization_id)

                count = count_query.scalar()
                name_count = NameCountModel(name=name, count=count)
                name_count_list.append(name_count)

        except Exception as e:
            # Handle any potential database errors
            print(f"Error: {str(e)}")

        return name_count_list

    def get_events_by_name_and_organization(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
        #Method used for getting the events by organization and application
        events = db.query(Event).filter(
            Event.name == eventrequest.name,
            Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
            Event.application_id == eventrequest.application_id
        )

        if eventrequest.organization_id != 0:
            events = events.filter(Event.organization_id == eventrequest.organization_id)

        events = events.all()

        return events
    def get_events_by_month(db: Session, eventrequest: EventRequest, skip: int = 0, limit: int = 100):
        #Method used for getting the events counts per month and returning into readable graph data
        
        start_date = datetime.strptime(eventrequest.startdate, '%Y-%m-%d')
        end_date = datetime.strptime(eventrequest.enddate, '%Y-%m-%d')

        # Generate a list of months between the start and end dates
        months = [start_date + relativedelta(months=i) for i in range((end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)]
        months = [month.strftime('%Y-%m') for month in months]

        # Get distinct event names from the database
        event_names = db.query(distinct(Event.name)).all()
        event_names = [name[0] for name in event_names]

        # Check for all orgs by month
        query = (
            db.query(Event.name, func.date_trunc('month', Event.created_date).label('month'), func.count())
            .filter(Event.created_date >= start_date, Event.created_date < end_date,
                    Event.application_id == eventrequest.application_id)
            .group_by(Event.name, 'month')
        )

        if eventrequest.organization_id != 0:
            query = query.filter(Event.organization_id == eventrequest.organization_id)

        # Create the final result list
        result_list = []
        for name in event_names:
            counts = [0] * len(months)
            for row in query.filter(Event.name == name):
                month_index = months.index(row.month.strftime('%Y-%m'))
                counts[month_index] = row[2]
            result_list.append({'name': name, 'data': counts})

        return result_list
    
    

        

