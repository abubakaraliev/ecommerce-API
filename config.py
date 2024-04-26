from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DB_HOST:str
    DB_NAME:str
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_PORT:int
    
    class Config:
        env_file:str = ".env"
        extra = "allow"
        
@lru_cache
def get_settings() -> Settings:
    return Settings()

