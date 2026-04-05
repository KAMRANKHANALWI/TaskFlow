# TaskFlow API

A full-stack Task Management REST API built with FastAPI, SQLModel, and SQLite.

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM (SQLAlchemy + Pydantic)
- **SQLite** — database
- **JWT + bcrypt** — authentication (Phase 3)
- **uv** — package manager

## Project Structure
```
app/
├── main.py          # app entry point, lifespan, routers
├── config.py        # settings from .env
├── database.py      # engine + session
├── dependencies.py  # get_session, get_current_user
├── models/          # SQLModel DB tables
├── schemas/         # Pydantic request/response shapes
├── routers/         # one file per feature
└── utils/           # auth helpers (JWT, bcrypt)
```

## Setup
```bash
# clone and enter
git clone https://github.com/KAMRANKHANALWI/TaskFlow.git
cd TaskFlow

# install dependencies
uv sync

# create .env from example
cp .env.example .env
# edit .env and set your SECRET_KEY

# run
uv run uvicorn app.main:app --reload
```

## API Docs

Visit `http://localhost:8000/docs` after running.

## Phases

- [x] Phase 1 — DB models + Pydantic schemas
- [x] Phase 2 — CRUD routers (projects, tasks, tags)
- [ ] Phase 3 — JWT auth (register, login, protected routes)
- [ ] Phase 4 — Middleware, exception handlers, background tasks
