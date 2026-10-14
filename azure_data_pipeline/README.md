# Azure-Based Data Integration and Processing System

A simple ETL pipeline built around Azure services.

```
 CSV / REST API ──► Ingest ──► Blob Storage (raw)
                                   │
                              Process (pandas)
                                   │
                    ┌──────────────┴──────────────┐
          Blob Storage (processed)          Azure SQL Database
```

## Files
| File | Purpose |
|---|---|
| `config.py` | Settings from environment variables |
| `storage.py` | Azure Blob Storage wrapper (local-folder fallback) |
| `ingest.py` | Pull from file/API into the raw container |
| `process.py` | Clean, validate, transform data |
| `database.py` | Load into Azure SQL (SQLite fallback) + summary query |
| `pipeline.py` | Orchestrates the whole flow (CLI) |
| `function_app.py` | Optional Azure Functions timer trigger |
| `sales.csv` | Sample data with deliberate errors (duplicates, bad dates, negatives) |

## Run locally (no Azure needed)
```bash
pip install -r requirements.txt
python pipeline.py --file sales.csv
```
Output goes to `local_storage/` and `local_warehouse.db`.

## Run against Azure
1. Create a Storage Account and an Azure SQL Database.
2. Copy `.env.example` to `.env` and fill in the connection string and SQL URL.
3. Run `python pipeline.py --file sales.csv` again.

## Azure setup (CLI)
```bash
az group create -n rg-dataflow -l centralindia
az storage account create -n <uniquename> -g rg-dataflow -l centralindia --sku Standard_LRS
az storage account show-connection-string -n <uniquename> -g rg-dataflow
```

## Ideas to extend
Azure Data Factory orchestration, Event Grid triggers on new blobs, Databricks/Synapse for larger data, Key Vault for secrets, Power BI on top of the SQL table.
