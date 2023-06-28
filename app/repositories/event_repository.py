"""
Repository for events

"""
from typing import List
from datetime import datetime
from sqlalchemy import func, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models import Event
from models import NameCountModel
from schemas import EventSchema, EventRequest
from dateutil.relativedelta import relativedelta
class EventRepository:
    """
    Repository for events

    """
    def __init__(self, database):
        """
        Initializes db

        """
        self.database = database
    @staticmethod
    def get_events(database: Session, skip: int = 0, limit: int = 100):
        """
        Gets all events

        """
        return database.query(Event).offset(skip).limit(limit).all()
    @staticmethod
    def create_event(database: Session, event: EventSchema):
        """
        Adds event db

        """
        _event = Event(**event.dict())
        database.add(_event)
        database.commit()
        database.refresh(_event)
        return _event
    @staticmethod
    def process_events(database:Session,event: List[EventSchema]):
        """
        Adds all events db

        """
        event_objects = [Event(**event.dict()) for event in event]
        database.add_all(event_objects)
        database.commit()
        return event_objects
    @staticmethod
    def get_eventscount_by_name_and_organization(database: Session, eventrequest: EventRequest):
        """
        Method used for counting the events per month per organization

        """
        query = database.query(Event.name).filter(
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
                count_query = database.query(func.count(Event.name)).filter(
                    Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
                    Event.name == name,
                    Event.application_id == eventrequest.application_id
                )

                if eventrequest.organization_id != 0:
                    count_query = count_query.filter(
                        Event.organization_id == eventrequest.organization_id)

                count = count_query.scalar()
                name_count = NameCountModel(name=name, count=count)
                name_count_list.append(name_count)
        except SQLAlchemyError as exception:
            # Handle specific database errors
            print(f"SQLAlchemy Error: {str(exception)}")
        except Exception as exception:
            # Handle any potential database errors
            print(f"Error: {str(exception)}")
        return name_count_list
    @staticmethod
    def get_events_by_name_and_organization(database: Session, eventrequest: EventRequest):
        """
        Method used for getting the events by organization and application

        """
        events = database.query(Event).filter(
            Event.name == eventrequest.name,
            Event.created_date.between(eventrequest.startdate, eventrequest.enddate),
            Event.application_id == eventrequest.application_id
        )

        if eventrequest.organization_id != 0:
            events = events.filter(Event.organization_id == eventrequest.organization_id)
        events = events.all()

        return events
    @staticmethod
    def get_events_by_month(database: Session, eventrequest: EventRequest):
        """
        Method used for getting the events counts per month and returning into readable graph data

        """
        start_date = datetime.strptime(eventrequest.startdate, '%Y-%m-%d')
        end_date = datetime.strptime(eventrequest.enddate, '%Y-%m-%d')

        # Generate a list of months between the start and end dates
        months = [start_date + relativedelta(months=i) for i in range
                  ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)]
        months = [month.strftime('%Y-%m') for month in months]

        # Get distinct event names from the database
        event_names = database.query(distinct(Event.name)).all()
        event_names = [name[0] for name in event_names]

        # Check for all orgs by month
        query = (
            database.query(Event.name, func.date_trunc
                           ('month', Event.created_date).label('month'), func.count())
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
