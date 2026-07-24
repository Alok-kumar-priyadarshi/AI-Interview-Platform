"""File storage abstraction.

Provides a provider-independent storage interface with two implementations,
selected by ``STORAGE_PROVIDER`` (docs/08-deployment/environment-variables.md):

* ``local`` — filesystem storage under ``STORAGE_LOCAL_DIR`` (Version 1 default).
* ``s3``    — any S3-compatible service, including Cloudflare R2.

Business services depend on the :class:`StorageProvider` protocol, never on a
concrete backend, so switching to R2 is a configuration change only.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Protocol

from app.core.config import Settings
from app.core.logging import get_logger
from app.exceptions.base import FileUploadError, StorageUnavailableError

logger = get_logger(__name__)


class StorageProvider(Protocol):
    async def save(self, *, key: str, data: bytes, content_type: str) -> str: ...

    async def load(self, *, key: str) -> bytes: ...

    async def delete(self, *, key: str) -> None: ...


class LocalStorage:
    """Filesystem-backed storage. Keys are relative paths under ``base_dir``."""

    def __init__(self, base_dir: str) -> None:
        self._base = Path(base_dir).resolve()

    def _path_for(self, key: str) -> Path:
        # Prevent path traversal: the resolved path must stay under base.
        candidate = (self._base / key).resolve()
        if not str(candidate).startswith(str(self._base)):
            raise FileUploadError("Invalid storage key.")
        return candidate

    async def save(self, *, key: str, data: bytes, content_type: str) -> str:
        def _write() -> str:
            path = self._path_for(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return f"local://{key}"

        return await asyncio.to_thread(_write)

    async def load(self, *, key: str) -> bytes:
        def _read() -> bytes:
            return self._path_for(key).read_bytes()

        try:
            return await asyncio.to_thread(_read)
        except FileNotFoundError as exc:
            raise FileUploadError("Stored file not found.") from exc

    async def delete(self, *, key: str) -> None:
        def _delete() -> None:
            self._path_for(key).unlink(missing_ok=True)

        await asyncio.to_thread(_delete)


class S3Storage:
    """S3-compatible storage (AWS S3 / Cloudflare R2). Lazily imports boto3."""

    def __init__(self, settings: Settings) -> None:
        if not settings.STORAGE_BUCKET:
            raise StorageUnavailableError("STORAGE_BUCKET is not configured.")
        self._settings = settings
        self._bucket = settings.STORAGE_BUCKET
        self._client = None

    def _get_client(self):  # type: ignore[no-untyped-def]
        if self._client is None:
            import boto3

            self._client = boto3.client(
                "s3",
                endpoint_url=self._settings.STORAGE_ENDPOINT,
                region_name=self._settings.STORAGE_REGION,
                aws_access_key_id=self._settings.STORAGE_ACCESS_KEY,
                aws_secret_access_key=self._settings.STORAGE_SECRET_KEY,
            )
        return self._client

    async def save(self, *, key: str, data: bytes, content_type: str) -> str:
        def _put() -> str:
            self._get_client().put_object(
                Bucket=self._bucket, Key=key, Body=data, ContentType=content_type
            )
            return f"s3://{self._bucket}/{key}"

        return await asyncio.to_thread(_put)

    async def load(self, *, key: str) -> bytes:
        def _get() -> bytes:
            obj = self._get_client().get_object(Bucket=self._bucket, Key=key)
            return obj["Body"].read()

        return await asyncio.to_thread(_get)

    async def delete(self, *, key: str) -> None:
        def _del() -> None:
            self._get_client().delete_object(Bucket=self._bucket, Key=key)

        await asyncio.to_thread(_del)


def build_storage(settings: Settings) -> StorageProvider:
    """Factory: return the configured storage provider."""
    if settings.STORAGE_PROVIDER == "s3":
        return S3Storage(settings)
    return LocalStorage(settings.STORAGE_LOCAL_DIR)
