"""Übergangsfenster der alten Web-UI-Adresse (P9 Step A, Nikinger-Entscheidung 2026-10-01,
`phase9_hardening/step_a/RUNBOOK_STEP_A.md` Befund 5).

Was hier festgehalten wird, und warum jede Zeile davon still verloren gehen könnte:

- die alte Origin schreibt **bis einschließlich** zum Enddatum, am Tag danach nicht mehr —
  und das Fenster schließt über die Uhr, nicht über einen Neustart (`clock` wird pro Anfrage gefragt)
- jede **andere** Origin bleibt verboten, auch während des Fensters
- ungesetzt = exakt das Verhalten vor diesem Commit
- die Konfiguration ist fail-closed: halb oder falsch gesetzt ist ein Startfehler
- `/api/v1/meta` liefert, was der Dialog braucht; der Dialog ist ein Overlay wie alle anderen
"""
from __future__ import annotations

import re
from datetime import date, datetime, timezone
from pathlib import Path

import httpx
import pytest
from authserver import crypto
from authserver.models import SessionRow
from mcpserver.config import load_settings
from starlette.requests import Request

from webui.config import UiSettings
from webui.errors import CsrfError
from webui.security import require_csrf

BASE_URL = "https://space.example.ts.net"  # muss zu conftest.py passen (Login-Fixtures)
LEGACY = "https://alt.example.ts.net"
UNTIL = date(2026, 10, 15)
STATIC = Path(__file__).resolve().parents[1] / "webui" / "static"


def _settings(today: date, *, legacy: bool = True) -> UiSettings:
    if not legacy:
        return UiSettings(base_url=BASE_URL, clock=lambda: today)
    return UiSettings(base_url=BASE_URL, legacy_origin=LEGACY, legacy_until=UNTIL, clock=lambda: today)


def _session() -> SessionRow:
    now = datetime(2026, 10, 1, 9, 0, 0, tzinfo=timezone.utc)
    return SessionRow(
        session_hash="irrelevant", space="niklas", csrf_hash=crypto.hash_secret("tok"),
        created_at=now, last_seen_at=now, absolute_expires_at=now,
        revoked_at=None, revoked_reason=None,
    )


def _post(origin: str) -> Request:
    headers = [(b"origin", origin.encode()), (b"x-csrf-token", b"tok")]
    return Request({"type": "http", "method": "POST", "headers": headers})


# -- CSRF -------------------------------------------------------------------------------------

@pytest.mark.parametrize("today", [date(2026, 10, 1), UNTIL])
def test_legacy_origin_writes_up_to_and_including_the_end_date(today):
    require_csrf(_post(LEGACY), _session(), settings=_settings(today))  # wirft nicht


def test_legacy_origin_is_rejected_the_day_after():
    with pytest.raises(CsrfError):
        require_csrf(_post(LEGACY), _session(), settings=_settings(date(2026, 10, 16)))


def test_the_window_closes_without_a_restart():
    """Dieselbe Settings-Instanz, die Uhr läuft weiter — genau der Fall „niemand startet neu"."""
    days = iter([date(2026, 10, 15), date(2026, 10, 16)])
    settings = UiSettings(base_url=BASE_URL, legacy_origin=LEGACY, legacy_until=UNTIL,
                          clock=lambda: next(days))
    require_csrf(_post(LEGACY), _session(), settings=settings)
    with pytest.raises(CsrfError):
        require_csrf(_post(LEGACY), _session(), settings=settings)


@pytest.mark.parametrize("origin", [
    "https://boese.example", "http://alt.example.ts.net", "https://alt.example.ts.net/", "null",
])
def test_any_other_origin_stays_rejected_inside_the_window(origin):
    with pytest.raises(CsrfError):
        require_csrf(_post(origin), _session(), settings=_settings(date(2026, 10, 1)))


def test_unset_window_is_the_old_behaviour():
    settings = _settings(date(2026, 10, 1), legacy=False)
    require_csrf(_post(BASE_URL), _session(), settings=settings)
    with pytest.raises(CsrfError):
        require_csrf(_post(LEGACY), _session(), settings=settings)
    assert settings.legacy_writable() is False


def test_the_new_address_is_unaffected_after_the_window():
    require_csrf(_post(BASE_URL), _session(), settings=_settings(date(2027, 1, 1)))


# -- Konfiguration (fail-closed) --------------------------------------------------------------

def _env(**extra: str) -> dict[str, str]:
    return {"SPACE_DATA_ROOT": "/tmp/irrelevant", **extra}


def test_settings_parse_a_complete_window():
    s = load_settings(_env(SPACE_UI_LEGACY_ORIGIN=LEGACY, SPACE_UI_LEGACY_UNTIL="2026-10-15"))
    assert (s.ui_legacy_origin, s.ui_legacy_until) == (LEGACY, UNTIL)


def test_settings_treat_empty_values_as_off():
    """Die Unit setzt die Variablen immer (`Environment=…=` mit leerem Wert, wenn `local.env`
    sie nicht kennt) — leer muss deshalb „aus" heißen, nicht „Fehler"."""
    s = load_settings(_env(SPACE_UI_LEGACY_ORIGIN="", SPACE_UI_LEGACY_UNTIL=""))
    assert (s.ui_legacy_origin, s.ui_legacy_until) == (None, None)


@pytest.mark.parametrize("origin,until", [
    (LEGACY, ""),                           # halb gesetzt
    ("", "2026-10-15"),                     # halb gesetzt
    (LEGACY + "/", "2026-10-15"),           # Browser schickt nie einen /
    ("http://alt.example.ts.net", "2026-10-15"),
    (LEGACY + "/ui", "2026-10-15"),
    ("alt.example.ts.net", "2026-10-15"),
    (LEGACY, "15.10.2026"),
])
def test_settings_reject_a_malformed_window(origin, until):
    with pytest.raises(ValueError):
        load_settings(_env(SPACE_UI_LEGACY_ORIGIN=origin, SPACE_UI_LEGACY_UNTIL=until))


def test_install_script_defaults_the_new_placeholders():
    """Ohne `${…:-}` bricht `install_units.sh` bei jeder alten `local.env` am Wächter
    „unaufgelöster Platzhalter" ab — oder, mit `set -u`, schon vorher."""
    root = Path(__file__).resolve().parents[2]
    script = (root / "phase3_edge" / "scripts" / "install_units.sh").read_text(encoding="utf-8")
    unit = (root / "phase4_auth" / "systemd" / "sharefyx-mcp.service").read_text(encoding="utf-8")
    for name, env in (("LEGACY_ORIGIN", "SPACE_UI_LEGACY_ORIGIN"), ("LEGACY_UNTIL", "SPACE_UI_LEGACY_UNTIL")):
        assert f'"s#__{name}__#${{{name}:-}}#g"' in script
        assert f"Environment={env}=__{name}__" in unit


# -- /api/v1/meta + Dialog --------------------------------------------------------------------

@pytest.fixture
def ui_settings() -> UiSettings:
    """Überschreibt die conftest-Fixture nur in diesem Modul — `sessions`/`full_app_items`
    bauen damit auf denselben Settings auf, wie `create_app()` es live tut."""
    return UiSettings(base_url=BASE_URL, legacy_origin=LEGACY, legacy_until=UNTIL,
                      clock=lambda: date(2026, 10, 1))


@pytest.mark.asyncio
async def test_meta_publishes_the_window(full_app_items, totp_code):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=full_app_items), base_url=BASE_URL) as client:
        response = await client.post(
            "/ui/login",
            data={"space": "niklas", "password": "correct horse battery staple", "totp": totp_code()},
        )
        assert response.status_code == 200
        meta = (await client.get("/api/v1/meta")).json()
    assert meta["canonical_url"] == BASE_URL
    assert meta["legacy"] == {"origin": LEGACY, "until": "2026-10-15", "writable": True}


def test_dialog_markup_reuses_the_settings_nav_style():
    html = (STATIC / "app.html").read_text(encoding="utf-8")
    block = re.search(r'<div class="overlay" id="legacy-host-dialog" hidden>.*?\n</div>', html, re.DOTALL)
    assert block, "legacy-host-dialog fehlt"
    assert 'class="btn account-nav" id="legacy-host-link"' in block.group(0)
    assert 'id="legacy-host-close"' in block.group(0)


def test_dialog_is_wired_like_every_other_overlay():
    js = (STATIC / "js" / "app.js").read_text(encoding="utf-8")
    code = "\n".join(line for line in js.splitlines() if not line.strip().startswith("//"))
    assert "!legacyHostDialogEl.hidden;" in code                       # anyOverlayOpen()
    assert "else if (!legacyHostDialogEl.hidden) legacyHostDialogEl.hidden = true;" in code  # ESC
    assert "showLegacyHostDialog(meta);" in code                       # bei jedem Laden
    assert "location.origin !== legacy.origin" in code                 # nur auf der alten Adresse
