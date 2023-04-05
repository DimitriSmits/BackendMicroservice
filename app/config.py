"""
This module contains functions for performing the configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/postgres'

# DATABASE_URL = os.environ['DATABASE_URL']

listen_addresses = '*'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
