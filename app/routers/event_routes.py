"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestEvent
from services import EventService

event_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@event_router.post("/create")
async def create_event_service(request: RequestEvent, db: Session = Depends(get_db)):    
    EventService.create_event(db, event=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Event created successfully").dict(exclude_none=True)


@event_router.get("/")
async def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _events = EventService.get_events(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_events)


# @book_router.patch("/update")
# async def update_book(request: RequestBook, db: Session = Depends(get_db)):
#     _book = crud.update_book(db, book_id=request.parameter.id,
#                              title=request.parameter.title, description=request.parameter.description)
#     return Response(status="Ok", code="200", message="Success update data", result=_book)


# @book_router.delete("/delete")
# async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
#     crud.remove_book(db, book_id=request.parameter.id)
#     return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
