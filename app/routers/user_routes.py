"""
This module contains functions for performing the routes.
"""


from fastapi import APIRouter,Path
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas import Response, RequestUser
from route_dependencies import get_db
from services import UserService

user_router = APIRouter()

@user_router.post("/create")
async def create_user_service(request: RequestUser, db: Session = Depends(get_db)):    
    UserService.create_user(db, user=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="User created successfully").dict(exclude_none=True)


@user_router.get("/")
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _users = UserService.get_users(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_users)


# @book_router.patch("/update")
# async def update_book(request: RequestBook, db: Session = Depends(get_db)):
#     _book = crud.update_book(db, book_id=request.parameter.id,
#                              title=request.parameter.title, description=request.parameter.description)
#     return Response(status="Ok", code="200", message="Success update data", result=_book)


# @book_router.delete("/delete")
# async def delete_book(request: RequestBook,  db: Session = Depends(get_db)):
#     crud.remove_book(db, book_id=request.parameter.id)
#     return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
