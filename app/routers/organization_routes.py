"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestOrganization
from services import OrganizationService

organization_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@organization_router.post("/create")
async def create_organization_service(request: RequestOrganization, db: Session = Depends(get_db)):    
    OrganizationService.create_organization(db, organization=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Organization created successfully").dict(exclude_none=True)


@organization_router.get("/")
async def get_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _organizations = OrganizationService.get_organizations(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_organizations)


# @book_router.patch("/update")
# async def update_book(request: RequestBook, db: Session = Depends(get_db)):
#     _book = crud.update_book(db, book_id=request.parameter.id,
#                              title=request.parameter.title, description=request.parameter.description)
#     return Response(status="Ok", code="200", message="Success update data", result=_book)


# @book_router.delete("/delete")
# async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
#     crud.remove_book(db, book_id=request.parameter.id)
#     return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
