from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Le .env se trouve à la racine du monorepo, pas dans ce worker
ENV_FILE = Path(__file__).resolve().parents[5] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    postgres_host: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_raw: str
    minio_secure: bool = False

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def minio_endpoint_url(self) -> str:
        scheme = "https" if self.minio_secure else "http"
        return f"{scheme}://{self.minio_endpoint}"


settings = Settings()  # type: ignore[call-arg]
print(settings)
