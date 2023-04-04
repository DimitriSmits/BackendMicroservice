from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Organization
from schemas import OrganizationSchema

class OrganizationRepository:
    def __init__(self, db):
        self.db = db

    def get_organizations(db: Session, skip: int = 0, limit: int = 100):

        return db.query(Organization).offset(skip).limit(limit).all()

    def create_organization(db: Session, organization: OrganizationSchema):

        _organization = Organization(**organization.dict())
        db.add(_organization)
        db.commit()
        db.refresh(_organization)
        return _organization

