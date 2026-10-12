import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.crops import router as crops_router
from routes.farm import router as farm_router
from routes.health import router as health_router
from routes.rotation import router as rotation_router

app = FastAPI(
    title="Field Shift Demo API",
    version="0.1.0",
    description="Rule-based crop planning API using clearly labelled mock data.",
)

LOCAL_FRONTEND_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


def get_allowed_origins() -> list[str]:
    configured_origins = os.getenv("FIELD_SHIFT_CORS_ORIGINS", "")
    extra_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
    return list(dict.fromkeys([*LOCAL_FRONTEND_ORIGINS, *extra_origins]))


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(crops_router, prefix="/api")
app.include_router(farm_router, prefix="/api")
app.include_router(rotation_router, prefix="/api")


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "service": "Field Shift Demo API",
        "docs": "/docs",
        "notice": "Demo / Mock Data — not a scientifically validated forecast",
    }
