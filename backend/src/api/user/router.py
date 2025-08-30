import logging
import uuid

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status

from application import dto
from application import interactors
from application.services import Authenticator
from application.types import UserAccessRights

from .. import schemas

router = APIRouter(prefix="/user", route_class=DishkaRoute)


@router.get(
    "/profile",
    description="Method for get user info",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserInfoResponse,
)
async def get_user_profile(
        user: FromDishka[dto.CurrentUser],
) -> schemas.UserInfoResponse:
    user_data = schemas.UserInfoResponse(**user.dict())
    user_data.has_password = bool(user.hashed_password)
    return user_data


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


@router.patch(
    "/password",
    description="Method for change user password",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserInfoResponse,
)
async def update_user_password(
        auth: FromDishka[Authenticator],
        user: FromDishka[dto.CurrentUser],
        updater: FromDishka[interactors.UpdateUserPassword],
        interactor: FromDishka[interactors.GetUserByUUID],
        data: schemas.PasswordUpdate,
) -> schemas.UserInfoResponse:
    if data.current_password:
        if not auth.verify_password(plain_password=data.current_password, hashed_password=user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incorrect current password",
            )

    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new password and confirm password mismatch",
        )

    hashed_password = auth.get_password_hash(data.new_password)
    update_data = dto.UpdatePassword(
        hashed_password=hashed_password,
    )
    await updater(user, update_data)

    update_user = await interactor(user.uuid_id)
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while retrieving updated user data",
        )

    return schemas.UserInfoResponse(**update_user.dict())


@router.get(
    "/rights/{uuid_id}",
    description="Method for get user access rights",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserAccessRightsSchema,
)
async def get_user_access_rights(
        _: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.GetUserByUUID],
        permission_interactor: FromDishka[interactors.GetCurrentAccessPermission],
        uuid_id: uuid.UUID
) -> schemas.UserAccessRightsSchema:
    user = await interactor(uuid_id)

    if not user:
        logging.error("error user '%s' not found", uuid_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error user '{uuid_id}' not found",
        )

    expires_at = None
    if user.access_rights != UserAccessRights.DEFAULT:
        permission = await permission_interactor(user.id)
        expires_at = permission.expires_at if permission else None

    return schemas.UserAccessRightsSchema(uuid_id=user.uuid_id, access_rights=user.access_rights, expires_at=expires_at)


@router.post(
    "/rights",
    description="Method for set user access rights",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserAccessRightsSchema,
)
async def set_user_access_rights(
        _: FromDishka[dto.AdminUser],
        interactor: FromDishka[interactors.GetUserByUUID],
        updater: FromDishka[interactors.UpdateUserByUUID],
        data: schemas.UserAccessRightsSchema,
) -> schemas.UserAccessRightsSchema:
    update_data = dto.UpdateUser(access_rights=data.access_rights)
    update_id = await updater(data.uuid_id, update_data)
    user = await interactor(data.uuid_id)

    if not update_id or not user:
        logging.error("error update success rights '%s' for user '%s'", data.access_rights, data.uuid_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error update success rights for user '{data.uuid_id}'",
        )

    return schemas.UserAccessRightsSchema(uuid_id=user.uuid_id, access_rights=user.access_rights)
