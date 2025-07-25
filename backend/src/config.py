from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from application.types import CheckerType


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    username: str
    password: str
    db_name: str
    host: str
    port: int = 5432
    debug: bool = False

    ssl: bool = False
    url: Optional[str] = None

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        if not 0 < value < 65535:
            raise ValueError("invalid db postgres port")
        return value

    @property
    def uri(self) -> str:
        uri = f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        return self.url if self.url else uri


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str
    port: int = 6379

    url: Optional[str] = None

    @field_validator("port")
    @classmethod
    def validate_port(cls, value: int) -> int:
        if not 0 < value < 65535:
            raise ValueError("invalid redis port")
        return value


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FASTAPI_")

    title: str
    description: str
    version: str
    upload_folder: str
    debug: bool = False

    allow_credentials: bool = True
    allow_origins: list[str] = Field(default_factory=list)
    allow_methods: list[str] = ["GET", "POST"]
    allow_headers: list[str] = ["*"]


class CookieConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="COOKIE_")

    access_key: str
    refresh_key: str
    samesite: Literal["lax", "strict", "none"] | None = "lax"

    httponly: bool = True
    secure: bool = True


class SecurityConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SECURITY_")

    algorithm: str
    secret_key: str

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cookie: CookieConfig = Field(default_factory=CookieConfig)


class ResolverConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RESOLVER_")

    plus: int
    pro: int
    full: int


class GoogleConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GOOGLE_")

    client_name: str
    client_id: str
    client_secret: str
    redirect_url: str


class ParserConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PARSER_")

    max_workers: int = 4
    chunks_count: int = 1000
    batch_size: int = 3000
    default_sleep_timeout: float = 0.5


class WorkerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WORKER_")

    redis_database: int = 0
    handle_signals: bool = False
    health_check_interval: int
    max_jobs: int
    job_timeout: int


class TesterConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TESTER_")

    checker_type: CheckerType
    repeat_count: int
    repeat_timeout: int

    max_concurrent_tasks: int
    batch_size: int
    batch_limit: int

    queue_timeout: float
    update_timeout: float


class AdminConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ADMIN_")

    title: str
    base_url: str
    templates_dir: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DBConfig = Field(default_factory=DBConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    resolver: ResolverConfig = Field(default_factory=ResolverConfig)
    google: GoogleConfig = Field(default_factory=GoogleConfig)
    parser: ParserConfig = Field(default_factory=ParserConfig)
    worker: WorkerConfig = Field(default_factory=WorkerConfig)
    tester: TesterConfig = Field(default_factory=TesterConfig)
    admin: AdminConfig = Field(default_factory=AdminConfig)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
