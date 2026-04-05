from pydantic import BaseModel
from datetime import datetime
from app.schemas.tag import TagOut

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: str = "todo"
    priority: str = "medium"
    project_id: int
    assignee_id: int | None = None
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    project_id: int
    assignee_id: int | None
    due_date: datetime | None
    created_at: datetime
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}