from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import User
from schemas import UserSchema

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_users(db: Session, skip: int = 0, limit: int = 100):

        return db.query(User).offset(skip).limit(limit).all()

    def create_user(db: Session, user: UserSchema):

        user = User(**user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

