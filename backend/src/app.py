import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database.migrator import SQLMigrator

import config


config.load_environment_variables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run database migrations on startup"""
    db_path = os.getenv("DATABASE_PATH")

    if not db_path:
        raise ValueError("DATABASE_PATH environment variable is not set.")

    migrator = SQLMigrator(db_url=db_path)
    migrator.run_migrations()

    yield


app = FastAPI(title="FastAPI WebApp", lifespan=lifespan)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI WebApp"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
