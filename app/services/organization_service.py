from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import OrganizationSchema

from repositories import OrganizationRepository

class OrganizationService:

    def get_organizations(db: Session, skip: int = 0, limit: int = 100):

        return OrganizationRepository.get_organizations(db)

    def create_organization(db:Session, organization: OrganizationSchema):

        return OrganizationRepository.create_organization(db, organization)

