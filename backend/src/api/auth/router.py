import logging
from typing import Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, Depends, HTTPException, status
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
    response_model=schemas.UserResponse,
)
async def register_user(
        auth: FromDishka[Authenticator],
        creator: FromDishka[interactors.CreateUser],
        data: schemas.UserCreateByPassword | schemas.UserGoogle,
) -> schemas.UserResponse:
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

    return schemas.UserResponse(uuid_id=uuid_id)


async def _common_login_logic(
        auth: Authenticator,
        interactor: interactors.GetUserByEmail,
        email: str,
        password: Optional[str] = None,
) -> schemas.Token2Response:
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

    access_token = auth.set_access_token(user.uuid_id)
    refresh_token = auth.set_refresh_token(user.uuid_id)

    return schemas.Token2Response(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/login/form",
    description="Login using form-data (OAuth2 compatible)",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenResponse,
)
async def login_by_form(
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.GetUserByEmail],
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.TokenResponse:
    token_data = await _common_login_logic(
        auth=auth,
        interactor=interactor,
        email=form_data.username,
        password=form_data.password,
    )

    return schemas.TokenResponse(access_token=token_data.access_token)


@router.post(
    "/login",
    description="Login using JSON body",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenResponse,
)
async def login_by_json(
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.GetUserByEmail],
        data: schemas.UserLoginByPassword | schemas.UserGoogle,
) -> schemas.Token2Response:
    return await _common_login_logic(
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
) -> schemas.UserMessageResponse:
    auth.delete_access_token()
    auth.delete_refresh_token()

    logging.info("user id=%s logout successfully", user.id)
    return schemas.UserMessageResponse(
        ok=True,
        message="logout successfully",
    )


@router.get(
    "/me",
    description="Method for get user info",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserInfoResponse,
)
async def get_me_user(
        user: FromDishka[dto.CurrentUser],
) -> schemas.UserInfoResponse:
    return schemas.UserInfoResponse(**user.dict())


@router.post(
    "/refresh",
    description="Method for refresh user token",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def process_refresh_token(
        auth: FromDishka[Authenticator],
        user: FromDishka[dto.CurrentUser],
) -> schemas.UserMessageResponse:
    auth.set_access_token(user.uuid_id)
    auth.set_refresh_token(user.uuid_id)

    return schemas.UserMessageResponse(
        ok=True,
        message="tokens successfully updated",
    )


@router.put(
    "/update",
    description="Method for update user data",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def update_user_data(
        user: FromDishka[dto.CurrentUser],
        updater: FromDishka[interactors.UpdateUserByUUID],
        data: schemas.UserUpdate,
) -> schemas.UserMessageResponse:
    update_data = dto.UpdateUser(
        email=data.email,
        user_name=data.user_name,
        first_name=data.first_name,
        last_name=data.last_name,
    )
    await updater(user.uuid_id, update_data)

    return schemas.UserMessageResponse(
        ok=True,
        message="user data successfully updated",
    )
