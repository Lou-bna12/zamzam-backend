import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ZamZam API"

    # --- DATABASE ---
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "loubna")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "loubna12")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "zamzam")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- SECURITY ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "MON_SUPER_SECRET_123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
