from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from schemas import EventSchema

T = TypeVar('T')

class RequestEvent(BaseModel):
    parameter: EventSchema = Field(...)
