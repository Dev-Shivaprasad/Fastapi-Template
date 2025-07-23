from typing import Optional
from sqlmodel import SQLModel, Field, Integer
from enum import Enum


class priority(Enum):
    Low = 0
    Medium = 1
    High = 2


class todostatus(Enum):
    Pending = 0
    PartiallyCompleted = 1
    Completed = 2


class todo(SQLModel, table=True):
    taskid: int | None = Field(default=None, sa_type=Integer, primary_key=True)
    task: str
    taskdescription: Optional[str]
    taskstatus: todostatus = Field(default=todostatus.Pending.value, sa_type=Integer)
    taskpriority: priority = Field(default=priority.Low.value, sa_type=Integer)


class todoDTO(SQLModel):
    taskid: int | None
    task: str
    taskdescription: Optional[str]
    taskstatus: str | None
    taskpriority: str | None
