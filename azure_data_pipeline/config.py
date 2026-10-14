"""Central configuration. Values come from environment variables / .env file."""
import os

from dotenv import load_dotenv

load_dotenv()

# Azure Blob Storage (data lake): raw -> processed
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
RAW_CONTAINER = os.getenv("RAW_CONTAINER", "raw")
PROCESSED_CONTAINER = os.getenv("PROCESSED_CONTAINER", "processed")

# Azure SQL Database (SQLAlchemy URL), e.g.
# mssql+pyodbc://user:pass@server.database.windows.net:1433/db?driver=ODBC+Driver+18+for+SQL+Server
SQL_CONNECTION_URL = os.getenv("SQL_CONNECTION_URL", "")
TARGET_TABLE = os.getenv("TARGET_TABLE", "sales_clean")

# Local fallbacks so the project runs without any Azure account
LOCAL_STORAGE_DIR = os.getenv("LOCAL_STORAGE_DIR", "local_storage")
LOCAL_DB_URL = os.getenv("LOCAL_DB_URL", "sqlite:///local_warehouse.db")

USE_AZURE_STORAGE = bool(AZURE_STORAGE_CONNECTION_STRING)
USE_AZURE_SQL = bool(SQL_CONNECTION_URL)
