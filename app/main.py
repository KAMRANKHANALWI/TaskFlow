from contextlib import asynccontextmanager
import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import create_db_and_tables
from app.models.user import User
from app.models.project import Project
from app.models.tag import Tag, TaskTagLink
from app.models.task import Task
from app.routers import auth, users, projects, tasks, tags

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Lifespan ──────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 TaskFlow starting up...")
    create_db_and_tables()
    logger.info("✅ Database tables ready")
    yield
    logger.info("👋 TaskFlow shutting down")

# ── App ───────────────────────────────────────────────
app = FastAPI(
    title="TaskFlow",
    version="1.0.0",
    description="A task management API built with FastAPI + SQLModel",
    lifespan=lifespan
)

# ── CORS ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request logging middleware ─────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} [{duration}ms]"
    )
    return response

# ── Global exception handlers ─────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "status_code": 422,
            "message": "Validation error",
            "detail": exc.errors()
        }
    )

# ── Routers ───────────────────────────────────────────
# public — no auth
app.include_router(auth.router)
# protected — auth enforced at router level
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(tags.router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "app": "TaskFlow", "version": "1.0.0"}




