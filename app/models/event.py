"""
This module contains functions for performing the eventmodel.
"""
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    json_data = Column(JSONB)
    created_date = Column(DateTime,default=datetime.datetime.now)

    batch_id = Column(Integer, ForeignKey("batch.id"))
    batch = relationship("Batch", back_populates="events")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="events")

    application_id = Column(Integer, ForeignKey("application.id"))
    application = relationship("Application", back_populates="events")

    organization_id = Column(Integer, ForeignKey("organization.id"))
    organization = relationship("Organization", back_populates="events")


