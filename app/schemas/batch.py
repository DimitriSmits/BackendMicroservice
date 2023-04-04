from typing import Dict, Optional
from datetime import datetime
from schemas import CamelCasedSchema

class BatchSchema(CamelCasedSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    created_date: Optional[datetime] = None

    class Config:
        orm_mode = True