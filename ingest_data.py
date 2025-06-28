import logging
import time

from ingestion.config import settings
from ingestion.database import get_engine
from ingestion.schema import TABLE_SCHEMAS
from ingestion.loader import process_and_load_data, create_materialized_view

def main():
    start_time = time.time()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.info(f"Starting data ingestion process for {settings.DB_TYPE.upper()} database.")

    try:
        engine = get_engine()
        process_and_load_data(engine, settings.DATA_DIR, TABLE_SCHEMAS)
        create_materialized_view(engine)
        
        end_time = time.time()
        duration = end_time - start_time
        
        logging.info(f"Data ingestion process completed successfully in {duration:.2f} seconds.")

    except Exception as e:
        logging.critical(f"A critical error occurred during the ingestion process: {e}")

if __name__ == "__main__":
    main()