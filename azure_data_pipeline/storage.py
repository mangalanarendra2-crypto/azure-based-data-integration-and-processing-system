"""Blob storage helper. Uses Azure Blob Storage if configured, else the local disk."""
import logging
from pathlib import Path

import config

log = logging.getLogger(__name__)


class BlobStorage:
    def __init__(self):
        self.use_azure = config.USE_AZURE_STORAGE
        if self.use_azure:
            from azure.storage.blob import BlobServiceClient

            self.client = BlobServiceClient.from_connection_string(
                config.AZURE_STORAGE_CONNECTION_STRING
            )
            log.info("Storage: Azure Blob Storage")
        else:
            self.root = Path(config.LOCAL_STORAGE_DIR)
            log.info("Storage: local folder '%s' (Azure not configured)", self.root)

    def upload(self, container: str, blob_name: str, data: bytes) -> str:
        if self.use_azure:
            cc = self.client.get_container_client(container)
            if not cc.exists():
                cc.create_container()
            cc.upload_blob(name=blob_name, data=data, overwrite=True)
        else:
            path = self.root / container / blob_name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        log.info("Uploaded %s/%s (%d bytes)", container, blob_name, len(data))
        return f"{container}/{blob_name}"

    def download(self, container: str, blob_name: str) -> bytes:
        if self.use_azure:
            return self.client.get_blob_client(container, blob_name).download_blob().readall()
        return (self.root / container / blob_name).read_bytes()

    def list_blobs(self, container: str) -> list[str]:
        if self.use_azure:
            return [b.name for b in self.client.get_container_client(container).list_blobs()]
        base = self.root / container
        if not base.exists():
            return []
        return sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file())
