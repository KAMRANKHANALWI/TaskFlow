from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.dependencies import get_session, get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(
    prefix="/projects", tags=["projects"], dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[ProjectOut])
def list_projects(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    projects = session.exec(select(Project).offset(skip).limit(limit)).all()
    return projects


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return project


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    project = Project(**data.model_dump(), owner_id=current_user.id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    if project.owner_id != current_user.id:  
        raise HTTPException(status_code=403, detail="Not your project")

    update_data = data.model_dump(exclude_unset=True)
    project.sqlmodel_update(update_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user), 
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    if project.owner_id != current_user.id:  
        raise HTTPException(status_code=403, detail="Not your project")
    session.delete(project)
    session.commit()
