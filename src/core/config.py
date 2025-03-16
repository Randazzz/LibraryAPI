from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    BOOK_LOAN_DAYS: int = 14
    BOOK_LIMIT_FOR_USER: int = 5

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    LOG_LEVEL: str = "INFO"

    REDIS_URL: str = "redis://localhost:6379"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env.dev", env_prefix="DEV_")


class TestSettings(Settings):
    LOG_LEVEL: str = "WARNING"

    model_config = SettingsConfigDict(env_file=".env.test", env_prefix="TEST_")


test_settings = TestSettings()

settings = Settings()
