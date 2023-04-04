"""
This module contains functions for performing the batchmodel.
"""

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Batch(Base):
    __tablename__ = 'batch'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_date = Column(DateTime,default=datetime.datetime.now)
    events = relationship("Event", back_populates="batch")
