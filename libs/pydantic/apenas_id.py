from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T_ID = TypeVar("T_ID")


class RetornoApenasId(BaseModel, Generic[T_ID]):
    id: T_ID


class RetornoDado(BaseModel, Generic[T_ID]):
    dado: T_ID
    hora: datetime = datetime.now()
