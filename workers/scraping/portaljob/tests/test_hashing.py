from portaljob.hashing import compute_content_hash


def test_deterministic():
    content = b'{"title": "Developpeur Python"}'
    assert compute_content_hash(content) == compute_content_hash(content)


def test_differs_for_different_content():
    assert compute_content_hash(b"A") != compute_content_hash(b"B")
