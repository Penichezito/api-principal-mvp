from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/freela_facility"
    
    # JWT
    SECRET_KEY: str = "freela_facility"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    
    # API Secundária
    SECONDARY_API_URL: str = "http://api-secundaria:5000"
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://frontend:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()