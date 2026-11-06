"""
Health endpoints.

Design notes:
- /health        -> liveness, always cheap. Does NOT touch the DB.
- /health/db     -> readiness for the DB. Separate so orchestrators can
                    distinguish "app is up" from "app can serve traffic".
- /health/worker -> placeholder until the monitoring worker exists (Phase 3).
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.db.session import ping_database

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", summary="Liveness probe")
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@router.get("/health/db", summary="Database readiness probe")
def health_db() -> JSONResponse:
    ok = ping_database()
    payload = {"status": "ok" if ok else "error", "database": "reachable" if ok else "unreachable"}
    return JSONResponse(
        status_code=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=payload,
    )


@router.get("/health/worker", summary="Monitoring worker readiness (Phase 3)")
def health_worker() -> JSONResponse:
    # Phase 1 stub: the worker doesn't exist yet, so report "unknown" but
    # keep the endpoint shape stable for the frontend and CI.
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "unknown", "detail": "worker not implemented until Phase 3"},
    )
