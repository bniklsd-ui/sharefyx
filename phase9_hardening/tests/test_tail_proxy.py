"""Tests fuer phase3_edge/systemd/sharefyx-tail-proxy.service — P9 Step A, Befund 1.

Der Plan §3.2 A4 verlangt `reverse_proxy <heimvm-tailnet-name>:<port>`. Gemessen am
2026-09-29 ist das ohne einen zusaetzlichen Relay nicht baubar: die Anwendung bindet per
gelockerter P3-B-Entscheidung auf `127.0.0.1:8765` (`sharefyx-mcp.service`,
`Environment=SPACE_HOST=127.0.0.1`; `ss -ltnp` zeigt keinen Listener auf der Tailnet-IP).
Dieses Modul ist der Relay, der genau diese eine Luecke schliesst, ohne P3-B zu brechen.

Sechs Wächter, jeder gegen eine Eigenschaft, die beim Bauen stillschweigend verloren
gehen kann:

  1. test_target_is_the_loopback_address            # P3-B: Ziel bleibt 127.0.0.1
  2. test_bind_is_a_tailnet_address_not_wildcard   # 0.0.0.0 wäre P3-B gebrochen
  3. test_hardening_matches_the_mcp_service        # dieselben Direktiven wie die MCP-Unit
  4. test_execstart_carries_no_repo_path            # unabhaengig vom Release-Pfad
  5. test_the_port_is_the_one_the_app_listens_on   # Port darf nicht auseinanderlaufen
  6. test_health_route_correction_holds             # /health, nicht /healthz (Befund 2)

Kein Netz, kein Dienst, kein root — alles statisch gegen die Dateien im Repo. Die
VPS-seitigen Artefakte (Caddyfile-Vorlage, ACL-Entwurf) haben je einen Wächter, weil ein
Fehler dort still ist: ein zu weit gefasster ACL-Entwurf scheitert erst am Deploy.

Die offene Frage, warum `socat` und nicht `tailscale serve --tcp` (ACL-Durchsetzung von
Tailscale-TCP-Forwardern, `[VERIFY] V162`), steht in `phase9_hardening/step_a/
RUNBOOK_STEP_A.md` §0 Befund 1 — dieser Test kann sie nicht beantworten, nur verhindern,
dass die getroffene Wahl unbemerkt verboten wird.
"""

from __future__ import annotations

import json
import re
from ipaddress import ip_address, ip_network
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROXY_SERVICE = REPO_ROOT / "phase3_edge" / "systemd" / "sharefyx-tail-proxy.service"
MCP_SERVICE = REPO_ROOT / "phase4_auth" / "systemd" / "sharefyx-mcp.service"
APP_PY = REPO_ROOT / "phase2_mcp" / "mcpserver" / "app.py"
CADDYFILE = REPO_ROOT / "phase9_hardening" / "step_a" / "Caddyfile.template"
ACL_DRAFT = REPO_ROOT / "phase9_hardening" / "step_a" / "tailscale-acl.draft.json"

# Das Härtungs-Set, das `sharefyx-mcp.service` und `tailscaled-watchdog.service` tragen.
# Absichtlich als Liste und nicht als-abgeleitete-Menge: Test 3 soll eine Änderung an der
# MCP-Unit *sehen* (dann stimmt der Vergleich eben nicht mehr) und nicht stillschweigend
# mitwachsen.
HARDENING_DIRECTIVES = (
    "NoNewPrivileges",
    "PrivateTmp",
    "ProtectSystem",
    "ProtectHome",
    "ProtectKernelTunables",
    "ProtectControlGroups",
    "RestrictAddressFamilies",
    "MemoryDenyWriteExecute",
    "SystemCallFilter",
)


def _env_value(unit: str, name: str) -> str:
    # `Environment=NAME=WERT` — der Prefix ist Teil der Zeile, deshalb wird er mitgeprueft.
    m = re.search(rf"^(?:Environment=)?{name}=(\S+)\s*$", unit, re.MULTILINE)
    assert m, f"{name}= fehlt in der Unit"
    return m.group(1)


def _directive_names(unit: str) -> set[str]:
    return {
        m.group(1)
        for m in re.finditer(r"^([A-Z][A-Za-z]+)=", unit, re.MULTILINE)
    }


# --- Test 1 -----------------------------------------------------------------

def test_target_is_the_loopback_address():
    """Ziel muss Loopback bleiben — P3-B in Reinform. `0.0.0.0` als Ziel gäbe es nie."""
    unit = PROXY_SERVICE.read_text()
    assert _env_value(unit, "APP_ADDR") == "127.0.0.1", \
        "APP_ADDR muss 127.0.0.1 sein (P3-B: SPACE_HOST wird nie 0.0.0.0)"
    assert re.search(r"TCP4:\$\{APP_ADDR\}:\$\{APP_PORT\}", unit), \
        "ExecStart muss auf das Loopback-Ziel proxyt, nicht auf einen festen Socket"


# --- Test 2 -----------------------------------------------------------------

def test_bind_is_a_tailnet_address_not_wildcard():
    """Bind auf eine Tailnet-IP (100.64.0.0/10). 0.0.0.0 hieße: auch im LAN erreichbar."""
    unit = PROXY_SERVICE.read_text()
    bind = _env_value(unit, "TAILNET_ADDR")
    addr = ip_address(bind)
    assert addr in ip_network("100.64.0.0/10"), \
        f"TAILNET_ADDR {bind} liegt nicht im Tailnet-Bereich 100.64.0.0/10"
    assert not addr.is_unspecified, "0.0.0.0 würde den Port im LAN öffnen — P3-B"
    assert not addr.is_loopback, \
        "127.0.0.1 als Bind wäre nutzlos: der VPS könnte die Heim-VM dann nicht erreichen"
    assert re.search(r"bind=\$\{TAILNET_ADDR\}", unit), \
        "ExecStart muss auf TAILNET_ADDR binden, sonst bindet socat auf 0.0.0.0"


# --- Test 3 -----------------------------------------------------------------

def test_hardening_matches_the_mcp_service():
    """Jede Härtungs-Direktive der MCP-Unit muss auch hier stehen.

    Der Watchdog aus Step B trug dieselben zehn; diese Unit ist derselben Familie und wird
    von niemandem täglich gelesen, wenn sie von Hand gelockert würde.
    """
    proxy = _directive_names(PROXY_SERVICE.read_text())
    mcp = _directive_names(MCP_SERVICE.read_text())

    missing = [d for d in HARDENING_DIRECTIVES if d in mcp and d not in proxy]
    assert not missing, f"Härtungs-Direktiven fehlen im Relay: {missing}"

    # und die Werte, die nicht nur „da sein" wollen: die drei, bei denen ein schwächerer
    # Wert still Bestand hätte.
    unit = PROXY_SERVICE.read_text()
    for directive, expected in (
        ("NoNewPrivileges", "true"),
        ("ProtectSystem", "strict"),
        ("ProtectHome", "read-only"),
    ):
        assert re.search(rf"^{directive}={re.escape(expected)}\s*$", unit, re.MULTILINE), \
            f"erwartet `{directive}={expected}` in der Unit"


# --- Test 4 -----------------------------------------------------------------

def test_execstart_carries_no_repo_path():
    """ExecStart darf keinen Repo-Pfad nennen.

    Gemessener Befund aus Step B (Session-Block 2026-09-28): `__REPO_ROOT__` zeigt auf
    `/opt/sharefyx/current`, ein Symlink auf ein Release, das eine neu hinzugekommene Datei
    nicht enthält — der Watchdog startete dadurch ins Leere. Diese Unit zeigt auf
    `/usr/bin/socat` und ist damit konstruktiv unabhängig vom Release-Pfad.
    """
    unit = PROXY_SERVICE.read_text()
    exec_start = re.search(r"^ExecStart=(.*)$", unit, re.MULTILINE)
    assert exec_start, "ExecStart fehlt"
    line = exec_start.group(1)
    assert "__REPO_ROOT__" not in line, \
        "ExecStart mit __REPO_ROOT__ erbt die Release-Pfad-Kopplung aus dem Step-B-Befund"
    assert "/usr/bin/socat" in line, \
        "erwartet den absoluten Systempfad /usr/bin/socat — ein relativer Pfad hängt an $PATH"


# --- Test 5 -----------------------------------------------------------------

def test_the_port_is_the_one_the_app_listens_on():
    """Der Proxy-Port muss der Port sein, auf dem die Anwendung wirklich lauscht.

    Sonst hört der Relay auf einem toten Port und der VPS bekommt `connection refused` —
    ein Fehler, der in A4 wie ein Firewall-Problem aussieht.
    """
    proxy_port = _env_value(PROXY_SERVICE.read_text(), "APP_PORT")
    mcp_port = _env_value(MCP_SERVICE.read_text(), "SPACE_PORT")
    assert proxy_port == mcp_port, (
        f"Relay lauscht auf {proxy_port}, die App auf {mcp_port} — die beiden gehören zusammen"
    )


# --- Test 6 -----------------------------------------------------------------

def test_health_route_correction_holds():
    """/health ist die einzige Health-Route — Befund 2 hält, solange der Code so ist.

    Plan §3.4 (Abnahmezeile P9-10) nennt `/healthz`; die Route gibt es nicht
    (`app.py:216`). Dieser Wächter schlägt an, falls jemand sie doch hinzufügt — dann ist
    das Runbook nachzuziehen, statt zwei Adressen zu pflegen.
    """
    app = APP_PY.read_text()
    registered = re.findall(r'Route\("(/health[a-z]*)"', app)
    assert registered == ["/health"], \
        f"erwartet genau ['/health'], gefunden: {registered} — Runbook §0 Befund 2 nachziehen"

    # Nur die *Konfiguration* wird geprüft, nicht der Kommentar, der die Korrektur
    # erklärt — dieselbe Unterscheidung wie in `test_graph_reload.py`: ein Kommentar darf
    # eine Route nennen, eine Anweisung nicht.
    caddy_config = "\n".join(
        line for line in CADDYFILE.read_text().splitlines()
        if not line.lstrip().startswith("#")
    )
    assert "/healthz" not in caddy_config, \
        "die Caddy-Vorlage darf kein /healthz konfigurieren — die Route existiert nicht"


# --- Wächter für die VPS-seite ----------------------------------------------

def test_acl_draft_grants_exactly_one_port_on_one_address():
    """Der ACL-Entwurf darf genau eine Regel tragen: 8765 auf 100.93.43.122.

    Ein Entwurf, der zu weit gefasst ist, scheitert erst am Deploy — deshalb hier fail-closed.
    """
    draft = json.loads(ACL_DRAFT.read_text())
    rules = [r for r in draft["acls"] if r.get("action") == "accept"]
    granted = [r for r in rules if "tag:sharefyx-edge" in r.get("src", [])]
    assert len(granted) == 1, f"erwartet genau eine accept-Regel für den VPS, gefunden: {granted}"

    rule = granted[0]
    assert rule["dst"] == ["100.93.43.122:8765"], \
        f"die Freigabe muss genau 100.93.43.122:8765 sein, ist {rule['dst']}"
    assert rule["src"] == ["tag:sharefyx-edge"], \
        "die Quelle muss der getaggte VPS sein, nicht ein ganzer Benutzer"
    assert "tagOwners" in draft and "tag:sharefyx-edge" in draft["tagOwners"], \
        "der Tag braucht einen Owner, sonst nimmt Tailscale die Policy nicht an"
