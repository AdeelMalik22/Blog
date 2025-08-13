from fastapi import FastAPI

from backend.api.comments.router import router as comments_router
from backend.api.posts.router import router as posts_router
from backend.api.users.router import router as users_router

app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(comments_router)