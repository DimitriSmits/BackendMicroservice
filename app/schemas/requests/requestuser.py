from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from schemas import UserSchema

T = TypeVar('T')

class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)
