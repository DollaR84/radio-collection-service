from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from passlib.context import CryptContext

from config import SecurityConfig


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
        to_encode.update({"exp": expire})
        token: str = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return token

    def get_email_from_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
            email: str = payload.get("sub")

            if not email:
                return None

            return email
        except JWTError:
            return None
