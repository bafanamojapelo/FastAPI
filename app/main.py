from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Create tables if they don't exist (only use in dev/test environments, not recommended for production)
# models.Base.metadata.create_all(bind=engine)  # Move this to a separate script or manage migrations via Alembic

app = FastAPI()

# CORS settings (allow requests from all origins, can be restricted if needed)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers for the different API endpoints
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Root path endpoint, returning a simple message
@app.get("/")
def read_root():
    return {"message": "Hello World"}
