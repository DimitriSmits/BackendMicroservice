from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from schemas import OrganizationSchema

T = TypeVar('T')

class RequestOrganization(BaseModel):
    parameter: OrganizationSchema = Field(...)
