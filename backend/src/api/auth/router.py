import logging
from typing import Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from application import dto
from application import interactors
from application.services import Authenticator

from .. import schemas

router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post(
    "/register",
    description="Method for register new user by password",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccessTokenResponse,
)
async def register_user(
        auth: FromDishka[Authenticator],
        creator: FromDishka[interactors.CreateUser],
        response: Response,
        data: schemas.UserCreateByPassword | schemas.UserGoogle,
) -> schemas.AccessTokenResponse:
    user_data = dto.NewUser(email=data.email)
    if isinstance(data, schemas.UserCreateByPassword):
        user_data.user_name = data.user_name
        user_data.hashed_password = auth.get_password_hash(data.password)
    elif isinstance(data, schemas.UserGoogle):
        user_data.google_id = data.google_id

    try:
        uuid_id = await creator(user_data)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Failed to create user: email '{data.email}' is exists",
        ) from error

    access_token = auth.set_access_token(uuid_id, response)
    auth.set_refresh_token(uuid_id, response)

    return schemas.AccessTokenResponse(access_token=access_token)


async def _common_login_logic(
        response: Response,
        auth: Authenticator,
        interactor: interactors.GetUserByEmail,
        email: str,
        password: Optional[str] = None,
) -> schemas.AccessTokenResponse:
    user = await interactor(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this user is not registered",
        )

    if password and not auth.verify_password(plain_password=password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect email or password",
        )

    access_token = auth.set_access_token(user.uuid_id, response)
    auth.set_refresh_token(user.uuid_id, response)

    return schemas.AccessTokenResponse(access_token=access_token)


@router.post(
    "/login/form",
    description="Login using form-data (OAuth2 compatible)",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenFormResponse,
)
async def login_by_form(
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.GetUserByEmail],
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.TokenFormResponse:
    token_data = await _common_login_logic(
        response=response,
        auth=auth,
        interactor=interactor,
        email=form_data.username,
        password=form_data.password,
    )

    return schemas.TokenFormResponse(access_token=token_data.access_token)


@router.post(
    "/login",
    description="Login using JSON body",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def login_by_json(
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.GetUserByEmail],
        response: Response,
        data: schemas.UserLoginByPassword | schemas.UserGoogle,
) -> schemas.AccessTokenResponse:
    return await _common_login_logic(
        response=response,
        auth=auth,
        interactor=interactor,
        email=data.email,
        password=data.password if isinstance(data, schemas.UserLoginByPassword) else None,
    )


@router.post(
    "/logout",
    description="Method for logout user",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def logout_user(
        auth: FromDishka[Authenticator],
        user: FromDishka[dto.CurrentUser],
        response: Response,
) -> schemas.UserMessageResponse:
    auth.delete_access_token(response)
    auth.delete_refresh_token(response)

    logging.info("user id=%s logout successfully", user.id)
    return schemas.UserMessageResponse(
        ok=True,
        message="logout successfully",
    )


@router.get(
    "/profile",
    description="Method for get user info",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserInfoResponse,
)
async def get_user_profile(
        user: FromDishka[dto.CurrentUser],
) -> schemas.UserInfoResponse:
    return schemas.UserInfoResponse(**user.dict())


@router.post(
    "/refresh",
    description="Method for refresh user token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def process_refresh_token(
        auth: FromDishka[Authenticator],
        response: Response,
) -> schemas.AccessTokenResponse:
    access_token = auth.process_refresh_token(response)
    return schemas.AccessTokenResponse(access_token=access_token.value)


@router.patch(
    "/update",
    description="Method for update user data",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserInfoResponse,
)
async def update_user_data(
        user: FromDishka[dto.CurrentUser],
        updater: FromDishka[interactors.UpdateUserByUUID],
        interactor: FromDishka[interactors.GetUserByUUID],
        data: schemas.UserUpdate,
) -> schemas.UserInfoResponse:
    update_data = dto.UpdateUser(
        email=data.email,
        user_name=data.user_name,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    await updater(user.uuid_id, update_data)

    update_user = await interactor(user.uuid_id)
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while retrieving updated user data",
        )

    return schemas.UserInfoResponse(**update_user.dict())
