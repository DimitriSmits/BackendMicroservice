"""
This module contains functions for performing the applicationmodel.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Application(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    events = relationship("Event", back_populates="application")
