from sqlalchemy.ext.asyncio import create_async_engine

import settings


async_engine = create_async_engine(settings.ASYNC_CONN_STRING)
