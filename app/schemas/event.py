from typing import Optional, List, Dict, Any
from datetime import datetime
from schemas import CamelCasedSchema

class EventSchema(CamelCasedSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    json_data: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    batch_id: Optional[int] = None
    user_id: Optional[int] = None
    application_id: Optional[int] = None

    class Config:
        orm_mode = True