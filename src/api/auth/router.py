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
async def register_user_by_password(
        data: schemas.UserCreateByPassword,
        auth: FromDishka[Authenticator],
        interactor: FromDishka[interactors.CreateUser],
) -> schemas.UserResponse:
    user_data = dto.NewUser(
        email=data.email,
        user_name=data.user_name,
        hashed_password=auth.get_password_hash(data.password),
    )

    try:
        user = await interactor(user_data)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Failed to create user: email '{data.email}' is exists",
        ) from error

    return schemas.UserResponse(uuid_id=user.uuid_id)
