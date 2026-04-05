from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task

class TaskTagLink(SQLModel, table=True):
    task_id: int | None = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, min_length=1, max_length=50)
    color: str = Field(default="#6366f1")

    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTagLink
    )