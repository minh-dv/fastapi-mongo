from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT = 587
    MAIL_SERVER: str
    MAIL_TLS = True
    MAIL_SSL = False
    USE_CREDENTIALS = True

    class Config:
        case_sensitive = True


settings = Settings()



