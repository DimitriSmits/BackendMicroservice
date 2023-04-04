from sqlalchemy.orm import sessionmaker

from database import engine


def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
