from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/daniellife"

    # JWT
    SECRET_KEY: str = "change-me-in-production-use-32-chars-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    ADMIN_EMAIL: str = "admin@daniellife.com"  # only this email can log in

    # ITIS proxy
    ITIS_BASE_URL: str = "https://itisweb2.itis.org.tw/ITIS_Publish/ITISNews_New_One.asp"

    # GitHub Models (OpenAI-compatible inference)
    GITHUB_TOKEN: str = ""
    GITHUB_MODELS_MODEL: str = "gpt-4o"

    # Frontend origin (CORS)
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
