from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)