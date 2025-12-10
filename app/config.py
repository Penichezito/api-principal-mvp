from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import json
import os

# Detecta se está rodando em Docker
IS_DOCKER = os.path.exists("/.dockerenv")

class Settings(BaseSettings):
    # Database - Detecta automaticamente local vs Docker
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@db:5432/freela_facility" 
        if IS_DOCKER 
        else "postgresql://postgres:postgres@localhost:5432/freela_facility"
    )
    
    # JWT
    SECRET_KEY: str = "freelafacility"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    
    # API Secundária
    SECONDARY_API_URL: str = (
        "http://api-secundaria:5000"
        if IS_DOCKER
        else "http://localhost:5000"
    )
    
    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://frontend:3000"]
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_origins(cls, v):
        """Parse ALLOWED_ORIGINS se vier como string JSON ou CSV"""
        if isinstance(v, str):
            # Tenta parsear como JSON
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Se não for JSON, tenta como CSV
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()