from sqlmodel import SQLModel, Field, Column, String

from pydantic import EmailStr
from uuid import uuid4, UUID


class user(SQLModel, table=True):
    UserId: UUID | None = Field(primary_key=True, default_factory=uuid4)
    UserName: str
    EmailId: EmailStr = Field(
        sa_column=Column("EmailId", type_=String(255), unique=True, nullable=False)
    )
    Password: str


class login(SQLModel):
    Email: EmailStr
    Password: str
