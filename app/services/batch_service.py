from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import BatchSchema

from repositories import BatchRepository

class BatchService:

    def get_batches(db: Session, skip: int = 0, limit: int = 100):

        return BatchRepository.get_batches(db)

    def create_batch(db:Session, batch: BatchSchema):

        return BatchRepository.create_batch(db, batch)

