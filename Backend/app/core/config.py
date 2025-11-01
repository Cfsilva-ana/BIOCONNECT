from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "BIOCONNECT 2050"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    MONGO_URI: str
    MONGO_DB: str
    
    SECRET_KEY: str = "bioconnect2050secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Thresholds para alertas
    HEART_RATE_HIGH: int = 120
    HEART_RATE_LOW: int = 50
    TEMPERATURE_HIGH: float = 37.5
    
    class Config:
        env_file = "env/.env"

settings = Settings()