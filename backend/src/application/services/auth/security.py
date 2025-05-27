from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Optional
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


class SecurityTool:
    __slots__ = ("config", "pwd_context", "request", "response",)

    def __init__(self, config: SecurityConfig, request: Request):
        self.config: SecurityConfig = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self.request: Request = request
        self.response: Optional[Response] = None

    def setup_response(self, response: Response) -> None:
        self.response = response

    def get_password_hash(self, password: str) -> str:
        hashed_password: str = self.pwd_context.hash(password)
        return hashed_password

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        status: bool = self.pwd_context.verify(plain_password, hashed_password)
        return status

    def create_access_token(self, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.access_token_expire_minutes)
        to_encode.update({"exp": expire.timestamp(), "type": "access"})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=self.config.refresh_token_expire_days)
        to_encode.update({"exp": int(expire.timestamp()), "type": "refresh"})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def check_token(self, token: str, token_type: Literal["access", "refresh"] = "access") -> dict[str, Any]:
        try:
            data: dict[str, Any] = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                options={"verify_exp": True},
            )
            if data.get("type") != token_type:
                raise NoJwtException()

            return data
        except ExpiredSignatureError as error:
            raise TokenExpiredException() from error

        except JWTError as error:
            raise NoJwtException() from error

    def check_expire_token(self, token: str, token_type: Literal["access", "refresh"] = "access") -> dict[str, Any]:
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
            token_type: Literal["access", "refresh"] = "access",
    ) -> uuid.UUID:
        if not any([token, payload]):
            raise NotTokenDataError()

        if not payload and token:
            payload = self.check_token(token, token_type=token_type)

        if not payload:
            raise NotTokenDataError()

        if payload.get("type") != token_type:
            raise NoJwtException()

        uuid_id: str = payload["sub"]
        if not uuid_id:
            raise NoJwtException()

        return uuid.UUID(uuid_id)

    def get_access_token(self) -> str:
        if self.config.cookie.is_enable and self.response:
            token = self.get_token_from_cookie()
        else:
            raise NoJwtException()

        return token

    def get_token_from_cookie(self) -> str:
        token = self.request.cookies.get("user_access_token")
        if not token:
            raise TokenNotFound()

        return token

    def get_refresh_token(self) -> str:
        token = self.request.cookies.get("user_refresh_token")
        if not token:
            raise TokenNotFound()

        return token

    def set_access_token(self, uuid_id: uuid.UUID) -> str:
        access_token = self.create_access_token({"sub": str(uuid_id)})
        if self.config.cookie.is_enable and self.response:
            self.response.set_cookie(
                key=self.config.cookie.access_key,
                value=access_token,
                httponly=self.config.cookie.httponly,
                secure=self.config.cookie.secure,
                samesite=self.config.cookie.samesite,
            )

        return access_token

    def set_refresh_token(self, uuid_id: uuid.UUID) -> str:
        refresh_token = self.create_refresh_token({"sub": str(uuid_id)})
        if self.config.cookie.is_enable and self.response:
            self.response.set_cookie(
                key=self.config.cookie.refresh_key,
                value=refresh_token,
                httponly=self.config.cookie.httponly,
                secure=self.config.cookie.secure,
                samesite=self.config.cookie.samesite,
            )

        return refresh_token

    def delete_access_token(self) -> None:
        if self.config.cookie.is_enable and self.response:
            self.response.delete_cookie(self.config.cookie.access_key)

    def delete_refresh_token(self) -> None:
        if self.config.cookie.is_enable and self.response:
            self.response.delete_cookie(self.config.cookie.refresh_key)
