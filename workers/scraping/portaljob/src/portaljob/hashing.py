import hashlib


def compute_content_hash(content: bytes) -> str:
    """Calcule le SHA-256 d'un contenu brut."""
    return hashlib.sha256(content).hexdigest()
