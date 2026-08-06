from authserver import templates


def test_error_page_escapes_message():
    html = templates.render_error_page("<script>alert(1)</script>")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_login_form_escapes_request_id():
    html = templates.render_login_form('">injected<')
    assert '">injected<' not in html
    assert "&quot;&gt;injected&lt;" in html


def test_login_form_carries_request_id_and_action_choices():
    html = templates.render_login_form("abc123")
    assert 'name="request_id" value="abc123"' in html
    assert 'name="action" value="allow"' in html
    assert 'name="action" value="deny"' in html
    assert 'action="/oauth/authorize"' in html
    assert 'method="post"' in html


def test_login_form_has_no_javascript_no_cookie_hint():
    """[2026-08-06] Vorher `test_..._no_stylesheet_...`: pinnte "kein <link>" als Absicht — seit
    dem Nikinger-Fund "alte UI beim Connector-Neuanmelden" lädt die Seite `/ui/static/app.css`
    (reine CSS-Wiederverwendung, kein Python-Import, siehe `templates.py`-Moduldocstring). Kein
    `<script>` bleibt bewusst bestehen: dieser Flow ist sicherheitskritischer als `webui`s
    Seiten (P5-G)."""
    html = templates.render_login_form("abc123")
    assert "<script" not in html
    assert "document.cookie" not in html


def test_login_form_loads_the_shared_stylesheet_via_link_not_inline_style():
    html = templates.render_login_form("abc123")
    assert '<link rel="stylesheet" href="/ui/static/app.css">' in html
    assert "style=" not in html
