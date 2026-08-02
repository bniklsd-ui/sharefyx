from mcpserver.auth import Principal


def test_principal_repr_hides_token():
    principal = Principal(space="nikinger", token_hash="0123456789abcdef")
    text = repr(principal)
    assert "0123456789abcdef" not in text
    assert "01234567" in text
