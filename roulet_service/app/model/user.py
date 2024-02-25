from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    second_name: str
    dick_size: int
