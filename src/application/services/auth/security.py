from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from fastapi import Request, Response

from jose import jwt, JWTError, ExpiredSignatureError

from passlib.context import CryptContext

from config import SecurityConfig

from .exceptions import NotTokenDataError, NoJwtException, TokenExpiredException, TokenNotFound


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

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.config.access_token_expire_minutes)
        to_encode.update({"exp": int(expire.timestamp()), "type": "access"})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.config.refresh_token_expire_days)
        to_encode.update({"exp": int(expire.timestamp()), "type": "refresh"})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def check_refresh_token(self, token: str) -> dict[str, str]:
        try:
            data: dict[str, str] = jwt.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
            return data

        except ExpiredSignatureError as error:
            raise TokenExpiredException() from error

        except JWTError as error:
            raise NoJwtException() from error

    def get_uuid_from_token(
            self,
            token: Optional[str] = None,
            payload: Optional[dict[str, str]] = None,
    ) -> str:
        if not all([token, payload]):
            raise NotTokenDataError()

        if not payload and isinstance(token, str):
            payload = self.check_refresh_token(token)

        if not payload:
            raise NotTokenDataError()

        uuid_id: str = payload["sub"]
        if not uuid_id:
            raise NoJwtException()

        return uuid_id

    def check_expire_refresh_token(self, token: str) -> str:
        payload = self.check_refresh_token(token)
        expire: str = payload["exp"]

        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.utcnow()):
            raise TokenExpiredException()

        return self.get_uuid_from_token(payload=payload)

    def get_access_token(self, request: Request) -> str:
        token = request.cookies.get("user_access_token")
        if not token:
            raise TokenNotFound()

        return token

    def get_refresh_token(self, request: Request) -> str:
        token = request.cookies.get("user_refresh_token")
        if not token:
            raise TokenNotFound()

        return token

    def set_access_token(self, response: Response, uuid_id: uuid.UUID) -> None:
        access_token = self.create_access_token({"sub": uuid_id})
        response.set_cookie(
            key=self.config.cookie.access_key,
            value=access_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
        )

    def set_refresh_token(self, response: Response, uuid_id: uuid.UUID) -> None:
        refresh_token = self.create_refresh_token({"sub": uuid_id})
        response.set_cookie(
            key=self.config.cookie.refresh_key,
            value=refresh_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
        )

    def delete_access_token(self, response: Response) -> None:
        response.delete_cookie(self.config.cookie.access_key)

    def delete_refresh_token(self, response: Response) -> None:
        response.delete_cookie(self.config.cookie.refresh_key)
