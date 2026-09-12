from dataclasses import dataclass
from datetime import datetime

import psycopg

from portaljob.config import settings


@dataclass
class RawDocumentMetadata:
    source: str
    url: str
    fetched_at: datetime
    content_type: str
    http_status: int
    content_hash: str
    storage_key: str


def insert_raw_document(doc: RawDocumentMetadata) -> None:
    with psycopg.connect(settings.postgres_dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO raw_documents
                    (source, url, fetched_at, content_type, http_status, content_hash, storage_key)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    doc.source,
                    doc.url,
                    doc.fetched_at,
                    doc.content_type,
                    doc.http_status,
                    doc.content_hash,
                    doc.storage_key,
                ),
            )
        conn.commit()


def document_exists(url: str, source: str) -> bool:
    """Vérifie si un RAW a déjà été stocké pour cette URL et cette source."""
    with psycopg.connect(settings.postgres_dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM raw_documents WHERE url = %s AND source = %s LIMIT 1",
                (url, source),
            )
            return cur.fetchone() is not None
