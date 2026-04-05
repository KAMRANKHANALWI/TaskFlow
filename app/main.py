from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models.user import User
from app.models.project import Project
from app.models.tag import Tag, TaskTagLink
from app.models.task import Task

from app.routers import auth, users, projects, tasks, tags

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("✅ Database tables created")
    yield

app = FastAPI(title="TaskFlow", version="1.0.0", lifespan=lifespan)

# public — no auth
app.include_router(auth.router)

# protected — auth enforced at router level
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(tags.router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "app": "TaskFlow"}