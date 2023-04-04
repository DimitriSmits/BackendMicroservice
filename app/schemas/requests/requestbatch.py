from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from schemas import BatchSchema

T = TypeVar('T')

class RequestBatch(BaseModel):
    parameter: BatchSchema = Field(...)
