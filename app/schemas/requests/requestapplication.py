from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from schemas import ApplicationSchema

T = TypeVar('T')

class RequestApplication(BaseModel):
    parameter: ApplicationSchema = Field(...)
