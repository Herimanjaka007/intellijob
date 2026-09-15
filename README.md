# intellijob

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MinIO](https://img.shields.io/badge/MinIO-latest-C72E49?logo=minio&logoColor=white)](https://min.io/)

**Plateforme de Job Market Intelligence pour Madagascar.**

intellijob collecte et analyse les offres d'emploi IT publiées sur **plusieurs sources** afin de fournir des insights sur **les compétences actuellement demandées** et sur **l'évolution du marché de l'emploi**.

> 🎯 **Mission** — répondre à la question :
> *« Quelles compétences sont actuellement demandées sur le marché IT malgache »*

## À propos

Le marché de l'emploi IT évolue rapidement, et les informations sont dispersées entre de nombreux portails d'emploi. intellijob transforme ces offres brutes en données exploitables :

- **Compétences demandées** — quelles technologies, frameworks et savoir-faire les recruteurs recherchent aujourd'hui ;
- **Évolution du marché** — suivi dans le temps de la demande pour détecter les tendances (langages, métiers, secteurs) ;
- **Aide à la décision** — accompagne un développeur, un étudiant ou un recruteur dans ses choix (formation, reconversion, recrutement).

##  Stack technique

| Brique | Technologie | Rôle |
| --- | --- | --- |
| Infrastructure | Docker Compose | Orchestration de l'environnement local |
| Base de données | PostgreSQL 16 | Métadonnées des documents collectés |
| Stockage objet | MinIO | Stockage des documents bruts (JSON) |
| Worker de collecte | Python 3.13 + [uv](https://docs.astral.sh/uv/) | Scraping multi-sources et pipeline |

## 📦 État actuel

Incrément 1 : `PortalJob → Scraper → Raw Storage (MinIO + PostgreSQL)`

Le pipeline actuel :

1. **collecte** la liste paginée des annonces IT publiées sur **PortalJob Madagascar** ;
2. **récupère** le détail de chaque annonce non encore connue ;
3. **stocke** les documents bruts dans **MinIO** (JSON) et les métadonnées dans **PostgreSQL**, avec **déduplication** par hash de contenu.

##  Démarrage rapide

### Prérequis

- [Docker](https://www.docker.com/) + Docker Compose ;
- [Python 3.13](https://www.python.org/downloads/) ou plus récent ;
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gestionnaire de dépendances et d'environnements virtuels).

### 1. Lancer l'infrastructure (PostgreSQL + MinIO)

Depuis la **racine du dépôt** :

**Linux / macOS :**

```bash
cp .env.example .env
docker compose up -d
docker compose ps
```

**Windows (PowerShell) :**

```powershell
copy .env.example .env
docker compose up -d
docker compose ps
```

PostgreSQL est exposé sur `localhost:5433` et la console MinIO sur <http://localhost:9001>.

### 2. Lancer le worker Python (collecte des offres)

Depuis la **racine du dépôt**, rendez-vous dans le dossier du worker puis lancez la collecte :

**Linux / macOS :**

```bash
cd workers/scraping/portaljob
uv sync
uv run portaljob
```

**Windows (PowerShell) :**

```powershell
cd workers\scraping\portaljob
uv sync
uv run portaljob
```

### 3. Lancer les tests

**Linux / macOS :**

```bash
cd workers/scraping/portaljob
uv run pytest
```

**Windows (PowerShell) :**

```powershell
cd workers\scraping\portaljob
uv run pytest
```

## 📁 Structure du projet

```
intellijob/
├── docker-compose.yml               # Infrastructure locale (PostgreSQL, MinIO)
├── infrastructure/
│   └── postgres/migrations/         # Migrations SQL (création des tables)
├── workers/
│   └── scraping/
│       └── portaljob/               # Worker Python (projet uv)
│           ├── src/portaljob/       # Code source (scraping, stockage…)
│           ├── tests/               # Tests unitaires
│           ├── pyproject.toml       # Dépendances & point d'entrée CLI
│           └── uv.lock              # Verrouillage des dépendances
├── docs/                            # Documentation
└── .env.example                     # Variables d'environnement (modèle)
```

## 🔐 Variables d'environnement

Copiez `.env.example` vers `.env` (voir [Démarrage rapide](#-démarrage-rapide)). Variables principales :

| Variable | Description |
| --- | --- |
| `POSTGRES_HOST` / `POSTGRES_PORT` | Hôte et port PostgreSQL (défaut : `localhost:5433`) |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | Identifiants et base PostgreSQL |
| `MINIO_ENDPOINT` | Endpoint MinIO (ex. `localhost:9000`) |
| `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` | Identifiants MinIO |
| `MINIO_BUCKET_RAW` | Bucket de stockage des documents bruts |
| `MINIO_SECURE` | `true` si MinIO est exposé en HTTPS |
