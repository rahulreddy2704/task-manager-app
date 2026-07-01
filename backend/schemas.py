"""
Pydantic schemas - define the shape of data going IN (requests) and
OUT (responses) of the API.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Shape of data required to create a task."""
    pass


class TaskUpdate(BaseModel):
    """Shape of data allowed when updating a task - all fields optional."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Shape of data returned to the client."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True