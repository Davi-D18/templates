from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK, summary="Health check")
async def health_check():
    return {"status": "ok"}
