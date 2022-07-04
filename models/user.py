from beanie import Document
from uuid import UUID, uuid4
from pydantic import Field
from typing import Optional


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    password: str
    reset_code: Optional[str]

    class Collection:
        name = "User"
