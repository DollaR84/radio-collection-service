from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError, ExpiredSignatureError

from passlib.context import CryptContext

from config import SecurityConfig

from .exceptions import NotTokenDataError, NoJwtException, TokenExpiredException, TokenNotFound


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class SecurityTool:
    __slots__ = ("config", "pwd_context", "request", "response",)

    def __init__(self, config: SecurityConfig, request: Request, response: Response):
        self.config: SecurityConfig = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self.request = request
        self.response = response

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

    def get_access_token(self) -> str:
        try:
            token = self.get_token_from_header()
        except Exception:
            token = self.get_token_from_cookie()

        return token

    def get_token_from_header(self, token: str = Depends(oauth2_scheme)) -> str:
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
        access_token = self.create_access_token({"sub": uuid_id})
        self.response.set_cookie(
            key=self.config.cookie.access_key,
            value=access_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
        )

        return access_token

    def set_refresh_token(self, uuid_id: uuid.UUID) -> str:
        refresh_token = self.create_refresh_token({"sub": uuid_id})
        self.response.set_cookie(
            key=self.config.cookie.refresh_key,
            value=refresh_token,
            httponly=self.config.cookie.httponly,
            secure=self.config.cookie.secure,
            samesite=self.config.cookie.samesite,
        )

        return refresh_token

    def delete_access_token(self) -> None:
        self.response.delete_cookie(self.config.cookie.access_key)

    def delete_refresh_token(self) -> None:
        self.response.delete_cookie(self.config.cookie.refresh_key)
