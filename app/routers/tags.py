from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.dependencies import get_session, get_current_user
from app.models.tag import Tag
from app.models.task import Task
from app.schemas.tag import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["tags"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[TagOut])
def list_tags(session: Session = Depends(get_session)):
    return session.exec(select(Tag)).all()


@router.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    session: Session = Depends(get_session)
):
    # check duplicate name
    existing = session.exec(select(Tag).where(Tag.name == data.name)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tag '{data.name}' already exists"
        )
    tag = Tag(**data.model_dump())
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.post("/{tag_id}/tasks/{task_id}", response_model=TagOut)
def assign_tag_to_task(
    tag_id: int,
    task_id: int,
    session: Session = Depends(get_session)
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag {tag_id} not found")

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, f"Task {task_id} not found")

    # M:N — add task to tag's task list
    if task not in tag.tasks:
        tag.tasks.append(task)
        session.add(tag)
        session.commit()
        session.refresh(tag)

    return tag


@router.delete("/{tag_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag_from_task(
    tag_id: int,
    task_id: int,
    session: Session = Depends(get_session)
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag {tag_id} not found")

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, f"Task {task_id} not found")

    if task in tag.tasks:
        tag.tasks.remove(task)
        session.add(tag)
        session.commit()


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    session: Session = Depends(get_session)
):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, f"Tag {tag_id} not found")
    session.delete(tag)
    session.commit()