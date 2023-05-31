"""
This module contains functions for performing the organizationmodel.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="organization")
    events = relationship("Event", back_populates="organization")
