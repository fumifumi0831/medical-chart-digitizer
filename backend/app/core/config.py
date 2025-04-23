import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API related
    API_V1_STR: str = "/api/v1"
    API_KEY: str = os.getenv("API_KEY", "development_api_key")
    
    # CORS allowed origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend
        "http://localhost:8000",  # Backend (for docs)
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # GCS
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "medical-charts-dev")
    USE_MINIO: bool = os.getenv("USE_MINIO", "False").lower() == "true"
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_CONTENT_TYPES: List[str] = ["image/jpeg", "image/png"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
