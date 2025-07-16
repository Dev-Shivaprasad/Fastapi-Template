from sqlmodel import SQLModel, Field

from pydantic import EmailStr
from uuid import uuid4, UUID


class user(SQLModel, table=True):
    userid: UUID | None = Field(primary_key=True, default_factory=uuid4)
    username: str
    emailid: EmailStr = Field(unique=True, nullable=False, max_length=255)
    password: str

class login(SQLModel):
    email: EmailStr
    password: str
