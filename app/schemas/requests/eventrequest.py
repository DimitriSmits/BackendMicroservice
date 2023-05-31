from typing import Optional, List, Dict, Any
from datetime import datetime
from schemas import CamelCasedSchema

class EventRequest(CamelCasedSchema):
    name: Optional[str] = None
    startdate: Optional[datetime] = None
    enddate: Optional[int] = None
    user_id: Optional[int] = None
    application_id: Optional[int] = None
    organization_id: Optional[int] = None

    class Config:
        orm_mode = True