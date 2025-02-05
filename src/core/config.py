from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    BOOK_LOAN_DAYS: int = 14

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env.dev"


settings = Settings()
