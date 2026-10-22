import os

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

DEFAULT_SECRET_KEY = "change-me-in-production-use-32-chars-min"


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/daniellife"

    @field_validator('DATABASE_URL')
    @classmethod
    def fix_db_url(cls, v: str) -> str:
        if v.startswith('mysql://'):
            return v.replace('mysql://', 'mysql+pymysql://', 1)
        return v

    # JWT
    SECRET_KEY: str = Field(default=DEFAULT_SECRET_KEY, validate_default=True)

    @field_validator('SECRET_KEY')
    @classmethod
    def check_secret_key(cls, v: str) -> str:
        # On Railway, refuse to start with a missing/default/weak key (JWTs would be forgeable)
        if os.getenv('RAILWAY_ENVIRONMENT') and (v == DEFAULT_SECRET_KEY or len(v) < 32):
            raise ValueError('SECRET_KEY must be set to a random value of at least 32 chars in production')
        return v

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    ADMIN_EMAIL: str = "admin@daniellife.com"  # only this email can log in

    # ITIS proxy
    ITIS_BASE_URL: str = "https://itisweb2.itis.org.tw/ITIS_Publish/ITISNews_New_One.asp"

    # AI Chat provider: "gemini" | "groq" | "github"
    AI_PROVIDER: str = "gemini"

    # Google Gemini (AI Studio) — gemini-2.0-flash, 1500 req/day free
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Groq — llama-3.3-70b-versatile, 14400 req/day free
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # GitHub Models — gpt-4o, 150 req/day free
    GITHUB_TOKEN: str = ""
    GITHUB_MODELS_MODEL: str = "gpt-4o"

    # Frontend origin (CORS)
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # Notion integration (paper notes sync)
    NOTION_TOKEN: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
