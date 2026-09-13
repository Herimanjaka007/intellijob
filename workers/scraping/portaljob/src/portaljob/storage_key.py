from datetime import datetime


def build_storage_key(
    source: str, content_hash: str, extension: str, fetched_at: datetime
) -> str:
    """
    Construit la clé de stockage MinIO.
    Format : raw/{source}/{yyyy}/{mm}/{dd}/{content_hash}.{extension}
    """
    return f"raw/{source}/{fetched_at:%Y}/{fetched_at:%m}/{fetched_at:%d}/{content_hash}.{extension}"
