import json

from portaljob.scraping.list_parser import extract_annonce_urls


def test_extract_from_all_sections():
    raw_body = json.dumps(
        {
            "annonces_prime": [{"annonce_url": "prime-1"}],
            "annonces_partenaires": [{"annonce_url": "partenaire-1"}],
            "annonces": {
                "data": [
                    {"annonce_url": "classique-1"},
                    {"annonce_url": "classique-2"},
                ],
                "links": [],
            },
        }
    )

    urls = extract_annonce_urls(raw_body)

    assert urls == ["prime-1", "partenaire-1", "classique-1", "classique-2"]


def test_extract_ignores_missing_sections():
    raw_body = json.dumps({"annonces": {"data": []}})
    assert extract_annonce_urls(raw_body) == []


def test_extract_skips_annonces_without_url():
    raw_body = json.dumps({"annonces": {"data": [{"annonce_poste": "Sans URL"}]}})
    assert extract_annonce_urls(raw_body) == []
