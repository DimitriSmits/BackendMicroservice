from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import UserSchema

from repositories import UserRepository

class UserService:

    def get_users(db: Session, skip: int = 0, limit: int = 100):

        return UserRepository.get_users(db)

    def create_user(db:Session, user: UserSchema):

        return UserRepository.create_user(db, user)

