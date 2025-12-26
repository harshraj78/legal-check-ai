from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legal-Check AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # We will add LLM API Keys here later
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()