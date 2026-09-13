from dataclasses import dataclass
from urllib.parse import unquote

import httpx

BASE_URL = "https://www.portaljob-madagascar.com"
LISTE_URL = f"{BASE_URL}/emploi/liste/secteur/informatique-web"
API_URL = f"{BASE_URL}/api/emploi/annonces"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class Session:
    cookie_str: str
    xsrf_token: str


@dataclass
class RawApiResponse:
    url: str
    http_status: int
    content_type: str
    body: str


def get_session() -> Session:
    """Récupère les cookies (dont XSRF-TOKEN) en visitant la page des offres."""
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(LISTE_URL)
        response.read()  # consomme la réponse, jamais sauvegardée

        cookies = response.cookies
        cookie_str = "; ".join(f"{name}={value}" for name, value in cookies.items())
        xsrf_token = unquote(cookies.get("XSRF-TOKEN", "") or "")

        return Session(cookie_str=cookie_str, xsrf_token=xsrf_token)


def fetch_annonces_raw(session: Session, payload: dict) -> RawApiResponse:
    """Appelle l'API annonces, retourne la réponse brute sans la parser."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": session.xsrf_token,
        "Cookie": session.cookie_str,
        "Referer": LISTE_URL,
        "Origin": BASE_URL,
        "User-Agent": USER_AGENT,
    }

    with httpx.Client() as client:
        response = client.post(API_URL, headers=headers, json=payload)

        return RawApiResponse(
            url=API_URL,
            http_status=response.status_code,
            content_type=response.headers.get("content-type", "application/json"),
            body=response.text,
        )


def fetch_annonce_detail_raw(session: Session, annonce_url: str) -> RawApiResponse:
    """Récupère le détail d'une annonce (description, compétences, requis...)."""
    headers = {
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": session.xsrf_token,
        "Cookie": session.cookie_str,
        "Referer": LISTE_URL,
        "Origin": BASE_URL,
        "User-Agent": USER_AGENT,
    }

    url = f"{BASE_URL}/api/emploi/detail-offre/{annonce_url}"

    with httpx.Client() as client:
        response = client.post(url, headers=headers)

        return RawApiResponse(
            url=url,
            http_status=response.status_code,
            content_type=response.headers.get("content-type", "application/json"),
            body=response.text,
        )


if __name__ == "__main__":
    session = get_session()
    # payload in portaljob
    payload = {"page": 1, "secteurs": [7]}
    raw_response = fetch_annonces_raw(session, payload)
    print(raw_response)
