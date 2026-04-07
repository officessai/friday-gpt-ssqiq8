"""Health endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    """Basic liveness probe."""
    return {"status": "ok"}
