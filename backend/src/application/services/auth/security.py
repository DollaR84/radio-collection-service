from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import uuid

from fastapi import Request, Response

from jose import jwt, JWTError, ExpiredSignatureError

from passlib.context import CryptContext

from config import SecurityConfig

from .exceptions import (
    NotTokenDataError,
    NoJwtException,
    TokenExpiredException,
    TokenExpiredNotFoundException,
    TokenNotFound,
)
from .types import TokenType


class SecurityTool:
    __slots__ = ("config", "pwd_context",)

    def __init__(self, config: SecurityConfig):
        self.config: SecurityConfig = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        hashed_password: str = self.pwd_context.hash(password)
        return hashed_password

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        status: bool = self.pwd_context.verify(plain_password, hashed_password)
        return status

    def create_token(self, data: dict[str, Any], token_type: TokenType, time_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + time_delta
        to_encode.update({"exp": expire.timestamp(), "type": token_type.value})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def check_token(self, token: str, token_type: TokenType) -> dict[str, Any]:
        try:
            data: dict[str, Any] = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                options={"verify_exp": True},
            )
            if data.get("type") != token_type.value:
                raise NoJwtException()

            return data
        except ExpiredSignatureError as error:
            raise TokenExpiredException() from error

        except JWTError as error:
            raise NoJwtException() from error

    def check_expire_token(self, token: str, token_type: TokenType) -> dict[str, Any]:
        payload = self.check_token(token, token_type=token_type)

        current_time = datetime.now(timezone.utc).timestamp()
        if "exp" in payload:
            if current_time > payload["exp"]:
                raise TokenExpiredException()
        else:
            raise TokenExpiredNotFoundException()

        return payload

    def get_uuid_from_token(
            self,
            token: Optional[str] = None,
            payload: Optional[dict[str, Any]] = None,
            token_type: TokenType = TokenType.ACCESS,
    ) -> uuid.UUID:
        if not any([token, payload]):
            raise NotTokenDataError()

        if not payload and token:
            payload = self.check_expire_token(token, token_type=token_type)

        if not payload:
            raise NotTokenDataError()

        if payload.get("type") != token_type.value:
            raise NoJwtException()

        uuid_id: str = payload["sub"]
        if not uuid_id:
            raise NoJwtException()

        return uuid.UUID(uuid_id)

    def get_access_token(self, request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            raise TokenNotFound()

        return token

    def get_refresh_token(self, request: Request) -> str:
        token = request.cookies.get("refresh_token")
        if not token:
            raise TokenNotFound()

        return token

    def set_access_token(self, uuid_id: uuid.UUID, response: Response) -> str:
        time_delta = timedelta(minutes=self.config.access_token_expire_minutes)
        access_token = self.create_token({"sub": str(uuid_id)}, TokenType.ACCESS, time_delta)

        response.set_cookie(
            key=self.config.cookie.access_key,
            value=access_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
            max_age=int(time_delta.total_seconds()),
            path="/",
        )

        return access_token

    def set_refresh_token(self, uuid_id: uuid.UUID, response: Response) -> str:
        time_delta = timedelta(days=self.config.refresh_token_expire_days)
        refresh_token = self.create_token({"sub": str(uuid_id)}, TokenType.REFRESH, time_delta)

        response.set_cookie(
            key=self.config.cookie.refresh_key,
            value=refresh_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
            max_age=int(time_delta.total_seconds()),
            path="/",
        )

        return refresh_token

    def delete_access_token(self, response: Response) -> None:
        response.delete_cookie(self.config.cookie.access_key)

    def delete_refresh_token(self, response: Response) -> None:
        response.delete_cookie(self.config.cookie.refresh_key)
