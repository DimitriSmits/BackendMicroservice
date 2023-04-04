"""
This module contains functions for performing the usermodel.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ ="user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    organization_id = Column(Integer, ForeignKey("organization.id"))
    organization = relationship("Organization", back_populates="users")
    events = relationship("Event", back_populates="user")
