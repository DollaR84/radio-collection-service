from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get(
    "/health",
    description="Method for check health api backend",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {"status": "OK"}

    return JSONResponse(content=response, status_code=status_code)
