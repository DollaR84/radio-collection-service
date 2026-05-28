import asyncio

from config import Config

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from application import dto
from application.services import Authenticator

from .orchestrators import AuthOrchestrator
from .orchestrators.exceptions import EmailIsExists, NotRegistered, IncorrectLoginData, SubscribeExpired

from .. import schemas


router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post(
    "/register",
    description="Method for register new user by password",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccessTokenResponse,
)
async def register_user(
        auth: FromDishka[AuthOrchestrator],
        response: Response,
        data: schemas.UserCreateByPassword,
) -> schemas.AccessTokenResponse:
    try:
        return await auth(data, response)
    except EmailIsExists as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to create user: email is exists",
        ) from error
    except NotRegistered as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register new user",
        ) from error


@router.post(
    "/login/form",
    description="Login using form-data (OAuth2 compatible)",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenFormResponse,
)
async def login_by_form(
        auth: FromDishka[AuthOrchestrator],
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.TokenFormResponse:
    data = schemas.UserLoginByPassword(
        email=form_data.username,
        password=form_data.password,
    )

    try:
        token_data = await auth(data, response)
    except IncorrectLoginData as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect email or password",
        ) from error

    return schemas.TokenFormResponse(access_token=token_data.access_token)


@router.post(
    "/login",
    description="Login using JSON body",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def login_by_json(
        auth: FromDishka[AuthOrchestrator],
        response: Response,
        data: schemas.UserLoginByPassword,
) -> schemas.AccessTokenResponse:
    try:
        return await auth(data, response)
    except IncorrectLoginData as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect email or password",
        ) from error
    except SubscribeExpired as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscribe has be expired. Need bye month subscribe",
        ) from error


@router.post(
    "/google",
    description="Login using google id token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def login_by_google_id_token(
        auth: FromDishka[AuthOrchestrator],
        config: FromDishka[Config],
        response: Response,
        data: schemas.UserGoogleToken,
) -> schemas.AccessTokenResponse:
    try:
        id_info = await asyncio.to_thread(
            id_token.verify_oauth2_token,
            data.id_token,
            google_requests.Request(),
            config.google.client_id
        )

        if "accounts.google.com" not in id_info["iss"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong token issuer. Only official Google tokens are allowed."
            )

        id_info["device_id"] = data.device_id
        return await auth(id_info, response)

    except NotRegistered as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register new user",
        ) from error
    except SubscribeExpired as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscribe has be expired. Need bye month subscribe",
        ) from error
    except ValueError as error:
        error_msg = str(error).lower()

        if "token has expired" in error_msg or "expired" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google ID Token has expired. Please refresh it on the client side."
            ) from error

        if "signature" in error_msg or "invalidate" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token signature. Cryptographic check failed."
            ) from error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed token. It is not a valid JWT or Google ID token."
        ) from error


@router.get(
    "/google",
    description="Login using google id",
    status_code=status.HTTP_302_FOUND,
)
async def login_by_google(
        auth: FromDishka[Authenticator],
        config: FromDishka[Config],
        request: Request,
) -> RedirectResponse:
    redirect_uri = "/".join([config.google.redirect_url, "api", "auth", "google", "callback"])
    redirect: RedirectResponse = await auth.oauth.google.authorize_redirect(request, redirect_uri)
    return redirect


@router.get(
    "/google/callback",
    status_code=status.HTTP_302_FOUND,
)
async def google_callback(
        auth: FromDishka[AuthOrchestrator],
        authenticator: FromDishka[Authenticator],
        config: FromDishka[Config],
        request: Request,
) -> RedirectResponse:
    token = await authenticator.oauth.google.authorize_access_token(request)
    if "userinfo" in token:
        user_data = token.get("userinfo")
    else:
        user_data = await authenticator.oauth.google.userinfo(token=token)

    redirect_uri = "/".join([config.google.redirect_url, "profile"])
    redirect = RedirectResponse(redirect_uri)

    try:
        await auth(user_data, redirect)
    except NotRegistered as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register new user",
        ) from error

    return redirect


@router.get(
    "/validate",
    description="Method for validate access token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def validate_access_token(
        token: FromDishka[dto.AccessToken],
        auth: FromDishka[Authenticator],
) -> schemas.UserMessageResponse:
    try:
        auth.check_access_token(token)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired",
        ) from error

    return schemas.UserMessageResponse(
        ok=True,
        message="access token is valid",
    )


@router.post(
    "/logout",
    description="Method for logout user",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def logout_user(
        auth: FromDishka[Authenticator],
        _: FromDishka[dto.CurrentUser],
        response: Response,
) -> schemas.UserMessageResponse:
    auth.delete_access_token(response)
    auth.delete_refresh_token(response)

    return schemas.UserMessageResponse(
        ok=True,
        message="logout successfully",
    )


@router.post(
    "/refresh",
    description="Method for refresh user token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def process_refresh_token(
        auth: FromDishka[Authenticator],
        request: Request,
        response: Response,
) -> schemas.AccessTokenResponse:
    access_token = auth.process_refresh_token(request, response)
    return schemas.AccessTokenResponse(access_token=access_token.value)


@router.get(
    "/status",
    description="Method for get status authentication",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessStatusResponse,
)
async def get_authentication_status(
        user: FromDishka[dto.CurrentUser],
) -> schemas.AccessStatusResponse:
    return schemas.AccessStatusResponse(authenticated=bool(user))


@router.get(
    "/token",
    description="Method for get access token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def get_access_token(
        token: FromDishka[dto.AccessToken],
) -> schemas.AccessTokenResponse:
    return schemas.AccessTokenResponse(access_token=token.value)
