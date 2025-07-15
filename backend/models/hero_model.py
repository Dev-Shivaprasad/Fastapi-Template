from typing import Optional
from sqlmodel import SQLModel, Field, Integer


class hero(SQLModel, table=True):
    id: int | None = Field(default=None, sa_type=Integer, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


class addhero_create(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None


class addhero_update(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    
