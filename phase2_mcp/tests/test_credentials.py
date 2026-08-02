from mcpserver import credentials


def test_hash_token_is_stable_hex64():
    token = "irgendein-token-wert"
    first = credentials.hash_token(token)
    second = credentials.hash_token(token)
    assert first == second
    assert len(first) == 64
    assert all(c in "0123456789abcdef" for c in first)
