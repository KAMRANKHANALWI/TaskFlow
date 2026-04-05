from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select
import logging

from app.dependencies import get_session, get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

# ── background function ────────────────────────────────
def notify_task_created(task_title: str, username: str):
    # simulating email — swap this for real email later
    logger.info(f"📧 [EMAIL] Hi {username}! Task '{task_title}' was created.")
    logger.info(f"📧 [EMAIL] Check your TaskFlow dashboard to get started.")

# ── routes ────────────────────────────────────────────
@router.get("/", response_model=list[TaskOut])
def list_tasks(
    skip: int = 0,
    limit: int = 10,
    status: str | None = None,
    priority: str | None = None,
    project_id: int | None = None,
    session: Session = Depends(get_session)
):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if project_id:
        query = query.where(Task.project_id == project_id)
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    background_tasks: BackgroundTasks,          
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = Task(**data.model_dump(exclude={"assignee_id"}), assignee_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # queue notification — runs AFTER response is sent
    background_tasks.add_task(
        notify_task_created,
        task.title,
        current_user.username
    )

    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")
    update_data = data.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")
    session.delete(task)
    session.commit()