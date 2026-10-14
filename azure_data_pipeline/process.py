"""Processing: read raw blobs, clean/transform with pandas, write to the processed zone."""
import io
import logging

import pandas as pd

import config
from storage import BlobStorage

log = logging.getLogger(__name__)


def read_raw(storage: BlobStorage, blob_name: str) -> pd.DataFrame:
    data = storage.download(config.RAW_CONTAINER, blob_name)
    if blob_name.lower().endswith(".json"):
        return pd.read_json(io.BytesIO(data))
    return pd.read_csv(io.BytesIO(data))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise columns, remove bad rows, derive new fields."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["order_id", "quantity", "unit_price"])

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]

    df["customer"] = df["customer"].fillna("Unknown").str.strip().str.title()
    df["product"] = df["product"].str.strip().str.title()
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")

    log.info("Cleaned data: %d -> %d rows", before, len(df))
    return df.reset_index(drop=True)


def write_processed(storage: BlobStorage, df: pd.DataFrame, blob_name: str) -> str:
    out_name = blob_name.rsplit(".", 1)[0] + "_clean.csv"
    return storage.upload(
        config.PROCESSED_CONTAINER, out_name, df.to_csv(index=False).encode("utf-8")
    )
