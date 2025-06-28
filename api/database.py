from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = "sqlite:///./water_data.db"

if not os.path.exists(DATABASE_URL.replace("sqlite:///", "")):
    raise FileNotFoundError(
        "Database file 'water_data.db' not found. "
        "Please run the ingestion script first."
    )

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()