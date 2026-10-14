"""Ingestion: pull data from a file or REST API and land it, untouched, in the raw zone."""
import logging
from datetime import datetime, timezone
from pathlib import Path

import requests

import config
from storage import BlobStorage

log = logging.getLogger(__name__)


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def ingest_file(storage: BlobStorage, path: str) -> str:
    """Upload a local CSV/JSON file to the raw container."""
    p = Path(path)
    blob_name = f"{p.stem}/{_stamp()}_{p.name}"
    return storage.upload(config.RAW_CONTAINER, blob_name, p.read_bytes())


def ingest_api(storage: BlobStorage, url: str, name: str = "api_data") -> str:
    """Fetch JSON from a REST endpoint and upload to the raw container."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    blob_name = f"{name}/{_stamp()}_{name}.json"
    return storage.upload(config.RAW_CONTAINER, blob_name, resp.content)
