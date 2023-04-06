import database


def get_db():
    db = database.get_session()()
    try:
        yield db
    finally:
        db.close()
