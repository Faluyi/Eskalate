from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    object: Optional[T] = None
    errors: Optional[List[str]] = None
