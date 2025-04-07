from dataclasses import dataclass, field
import os


@dataclass(slots=True)
class DBConfig:
    username: str = os.environ["POSTGRES_USER"]
    password: str = os.environ["POSTGRES_PASSWORD"]
    db_name: str = os.environ["POSTGRES_DB"]
    host: str = os.environ["POSTGRES_HOST"]
    port: int = int(os.environ["POSTGRES_PORT"])

    debug: bool = os.environ.get("SQLALCHEMY_DEBUG", "false").lower() == "true"

    @property
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(slots=True)
class APIConfig:
    debug: bool = os.environ.get("FASTAPI_DEBUG", "false").lower() == "true"
    upload_folder: str = os.environ["FASTAPI_UPLOAD_FOLDER"]


@dataclass(slots=True)
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    api: APIConfig = field(default_factory=APIConfig)
