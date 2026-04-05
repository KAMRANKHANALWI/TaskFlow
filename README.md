# TaskFlow API

A full-stack Task Management REST API built with FastAPI, SQLModel, and SQLite — covering all major FastAPI concepts in a single production-style project.

## Tech Stack

- **FastAPI** — web framework with auto Swagger docs
- **SQLModel** — ORM (SQLAlchemy + Pydantic combined)
- **SQLite** — lightweight file-based database
- **JWT (python-jose)** — stateless authentication
- **bcrypt** — password hashing
- **pydantic-settings** — environment variable management
- **uv** — fast Python package manager

## Features

- Full CRUD — Projects, Tasks, Tags
- M:N relationships — Tags ↔ Tasks via link table
- JWT authentication — register, login, protected routes
- Ownership checks — users can only edit/delete their own resources
- Query filtering — filter tasks by status, priority, project
- Pagination — offset/limit on all list endpoints
- CORS middleware — ready for Next.js frontend
- Request logging — every request logged with method, path, status, duration
- Background tasks — async post-response work (email simulation)
- Global exception handlers — consistent error format across all endpoints
- Auto docs — Swagger UI at /docs, ReDoc at /redoc

## Project Structure

```
app/
├── main.py          # app entry, lifespan, middleware, exception handlers
├── config.py        # pydantic-settings — reads from .env
├── database.py      # SQLModel engine + session
├── dependencies.py  # get_session, get_current_user
│
├── models/          # SQLModel table=True — maps to DB tables
│   ├── user.py      # User
│   ├── project.py   # Project
│   ├── task.py      # Task
│   └── tag.py       # Tag + TaskTagLink (M:N bridge)
│
├── schemas/         # Pydantic BaseModel — API input/output shapes
│   ├── user.py      # UserCreate, UserOut, TokenOut
│   ├── project.py   # ProjectCreate, ProjectUpdate, ProjectOut
│   ├── task.py      # TaskCreate, TaskUpdate, TaskOut
│   └── tag.py       # TagCreate, TagOut
│
├── routers/         # one file per feature
│   ├── auth.py      # POST /auth/register, /auth/login
│   ├── users.py     # GET /users/me
│   ├── projects.py  # full CRUD /projects
│   ├── tasks.py     # full CRUD /tasks + filters + background task
│   └── tags.py      # /tags + M:N assign/remove
│
└── utils/
    └── auth.py      # hash_password, verify_password, JWT encode/decode
```

## API Endpoints

### Auth (public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Create new account |
| POST | /auth/login | Login, returns JWT token |

### Users (protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users/me | Get current user profile |

### Projects (protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /projects/ | List all projects (paginated) |
| POST | /projects/ | Create project |
| GET | /projects/{id} | Get project by id |
| PUT | /projects/{id} | Update project (owner only) |
| DELETE | /projects/{id} | Delete project (owner only) |

### Tasks (protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks/ | List tasks (filter by status, priority, project) |
| POST | /tasks/ | Create task |
| GET | /tasks/{id} | Get task by id |
| PUT | /tasks/{id} | Update task (assignee only) |
| DELETE | /tasks/{id} | Delete task (assignee only) |

### Tags (protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tags/ | List all tags |
| POST | /tags/ | Create tag |
| POST | /tags/{tag_id}/tasks/{task_id} | Assign tag to task |
| DELETE | /tags/{tag_id}/tasks/{task_id} | Remove tag from task |
| DELETE | /tags/{id} | Delete tag |

## Setup

```bash
# clone
git clone https://github.com/KAMRANKHANALWI/TaskFlow.git
cd TaskFlow

# install dependencies
uv sync

# create .env from example
cp .env.example .env
# open .env and set a strong SECRET_KEY

# run dev server
uv run uvicorn app.main:app --reload
```

## API Docs

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI — interactive |
| http://localhost:8000/redoc | ReDoc — clean read |
| http://localhost:8000/openapi.json | Raw OpenAPI schema |

## Auth Flow

```
POST /auth/register → creates user, returns UserOut (no password)
POST /auth/login    → verifies password, returns JWT access token
GET  /any-protected → send token as: Authorization: Bearer <token>
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite:///./taskflow.db | Database connection string |
| SECRET_KEY | — | JWT signing key (min 32 chars) |
| ALGORITHM | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Token expiry in minutes |
| DEBUG | True | SQLAlchemy query logging |

## Roadmap

- [x] Phase 1 — DB models + Pydantic schemas
- [x] Phase 2 — CRUD routers (projects, tasks, tags)
- [x] Phase 3 — JWT auth (register, login, protected routes, ownership)
- [x] Phase 4 — Middleware, exception handlers, background tasks
- [ ] Phase 5 — Next.js frontend
- [ ] Phase 6 — Forgot password + email integration
- [ ] Phase 7 — Deploy (Railway / Render)
