from sqlalchemy import create_engine

import settings

engine = create_engine(settings.CONN_STRING)

