"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestApplication
from services import ApplicationService
application_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application_router.post("/create")
async def create_application_service(request: RequestApplication, db: Session = Depends(get_db)):    
    ApplicationService.create_application(db, application=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Application created successfully").dict(exclude_none=True)


@application_router.get("/")
async def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _applications = ApplicationService.get_applications(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_applications)


# @book_router.patch("/update")
# async def update_book(request: RequestBook, db: Session = Depends(get_db)):
#     _book = crud.update_book(db, book_id=request.parameter.id,
#                              title=request.parameter.title, description=request.parameter.description)
#     return Response(status="Ok", code="200", message="Success update data", result=_book)


# @book_router.delete("/delete")
# async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
#     crud.remove_book(db, book_id=request.parameter.id)
#     return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
