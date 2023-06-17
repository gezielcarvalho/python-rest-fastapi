from typing import Optional
from pydantic import BaseModel
from uuid import UUID, uuid4


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    fullname: str
    username: str
    email: str
    password: str
    address: str
