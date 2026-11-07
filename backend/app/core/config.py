from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "Distributed Commerce API"
    database_url: str = "postgresql+psycopg://commerce:commerce@db:5432/commerce"
    redis_url: str = "redis://redis:6379/0"
    jwt_secret: str = "change-this-in-production"
    access_token_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
