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
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(slots=True)
class RedisConfig:
    host: str = os.environ["REDIS_PORT"]
    port: int = int(os.environ["REDIS_PORT"])


@dataclass(slots=True)
class APIConfig:
    debug: bool = os.environ.get("FASTAPI_DEBUG", "false").lower() == "true"
    upload_folder: str = os.environ["FASTAPI_UPLOAD_FOLDER"]


@dataclass(slots=True)
class SecurityConfig:
    algorithm: str = os.environ["ALGORITHM"]
    secret_key: str = os.environ["SECRET_KEY"]

    access_token_expire_minutes: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    refresh_token_expire_minutes: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 15))


@dataclass(slots=True)
class GoogleConfig:
    google_client_name: str = os.environ["GOOGLE_CLIENT_NAME"]
    google_client_id: str = os.environ["GOOGLE_CLIENT_ID"]
    google_client_secret: str = os.environ["GOOGLE_CLIENT_SECRET"]
    google_redirect_url: str = os.environ["GOOGLE_REDIRECT_URL"]


@dataclass(slots=True)
class ParserConfig:
    max_workers: int = 4
    batch_size: int = 25
    default_sleep_timeout: float = 0.5


@dataclass(slots=True)
class WorkerConfig:
    redis_database: int = int(os.environ["REDIS_DATABASE"])
    handle_signals: bool = os.environ.get("HANDLE_SIGNALS", "false").lower() == "true"
    health_check_interval: int = int(os.environ["HEALTH_CHECK_INTERVAL"])
    max_jobs: int = int(os.environ["MAX_JOBS"])
    job_timeout: int = int(os.environ["JOB_TIMEOUT"])


@dataclass(slots=True)
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    api: APIConfig = field(default_factory=APIConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    google: GoogleConfig = field(default_factory=GoogleConfig)
    parser: ParserConfig = field(default_factory=ParserConfig)
    worker: WorkerConfig = field(default_factory=WorkerConfig)
