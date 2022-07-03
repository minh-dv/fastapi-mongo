from beanie import Document
from uuid import UUID, uuid4
from pydantic import Field


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    password: str

    class Collection:
        name = "User"
