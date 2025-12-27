from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legal-Check AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Defaults for local dev, will be overridden by .env in Docker
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "legal_ai"
    DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str) and v:
            return v
        
        # Build the DSN from components if DATABASE_URL isn't provided directly
        return str(PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_SERVER"],
            port=5432,
            path=f"{info.data['POSTGRES_DB']}",
        ))


    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()