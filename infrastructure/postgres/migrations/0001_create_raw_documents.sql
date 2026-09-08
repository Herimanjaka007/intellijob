CREATE TABLE IF NOT EXISTS raw_documents (
    id              BIGSERIAL PRIMARY KEY,
    source          TEXT NOT NULL,
    url             TEXT NOT NULL,
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    content_type    TEXT NOT NULL,
    http_status     INTEGER NOT NULL,
    content_hash    TEXT NOT NULL,
    storage_key     TEXT NOT NULL
);

-- Accélère les recherches par source (ex: "toutes les collectes PortalJob")
CREATE INDEX IF NOT EXISTS idx_raw_documents_source ON raw_documents (source);

-- Accélère les recherches par URL (ex: "historique des collectes d'une offre donnée")
CREATE INDEX IF NOT EXISTS idx_raw_documents_url ON raw_documents (url);

-- Accélère la détection de contenu déjà stocké (évite de re-uploader dans MinIO)
CREATE INDEX IF NOT EXISTS idx_raw_documents_content_hash ON raw_documents (content_hash);