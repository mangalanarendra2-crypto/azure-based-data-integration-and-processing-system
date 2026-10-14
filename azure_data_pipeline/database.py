"""Load cleaned data into Azure SQL Database (or a local SQLite file as fallback)."""
import logging

import pandas as pd
from sqlalchemy import create_engine, text

import config

log = logging.getLogger(__name__)


def get_engine():
    if config.USE_AZURE_SQL:
        log.info("Database: Azure SQL")
        return create_engine(config.SQL_CONNECTION_URL, fast_executemany=True)
    log.info("Database: local SQLite (%s)", config.LOCAL_DB_URL)
    return create_engine(config.LOCAL_DB_URL)


def load(df: pd.DataFrame, table: str = config.TARGET_TABLE) -> int:
    engine = get_engine()
    df.to_sql(table, engine, if_exists="append", index=False)
    log.info("Loaded %d rows into '%s'", len(df), table)
    return len(df)


def summary_by_month(table: str = config.TARGET_TABLE) -> pd.DataFrame:
    """Simple analytics query to prove the data landed."""
    engine = get_engine()
    query = text(
        f"SELECT order_month, COUNT(*) AS orders, SUM(total_amount) AS revenue "
        f"FROM {table} GROUP BY order_month ORDER BY order_month"
    )
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
