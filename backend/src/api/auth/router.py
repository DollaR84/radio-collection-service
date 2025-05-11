from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status

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


@router.post(
    "/login",
    description="Method for login user by password",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def login_user(
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.GetUserByEmail],
        data: schemas.UserLoginByPassword | schemas.UserGoogle,
) -> schemas.UserMessageResponse:
    user = await interactor(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this user is not registered",
        )

    if isinstance(data, schemas.UserLoginByPassword):
        if not auth.verify_password(plain_password=data.password, hashed_password=user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incorrect email or password",
            )

    access_token = auth.set_access_token(user.uuid_id)
    refresh_token = auth.set_refresh_token(user.uuid_id)

    return schemas.UserMessageTokenResponse(
        ok=True,
        message="Authorization successful",
        access=access_token,
        refresh=refresh_token,
    )


@router.post(
    "/logout",
    description="Method for logout user",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserMessageResponse,
)
async def logout_user(
        auth: FromDishka[Authenticator],
) -> schemas.UserMessageResponse:
    auth.delete_access_token()
    auth.delete_refresh_token()

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
