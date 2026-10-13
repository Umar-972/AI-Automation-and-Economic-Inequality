from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "QuantChronicle"
    database_url: str = "postgresql+psycopg://quantchronicle:quantchronicle@localhost:5432/quantchronicle"
    jwt_secret_key: str = "CHANGE-ME-IN-PRODUCTION-USE-A-LONG-RANDOM-SECRET"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    default_timezone: str = "UTC"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
