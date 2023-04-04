from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import ApplicationSchema

from repositories import ApplicationRepository

class ApplicationService:

    def get_applications(db: Session, skip: int = 0, limit: int = 100):

        return ApplicationRepository.get_applications(db)

    def create_application(db:Session, application: ApplicationSchema):

        return ApplicationRepository.create_application(db, application)

