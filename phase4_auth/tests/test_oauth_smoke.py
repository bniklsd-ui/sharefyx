"""Testet `scripts/oauth_smoke.py`. Die meisten Tests hier fahren es als echten Subprozess —
dieselbe Begründung wie `phase2_mcp/tests/test_mcp_smoke.py`: eine realistische Prüfung, keine
In-Process-Simulation, und das Skript ist bewusst kein Teil des `authserver`-Pakets.
`oauth_smoke.py` baut sein eigenes temporäres `DATA_ROOT`/`auth.sqlite3` selbst (kein
`--data-root`-Flag) — diese Tests übergeben deshalb keins.

**Ausnahme:** `test_oauth_log_never_contains_secrets` ruft `oauth_smoke._run()` direkt in-process
auf, statt einen Subprozess zu starten. Der Test braucht sowohl die echten, im Lauf erzeugten
Geheimnisse (`observed_secrets`) als auch den Logpuffer **desselben** Laufs — über den
Subprozess-Weg gäbe es dafür nur `--json` auf stdout, und die Geheimnisse dafür dort auszugeben
wäre genau das Leck, das dieser Test ausschließen soll.
"""
import asyncio
import importlib.util
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

SMOKE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "oauth_smoke.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SMOKE_PATH), *args], capture_output=True, text=True, timeout=30
    )


def _load_oauth_smoke_module():
    """`scripts/` ist kein Package (kein `__init__.py`, siehe `mcp_smoke.py`-Präzedenz) — Laden
    über den Dateipfad statt über einen Package-Import, gleiches Muster wie `SMOKE_PATH` oben.
    Registrierung in `sys.modules` **vor** `exec_module()` ist Pflicht, nicht Kosmetik: `Check`
    ist ein `@dataclass` mit `from __future__ import annotations` (String-Annotationen) — dessen
    Dekorator löst `cls.__module__` über `sys.modules` auf, um `ClassVar` zu erkennen, und crasht
    ohne einen vorab eingetragenen Modulnamen."""
    spec = importlib.util.spec_from_file_location("oauth_smoke", SMOKE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["oauth_smoke"] = module
    spec.loader.exec_module(module)
    return module


def test_smoke_json_all_checks_pass():
    # Zählt nicht mit, wie viele Prüfungen es gerade gibt (gleiche Begründung wie
    # test_mcp_smoke.py) — der Exit-Code trägt bereits das Pass/Fail-Signal.
    result = _run("--json")
    assert result.returncode == 0, result.stderr
    checks = json.loads(result.stdout)
    assert checks
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]


def test_smoke_covers_exactly_eleven_checks():
    """Plan §6 Abnahmezeilen 10/11 und §5 Step 6 Done-when nennen `oauth_smoke.py` **11/11** —
    ein Regressionstest, kein Zufall der aktuellen Aufteilung (siehe Moduldocstring, warum Runde
    2 gebündelt ist)."""
    result = _run("--json")
    checks = json.loads(result.stdout)
    assert len(checks) == 11, [c["name"] for c in checks]


def test_smoke_text_report_reads_all_green():
    result = _run()
    assert result.returncode == 0, result.stderr
    assert "fehlgeschlagen" not in result.stdout
    assert re.search(r"Alle \d+ Prüfungen grün\.", result.stdout)


def test_smoke_proves_refresh_and_code_replay_kill_the_family():
    """Die beiden namentlich im Plan verlangten Prüfungen (Abnahmezeilen 10/11) müssen wirklich
    existieren, nicht nur zufällig unter den elf grünen Haken sein."""
    result = _run("--json")
    checks = {c["name"]: c for c in json.loads(result.stdout)}
    assert checks["refresh_replay_kills_family"]["ok"] is True
    assert checks["code_replay_kills_family"]["ok"] is True


def test_smoke_script_does_not_touch_real_keyring_or_user_state():
    """Regressionstest für die im Moduldocstring versprochene Eigenschaft: `oauth_smoke.py`
    darf weder den echten Keyring noch echte Nutzerakten anfassen — TOTP-Seeds sind echte,
    umkehrbare Geheimnisse, nicht bloß Token-Hashes wie in P2/P3. Prüft Imports, nicht Prosa —
    der Moduldocstring selbst *nennt* `load_users()`/`load_auth_settings()` beim Erklären, warum
    sie nicht benutzt werden."""
    import_lines = [
        line
        for line in SMOKE_PATH.read_text().splitlines()
        if line.startswith("import ") or line.startswith("from ")
    ]
    source_imports = "\n".join(import_lines)
    assert "users" not in source_imports
    assert "load_auth_settings" not in source_imports
    assert "keyring" not in source_imports


class _CapturingHandler(logging.Handler):
    """Wie `phase2_mcp/tests/test_request_log.py::_CapturingHandler` — sammelt die rohen
    `LogRecord`-Objekte des `sharefyx.request`-Loggers, unformatiert."""

    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def test_oauth_log_never_contains_secrets(tmp_path):
    """Der wichtigste Test des Logging-Steps (Plan §4): treibt den vollständigen Fluss über
    `oauth_smoke._run()` mit erkennbaren Markerwerten und prüft den kompletten Logpuffer auf
    jeden Marker UND jedes real erzeugte Geheimnis (`observed_secrets`: TOTP-Codes,
    Autorisierungscodes, Access-/Refresh-Token). Prüft eine Zusage, keine Implementierung —
    genauso wie sein Vorbild `test_tool_event_never_contains_item_title`."""
    handler = _CapturingHandler()
    request_logger = logging.getLogger("sharefyx.request")
    request_logger.addHandler(handler)
    request_logger.setLevel(logging.INFO)
    previous_propagate = request_logger.propagate
    request_logger.propagate = False
    try:
        oauth_smoke = _load_oauth_smoke_module()
        checks: list = []
        observed_secrets: list[str] = []
        asyncio.run(oauth_smoke._run(tmp_path, checks, observed_secrets))
    finally:
        request_logger.removeHandler(handler)
        request_logger.propagate = previous_propagate
        sys.modules.pop("oauth_smoke", None)

    assert checks and all(c.ok for c in checks), [c for c in checks if not c.ok]
    assert observed_secrets  # Tautologie-Schutz Teil 1 (gleicher Advisor-Fund wie in P3 Step 2/
    # test_tool_event_never_contains_item_title): ohne echte Geheimnisse im Lauf wäre die
    # Abwesenheitsprüfung unten leer und würde auch bei einem komplett stummen Logger grün bleiben.

    oauth_events = [
        r.msg for r in handler.records if isinstance(r.msg, dict) and r.msg.get("ev") == "oauth"
    ]
    # Tautologie-Schutz Teil 2: beweist, dass `OAuthLogASGI` tatsächlich lief (alle vier Stufen
    # aus dem echten Fluss) — sonst würde ein leerer `handler.records` (z. B. weil die Verdrahtung
    # in `_run()` entfernt wurde oder der Loggername driftet) denselben Test ebenfalls grün lassen,
    # weil `secret not in ""` immer wahr ist.
    assert {e["stage"] for e in oauth_events} >= {
        "register", "authorize_get", "authorize_post", "token"
    }

    # Bewusst OHNE `TokenScrubbingFilter` im Aufnahmepfad (anders als ein evtl. erster Instinkt,
    # über echtes `configure_logging()`/stderr zu capturen): der Filter würde ein echtes Leck
    # nachträglich verdecken. Dieser Test prüft die PRIMÄRE Sicherung — Feld-Whitelist +
    # `OAuthLogASGI`s Body-/Header-Freiheit —, nicht die Verteidigung in der Tiefe. Der Filter
    # selbst ist separat getestet (`test_logging.py`).
    full_text = "\n".join(
        json.dumps(r.msg, ensure_ascii=False) if isinstance(r.msg, dict) else str(r.msg)
        for r in handler.records
    )
    for secret in [*observed_secrets, *oauth_smoke.MARKER_SECRETS]:
        assert secret not in full_text, f"Geheimnis im Log gefunden: {secret!r}"
