# intellijob

Plateforme de Job Market Intelligence pour Madagascar.

## État actuel

Incrément 1 : `PortalJob → Scraper → Raw Storage (MinIO + PostgreSQL)`

## Démarrer l'infrastructure locale

\`\`\`bash
cp .env.example .env
docker compose up -d
docker compose ps
\`\`\`