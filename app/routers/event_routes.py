"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session
from schemas import Response, RequestEvent, EventSchema
from schemas import EventRequest
from route_dependencies import get_db
from services import EventService
from typing import Optional

event_router = APIRouter()

@event_router.post("/create")
async def create_event_service(request: RequestEvent, db: Session = Depends(get_db)):    
    print("TEST REQUEST")
    print(request.parameter)
    EventService.create_event(db, event=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Event created successfully").dict(exclude_none=True)


@event_router.get("/")
async def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _events = EventService.get_events(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_events)

@event_router.get("/namecountlist")
async def get_events_namecountlist(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    organization: Optional[int] = Query(None),
    startdate: Optional[str] = Query(None),
    enddate: Optional[str] = Query(None),
    application: Optional[int] = Query(None),
):
    
    event_request = EventRequest()
    event_request.application_id = application
    #User_ID used for organization_id, change later
    event_request.user_id = 1
    event_request.organization_id = organization
    event_request.startdate = startdate
    event_request.enddate = enddate

    namecountlist = EventService.get_eventscount_by_name_and_organization(db, event_request, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=namecountlist)

@event_router.get("/namecountlistt")
async def get_events_namecountlist(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    organization: Optional[int] = Query(None),
    startdate: Optional[str] = Query(None),
    enddate: Optional[str] = Query(None),
    application: Optional[int] = Query(None),
):
    
    event_request = EventRequest()
    event_request.application_id = application
    #User_ID used for organization_id, change later
    event_request.user_id = 1
    event_request.organization_id = organization
    event_request.startdate = startdate
    event_request.enddate = enddate

    namecountlist = EventService.get_eventscount_by_name_and_organization(db, event_request, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=namecountlist)

@event_router.get("/eventsdetails")
async def get_events_eventsdetails(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None),
    organization: Optional[int] = Query(None),
    application: Optional[int] = Query(None),
):
    print("JAJAJAJA") 
    event_request = EventRequest()
    event_request.application_id = application
    #User_ID used for organization_id, change later
    event_request.user_id = 1
    event_request.organization_id = organization
    event_request.name = name

    namecountlist = EventService.get_eventscount_by_name_and_organization(db, event_request, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=namecountlist)
