import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

NEONDB = "neon"
SQLITE = "sqlite"

class Config:
    DB_TYPE = SQLITE
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

class SQLiteConfig(Config):
    DB_URL = f"sqlite:///{Config.BASE_DIR / 'water_data.db'}"

class NeonDBConfig(Config):
    DB_URL = os.getenv("NEON_DB_URL")
    if not DB_URL:
        raise ValueError("NEON_DB_URL environment variable not set for NeonDB configuration.")

def get_config():
    if Config.DB_TYPE == "neon":
        return NeonDBConfig()
    return SQLiteConfig()

settings = get_config()