# Blog

A simple blog REST API built with **FastAPI** and **MySQL**, supporting users, posts, comments, and JWT-based authentication.

## Features

- **Users** — registration, login (JWT access token), update, delete
- **Posts** — create, list (with author details), delete
- **Comments** — create, list by post, update, delete
- **Auth** — JWT bearer token authentication for protected routes
- **Migrations** — schema versioning via Alembic

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | MySQL (via PyMySQL) |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Validation | Pydantic |

## Project Structure

```
Blog/
├── main.py                    # FastAPI app entrypoint, router registration
├── alembic/                   # Database migrations
│   └── versions/
├── alembic.ini
├── test_main.http             # Sample HTTP requests for manual testing
└── backend/
    ├── api/
    │   ├── users/
    │   │   ├── models.py       # User SQLAlchemy model
    │   │   ├── router.py       # /users endpoints
    │   │   └── schemas/        # Request/response Pydantic schemas
    │   ├── posts/
    │   │   ├── models.py       # Posts, Authors SQLAlchemy models
    │   │   ├── router.py       # /posts endpoints
    │   │   └── schema/
    │   └── comments/
    │       ├── models.py       # Comment SQLAlchemy model
    │       ├── router.py       # /comments endpoints
    │       └── schemas/
    └── utils/
        ├── database.py         # Engine/session setup
        ├── auth.py              # Token verification, user authentication
        └── hash_password.py     # Password hashing, JWT creation
```

## Setup

### Prerequisites

- Python 3.10+
- A running MySQL server with a `Blog` database created

### Install dependencies

There's no `requirements.txt` in the repo yet. Install the packages this project imports directly:

```bash
pip install fastapi uvicorn sqlalchemy pymysql alembic pydantic "python-jose[cryptography]" "passlib[bcrypt]"
```

### Configure the database

Database credentials are currently hardcoded in `backend/utils/database.py`:

```python
DB_URL = 'mysql://root:Adeel_Dec6@127.0.0.1:3306/Blog'
```

Update this to match your local MySQL setup, or (recommended) move it to an environment variable — see [CLAUDE.md](./CLAUDE.md) for details.

### Run migrations

```bash
alembic upgrade head
```

### Start the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Overview

### Users (`/users`)
| Method | Path | Auth required | Description |
|---|---|---|---|
| POST | `/users/api/v1/login` | No | Log in, returns JWT access token |
| POST | `/users/creat_users` | Yes | Create a new user |
| GET | `/users/get_user` | Yes | List all users |
| PUT | `/users/update_user` | Yes | Update the authenticated user |
| DELETE | `/users/delete_user/{user_id}` | No | Delete a user by ID |

### Posts (`/posts`)
| Method | Path | Description |
|---|---|---|
| GET | `/posts/get_post` | List all posts with author info |
| POST | `/posts/create_post` | Create a new post |
| DELETE | `/posts/delete_post/{post_id}` | Delete a post by ID |

### Comments (`/comments`)
| Method | Path | Description |
|---|---|---|
| POST | `/comments/comments` | Create a comment on a post |
| GET | `/comments/get_comments/{post_id}` | List comments for a post |
| PATCH | `/comments/update_comments` | Update a comment |
| DELETE | `/comments/delete_comments` | Delete a comment |

## Testing Endpoints Manually

`test_main.http` contains sample HTTP requests you can run directly from an IDE (PyCharm/VS Code REST Client) to try out the API.

## Known Gaps / Roadmap

- No `requirements.txt` / dependency lock file yet
- Database credentials and JWT secret key are hardcoded — move to environment variables
- No automated tests
- `create_user` endpoint requires auth but there's no initial way to create the first user without one