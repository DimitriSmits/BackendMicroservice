"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestBatch
from services import BatchService

batch_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@batch_router.post("/create")
async def create_batch_service(request: RequestBatch, db: Session = Depends(get_db)):    
    BatchService.create_batch(db, batch=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Batch created successfully").dict(exclude_none=True)


@batch_router.get("/")
async def get_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _batches = BatchService.get_batches(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_batches)


# @book_router.patch("/update")
# async def update_book(request: RequestBook, db: Session = Depends(get_db)):
#     _book = crud.update_book(db, book_id=request.parameter.id,
#                              title=request.parameter.title, description=request.parameter.description)
#     return Response(status="Ok", code="200", message="Success update data", result=_book)


# @book_router.delete("/delete")
# async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
#     crud.remove_book(db, book_id=request.parameter.id)
#     return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
