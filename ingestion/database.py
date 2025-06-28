from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

from .config import settings

def get_engine() -> Engine:
    try:
        engine = create_engine(settings.DB_URL, pool_pre_ping=True)
        with engine.connect() as connection:
            logging.info(f"Successfully connected to the database: {settings.DB_TYPE}")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Database connection failed for {settings.DB_TYPE}: {e}")
        raise

def execute_query(engine: Engine, query: str):
    try:
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS clean_violations;"))
            connection.execute(text(query))
            connection.commit()
        logging.info("Successfully executed query.")
    except SQLAlchemyError as e:
        logging.error(f"Query execution failed: {e}")
        raise