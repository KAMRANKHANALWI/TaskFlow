from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project
    from app.models.tag import Tag

from app.models.tag import TaskTagLink  # ← real import, not TYPE_CHECKING

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="")
    status: str = Field(default="todo")
    priority: str = Field(default="medium")
    project_id: int = Field(foreign_key="project.id")
    assignee_id: int | None = Field(default=None, foreign_key="user.id")
    due_date: datetime | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # relationships
    project: "Project" = Relationship(back_populates="tasks")
    assignee: "User" = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTagLink  # ← actual class, not a string
    )