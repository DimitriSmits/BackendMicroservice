from typing import Dict, Optional
from datetime import datetime
from schemas import CamelCasedSchema

class UserSchema(CamelCasedSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None

    class Config:
        orm_mode = True