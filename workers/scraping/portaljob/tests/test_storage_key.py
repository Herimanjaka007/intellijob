from datetime import datetime
from portaljob.storage_key import build_storage_key


def test_format():
    fetched_at = datetime(2026, 9, 4)
    key = build_storage_key("portaljob", "abc123", "json", fetched_at)
    assert key == "raw/portaljob/2026/09/04/abc123.json"
