"""Orchestrator: ingest -> store raw -> process -> store processed -> load to SQL.

Usage:
    python pipeline.py --file sample_data/sales.csv
    python pipeline.py --api https://example.com/data.json --name my_api
"""
import argparse
import logging

import database
import ingest
import process
from storage import BlobStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pipeline")


def run(file: str | None = None, api: str | None = None, name: str = "api_data") -> None:
    storage = BlobStorage()

    # 1. Ingest -> raw zone
    if file:
        raw_ref = ingest.ingest_file(storage, file)
    elif api:
        raw_ref = ingest.ingest_api(storage, api, name)
    else:
        raise SystemExit("Provide --file or --api")

    # 2. Process raw -> clean
    blob_name = raw_ref.split("/", 1)[1]
    df = process.clean(process.read_raw(storage, blob_name))

    # 3. Processed zone + warehouse
    process.write_processed(storage, df, blob_name)
    database.load(df)

    # 4. Quick report
    log.info("Monthly summary:\n%s", database.summary_by_month().to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Azure data integration pipeline")
    ap.add_argument("--file", help="local CSV/JSON file to ingest")
    ap.add_argument("--api", help="REST API URL returning JSON records")
    ap.add_argument("--name", default="api_data", help="dataset name for API ingestion")
    args = ap.parse_args()
    run(args.file, args.api, args.name)
