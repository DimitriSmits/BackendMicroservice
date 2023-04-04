from typing import Dict, Optional

from schemas import CamelCasedSchema

class ApplicationSchema(CamelCasedSchema):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True