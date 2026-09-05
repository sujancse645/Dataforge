from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import health, configurations, experiments

app = FastAPI(
    title="Coverage Cliff API",
    version="1.0.0",
    description="FastAPI backend for Coverage Cliff Experiment Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(configurations.router, prefix="/api/v1", tags=["Configurations"])
app.include_router(experiments.router, prefix="/api/v1", tags=["Experiments"])
