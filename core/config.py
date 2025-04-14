from authx import AuthXConfig
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

jwt = os.getenv("JWT_SECRET")
db = os.getenv("DATABASE_URL")
if jwt is None or db is None:
    raise ValueError("database url or jwt not in .env")


class Settings(BaseModel):
    # JWT Configuration
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = jwt
    JWT_TOKEN_LOCATION: list = ["headers"]

    # Database Configuration
    DATABASE_URL: str = db


def get_authx_config() -> AuthXConfig:
    settings = Settings()
    return AuthXConfig(
        JWT_ALGORITHM=settings.JWT_ALGORITHM,
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION,
    )


settings = Settings()
authx_config = get_authx_config()
