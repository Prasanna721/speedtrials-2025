import pandas as pd
import logging
from pathlib import Path
from sqlalchemy import Engine

from .database import execute_query
from .schema import MATERIALIZED_VIEW_QUERY

def clean_dataframe(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.upper()
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def load_csv_to_db(engine: Engine, table_name: str, file_path: Path, date_columns: list):
    try:
        df = pd.read_csv(file_path, low_memory=False, encoding='utf-8')
        df_cleaned = clean_dataframe(df, date_columns)
        
        logging.info(f"Loading {len(df_cleaned)} rows into table '{table_name}'...")
        df_cleaned.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False,
            chunksize=10000 
        )
        logging.info(f"Successfully loaded '{table_name}'.")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Failed to load data for table '{table_name}'. Error: {e}")
        raise

def process_and_load_data(engine: Engine, data_path: Path, table_schemas: dict):
    for table_name, schema in table_schemas.items():
        file_path = data_path / schema["file_name"]
        load_csv_to_db(
            engine=engine,
            table_name=table_name,
            file_path=file_path,
            date_columns=schema["date_columns"]
        )

def create_materialized_view(engine: Engine):
    logging.info("Creating materialized view: 'clean_violations'...")
    execute_query(engine, MATERIALIZED_VIEW_QUERY)
    logging.info("'clean_violations' view created successfully.")