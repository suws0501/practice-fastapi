from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    completed: Optional[bool] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if values.title is None and values.completed is None:
            raise ValueError("At least one field must be provided")
        return values

class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

class TodoCreatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    completed: bool

class TodoUpdatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    completed: bool
    updated_at: datetime

