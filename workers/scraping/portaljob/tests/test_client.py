import httpx
from portaljob.scraping.client import fetch_annonces_raw, Session


def test_fetch_annonces_raw_returns_raw_body(monkeypatch):
    def mock_post(self, url, headers=None, json=None):
        return httpx.Response(
            status_code=200,
            headers={"content-type": "application/json"},
            content=b'{"annonces": {"data": []}}',
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx.Client, "post", mock_post)

    session = Session(cookie_str="XSRF-TOKEN=abc", xsrf_token="abc")
    result = fetch_annonces_raw(session, {"page": 1})

    assert result.http_status == 200
    assert result.body == '{"annonces": {"data": []}}'
