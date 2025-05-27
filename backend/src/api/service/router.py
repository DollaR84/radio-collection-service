from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from application.services import NoService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/form",
    scheme_name="Bearer",
    scopes={},
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    description="Method for root page stub",
    status_code=status.HTTP_200_OK,
)
async def index(reasigner: FromDishka[NoService]) -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {
        "status": "OK",
        "reason": await reasigner("To login, follow the link: '/auth'"),
    }

    return JSONResponse(content=response, status_code=status_code)


@router.get(
    "/health",
    description="Method for check health api backend",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {"status": "OK"}

    return JSONResponse(content=response, status_code=status_code)


@router.get(
    "/dummy",
    description="Method for depends oauth2_scheme",
    status_code=status.HTTP_200_OK,
)
async def dummy_route(reasigner: FromDishka[NoService], _: str = Depends(oauth2_scheme)) -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {
        "status": "OK",
        "reason": await reasigner("dummy route"),
    }

    return JSONResponse(content=response, status_code=status_code)


@router.get(
    "/docs",
    include_in_schema=False,
)
async def custom_swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "oauth2RedirectUrl": "/oauth2-redirect",
            "initOAuth": {
                "clientId": "swagger-ui",
                "usePkceWithAuthorizationCodeGrant": True,
            }
        }
    )
