from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from models import Application
from schemas import ApplicationSchema

class ApplicationRepository:
    def __init__(self, db):
        self.db = db

    def get_applications(db: Session, skip: int = 0, limit: int = 100):
        
        return db.query(Application).offset(skip).limit(limit).all()

    def create_application(db: Session, application: ApplicationSchema):

        application_data = application.dict()
        _application = Application(**application_data)
        db.add(_application)
        db.commit()
        db.refresh(_application)
        return _application

