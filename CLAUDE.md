# CLAUDE.md

Guidance for Claude Code (or any AI coding agent) working in this repository.

## Project Summary

FastAPI blog backend with MySQL, using SQLAlchemy for ORM and Alembic for migrations. Three domains: `users`, `posts`, `comments`, each following the same pattern: `models.py` (SQLAlchemy), `router.py` (FastAPI routes), and a `schemas/` (or `schema/`) folder with `request.py` / `response.py` (Pydantic).

## Architecture Conventions

- **Entry point**: `main.py` creates the `FastAPI()` app and includes the three routers (`posts`, `users`, `comments`).
- **Per-domain module layout** (follow this pattern for any new domain):
  ```
  backend/api/<domain>/
      models.py           # SQLAlchemy models, inherit from backend.utils.database.Base
      router.py           # APIRouter with prefix="/<domain>", tags=["<Domain>"]
      schemas/ (or schema/)   # NOTE: naming is inconsistent — posts uses "schema", users/comments use "schemas"
          request.py       # Pydantic request models
          response.py      # Pydantic response models
  ```
- **DB session**: obtained via `Depends(get_db)` from `backend.utils.database`, imported per-router.
- **Auth**: `Depends(get_current_user)` from `backend.utils.auth` protects a route; it validates a JWT bearer token and returns the `username` from the token payload (not a full user object).
- **Migrations**: managed with Alembic; migration scripts live in `alembic/versions/`. Run `alembic revision --autogenerate -m "message"` after model changes, then `alembic upgrade head`.

## Known Issues to Be Careful About

When touching related code, be aware of these existing problems — fix them if you're already working in that area, but don't go out of your way to do a large unrelated refactor unless asked:

1. **Hardcoded secrets** — `backend/utils/database.py` has a hardcoded MySQL connection string (including a plaintext password), and `backend/utils/hash_password.py` has `SECRET_KEY = "your-secret-key"` hardcoded. Both should come from environment variables (e.g. via `python-dotenv` or `pydantic-settings`). Never commit real secrets when fixing this — use `.env` + `.env.example` and confirm `.env` is gitignored (it already is).
2. **Incorrect `HTTPException` import** — `backend/api/users/router.py` imports `HTTPException` from `http.client` instead of `fastapi`. This means `raise HTTPException("Email already registered")` in `create_user` won't behave like a proper FastAPI HTTP error response. Fix by importing from `fastapi` and using `status_code=...`, `detail=...` kwargs.
3. **Chicken-and-egg auth on user creation** — `POST /users/creat_users` requires `Depends(get_current_user)`, meaning there's no way to create the very first user without already having a valid token. Consider whether registration should be public, or gated behind an admin-only flow.
4. **No password verification before token issuance sanity check** — `authenticate_user` in `auth.py` returns `False` on failure, but `router.py`'s `/login` doesn't check that return value before using `user_response.username` — this will raise an `AttributeError` on wrong password instead of a clean 401. Fix by checking `if not user_response: raise HTTPException(401, ...)`.
5. **No dependency manifest** — there's no `requirements.txt`/`pyproject.toml`. If you add or update dependencies, please create/update one so environments are reproducible.
6. **Directory naming inconsistency** — `posts` uses `schema/` (singular) while `users` and `comments` use `schemas/` (plural). Match whichever directory already exists in that domain; don't unify them unless explicitly asked, since it would break existing imports across the codebase.
7. **No automated tests** — only `test_main.http` (manual HTTP requests) exists. If asked to add tests, prefer `pytest` + FastAPI's `TestClient`, with a separate test database or mocked session.

## Coding Conventions to Follow

- Keep routers thin: business logic inline is currently acceptable at this codebase's size, but prefer small, readable functions over deeply nested logic.
- Pydantic response models should mirror the SQLAlchemy models' public fields, not full DB objects (e.g. never return the `password` field).
- Use `db: Session = Depends(get_db)` for all new endpoints needing DB access — don't create ad hoc engine/session instances elsewhere.
- Match the existing return style: most endpoints return plain dicts like `{"message": "..."}` for simple confirmations, and Pydantic response models for data-bearing responses.

## Commands

```bash
# Install dependencies (no lockfile yet — install these directly)
pip install fastapi uvicorn sqlalchemy pymysql alembic pydantic "python-jose[cryptography]" "passlib[bcrypt]"

# Run the dev server
uvicorn main:app --reload

# Create a new migration after changing models
alembic revision --autogenerate -m "describe change"

# Apply migrations
alembic upgrade head
```

## Do Not

- Do not commit real database credentials or secret keys, even temporarily.
- Do not remove the `Author`/`Authors` model distinction between `posts` schema (`Author`) and SQLAlchemy model (`Authors`) without checking all usages — they're intentionally separate (Pydantic vs. ORM).
- Do not rename `schema`/`schemas` folders across domains as a "cleanup" unless explicitly requested, since it's a breaking import change.