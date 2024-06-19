from pathlib import Path

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)


class LocalStorage(AbstractStorageService):
    # TMP_BUCKET = "/tmp/codeflix-storage"
    TMP_BUCKET = "tmp/codeflix-storage"

    def __init__(self, bucket: str = TMP_BUCKET):
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(self, file_path: str, content: bytes, content_type: str):
        full_path = self.bucket / file_path

        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)

        with open(full_path, "wb") as file:
            file.write(content)
