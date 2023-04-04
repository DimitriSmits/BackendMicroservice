from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from datetime import datetime
from models import Batch
from schemas import BatchSchema

class BatchRepository:
    def __init__(self, db):
        self.db = db

    def get_batches(db: Session, skip: int = 0, limit: int = 100):

        return db.query(Batch).offset(skip).limit(limit).all()

    def create_batch(db: Session, batch: BatchSchema):

        _batch = Batch(**batch.dict())
        db.add(_batch)
        db.commit()
        db.refresh(_batch)
        return _batch

