import os
from datetime import datetime, timezone

from portaljob.scraping.client import (
    get_session,
    fetch_annonces_raw,
    fetch_annonce_detail_raw,
)
from portaljob.scraping.list_parser import extract_annonce_urls
from portaljob.hashing import compute_content_hash
from portaljob.storage_key import build_storage_key
from portaljob.storage.object_store import upload_raw_content
from portaljob.storage.metadata_repo import (
    insert_raw_document,
    document_exists,
    RawDocumentMetadata,
)
from portaljob.logger import get_logger

SOURCE_LISTE = "portaljob_liste"
SOURCE_DETAIL = "portaljob_detail"
MAX_PAGES = int(os.environ.get("MAX_PAGES", "1"))

logger = get_logger(__name__)


def _store_raw(
    source: str, url: str, body: str, content_type: str, http_status: int
) -> None:
    fetched_at = datetime.now(timezone.utc)
    content_hash = compute_content_hash(body.encode("utf-8"))
    storage_key = build_storage_key(source, content_hash, "json", fetched_at)

    upload_raw_content(storage_key, body, content_type)
    insert_raw_document(
        RawDocumentMetadata(
            source=source,
            url=url,
            fetched_at=fetched_at,
            content_type=content_type,
            http_status=http_status,
            content_hash=content_hash,
            storage_key=storage_key,
        )
    )
    logger.info(
        f"RAW stocké | source={source} | status={http_status} | key={storage_key}"
    )


def _scrape_listing(session) -> list[str]:
    """Phase 1 : scrape toutes les pages de liste, retourne les annonce_url uniques trouvées."""
    all_urls: list[str] = []

    for page in range(1, MAX_PAGES + 1):
        logger.info(f"Scraping liste - page {page}/{MAX_PAGES}")
        raw = fetch_annonces_raw(session, {"page": page})
        page_url = (
            f"https://www.portaljob-madagascar.com/api/emploi/annonces?page={page}"
        )

        _store_raw(SOURCE_LISTE, page_url, raw.body, raw.content_type, raw.http_status)

        all_urls.extend(extract_annonce_urls(raw.body))

    # Déduplication des URLs trouvées sur plusieurs pages/sections
    return list(dict.fromkeys(all_urls))


def _scrape_details(session, annonce_urls: list[str]) -> None:
    """Phase 2 : scrape le détail de chaque annonce non encore connue."""
    for annonce_url in annonce_urls:
        detail_url = f"https://www.portaljob-madagascar.com/api/emploi/detail-offre/{annonce_url}"

        if document_exists(detail_url, SOURCE_DETAIL):
            logger.info(f"Détail déjà connu, skip | {annonce_url}")
            continue

        logger.info(f"Scraping détail | {annonce_url}")
        raw = fetch_annonce_detail_raw(session, annonce_url)
        _store_raw(
            SOURCE_DETAIL, detail_url, raw.body, raw.content_type, raw.http_status
        )


def main() -> None:
    logger.info("Connexion à PortalJob...")
    session = get_session()

    annonce_urls = _scrape_listing(session)
    logger.info(f"{len(annonce_urls)} annonces uniques trouvées")

    _scrape_details(session, annonce_urls)

    logger.info("Terminé.")


if __name__ == "__main__":
    main()
