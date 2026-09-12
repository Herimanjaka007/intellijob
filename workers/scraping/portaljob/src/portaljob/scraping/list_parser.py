import json


def extract_annonce_urls(raw_body: str) -> list[str]:
    """
    Extrait les identifiants annonce_url depuis une réponse brute de liste.
    Ne transforme PAS le contenu métier — lecture minimale pour piloter le scraping du détail.
    """
    data = json.loads(raw_body)

    urls: list[str] = []
    for section in ("annonces_prime", "annonces_partenaires"):
        for annonce in data.get(section) or []:
            if annonce.get("annonce_url"):
                urls.append(annonce["annonce_url"])

    annonces_page = data.get("annonces") or {}
    for annonce in annonces_page.get("data") or []:
        if annonce.get("annonce_url"):
            urls.append(annonce["annonce_url"])

    return urls
