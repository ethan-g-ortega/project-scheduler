from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openweather_api_key: str
    weather_timeout_ms: int = 2000
    weather_cache_ttl: int = 120 #in seconds
    class Config:
        env_file = ".env"

settings = Settings()