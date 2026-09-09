from portaljob.config import settings


def test_minio_endpoint_url_has_valid_scheme():
    assert settings.minio_endpoint_url.startswith(
        "http://"
    ) or settings.minio_endpoint_url.startswith("https://")
