"""Testet `scripts/serve.py :: main()` — nicht als Subprozess (der würde echt `uvicorn.run()`
aufrufen und blockieren), sondern in-process mit `uvicorn.run` und `load_users` gepatcht.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** `serve.py` verlangt seither immer eine gültige
`OAuthConfig` (kein `oauth=None`-Pfad mehr) — bisher deckte kein Test die Verdrahtung von
`load_settings()`/`load_auth_settings()`/`create_app()` bis zum `uvicorn.run()`-Aufruf ab, beide
Smoke-Skripte bauen `create_app()` direkt und rufen `main()` nie auf. Das nächste `systemctl
restart sharefyx-mcp` wäre sonst der erste echte Test dieser Verdrahtung — zu spät für einen
falschen Parameternamen. `load_users` wird gepatcht, damit dieser Test nie den echten Keyring
(Service `nikinger-space`) anfasst, gleiches Muster wie `mcp_smoke.py`/`oauth_smoke.py`.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from mcpserver.request_log import AccessLogASGI

SERVE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "serve.py"


def _load_serve_module():
    """`scripts/` ist kein Package — Laden über den Dateipfad, gleiches Muster wie
    `test_oauth_smoke.py :: _load_oauth_smoke_module()`."""
    spec = importlib.util.spec_from_file_location("serve", SERVE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["serve"] = module
    spec.loader.exec_module(module)
    return module


def test_main_wires_a_real_app_and_calls_uvicorn_run(tmp_path, monkeypatch):
    monkeypatch.setenv("SPACE_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("SPACE_PUBLIC_BASE_URL", "https://space.example.ts.net")
    monkeypatch.setenv("SPACE_AUTH_DB", str(tmp_path / "auth.sqlite3"))

    serve = _load_serve_module()
    monkeypatch.setattr(serve, "load_users", lambda: {})

    calls: list[dict] = []

    def fake_run(app, **kwargs):
        calls.append({"app": app, **kwargs})

    monkeypatch.setattr(serve.uvicorn, "run", fake_run)

    result = serve.main([])

    assert result == 0
    assert len(calls) == 1
    # AccessLogASGI(OAuthLogASGI(app)) umschließt die eigentliche Starlette-App (Plan §3.3) —
    # das ist die Verdrahtung, die dieser Test beweist, kein Umweg.
    assert isinstance(calls[0]["app"], AccessLogASGI)
    assert calls[0]["access_log"] is False


def test_main_dies_loudly_without_public_base_url(tmp_path, monkeypatch):
    """Kein stiller Fallback: fehlt `SPACE_PUBLIC_BASE_URL`, stirbt `load_auth_settings()`
    ungefangen — genau das Verhalten, das das Step-6b-Gate früher für lokale Läufe umging."""
    monkeypatch.setenv("SPACE_DATA_ROOT", str(tmp_path))
    monkeypatch.delenv("SPACE_PUBLIC_BASE_URL", raising=False)
    monkeypatch.setenv("SPACE_AUTH_DB", str(tmp_path / "auth.sqlite3"))

    serve = _load_serve_module()
    monkeypatch.setattr(serve, "load_users", lambda: {})
    monkeypatch.setattr(serve.uvicorn, "run", lambda app, **kwargs: None)

    try:
        serve.main([])
        raised = False
    except ValueError:
        raised = True

    assert raised is True
