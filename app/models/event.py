"""
This module contains functions for performing the eventmodel.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    json_data = Column(JSONB)
    description = Column(String)

    batch_id = Column(Integer, ForeignKey("batch.id"))
    batch = relationship("Batch", back_populates="events")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="events")

    application_id = Column(Integer, ForeignKey("application.id"))
    application = relationship("Application", back_populates="events")
