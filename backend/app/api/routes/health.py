from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description="Returns the current health status of the API.",
)
def health_check() -> dict[str, str]:
    return {"status": "ok"}
