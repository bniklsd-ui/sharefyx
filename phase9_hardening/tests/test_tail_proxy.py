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

Dazu vier Wächter für die Caddy-Vorlage (Stand 2026-10-01, aus der A4-Vorbereitungsrunde). Sie
sind nicht theoretisch: der Platzhalter `<vps-tailnet>` war im Kopfkommentar als Adresse *des
VPS* beschrieben, während `reverse_proxy` darunter auf die Heim-VM zeigt — wer nach der Kopfzeile
einsetzt, proxt Caddy auf sich selbst und der Fehler sieht in A4 wie ein totes Relay aus.

  7. test_the_upstream_placeholder_names_the_home_vm
  8. test_the_template_and_its_header_name_the_same_placeholders
  9. test_the_upstream_port_is_the_relay_port
 10. test_no_second_hsts_header_and_no_admin_off

Kein Netz, kein Dienst, kein root — alles statisch gegen die Dateien im Repo. Die
VPS-seitigen Artefakte (Caddyfile-Vorlage, ACL-Entwurf) haben je einen Wächter, weil ein
Fehler dort still ist: ein zu weit gefasster ACL-Entwurf scheitert erst am Deploy.

Die offene Frage, warum `socat` und nicht `tailscale serve --tcp` (ACL-Durchsetzung von
Tailscale-TCP-Forwardern, `[VERIFY] V162`), steht in `phase9_hardening/step_a/
RUNBOOK_STEP_A.md` §0 Befund 1 — dieser Test kann sie nicht beantworten, nur verhindern,
dass die getroffene Wahl unbemerkt verboten wird.

Die Vorlage wurde am 2026-10-01 gegen das **echte** `caddy validate` der Ubuntu-24.04-Version
geprüft (`caddy 2.6.2-6ubuntu0.24.04.3`, `Valid configuration`) und der Host-Header-Durchreich
daran gemessen (Befund 8 im Runbook). Diese Messung braucht das Binary und ist deshalb kein
Test — sie ist die Grundlage der Wächter 7–10, die ohne Binary auskommen.
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
    """Der ACL-Entwurf darf genau einen Grant tragen: tcp:8765 auf 100.93.43.122.

    Ein Entwurf, der zu weit gefasst ist, scheitert erst am Deploy — deshalb hier fail-closed.
    Die Form ist `grants`, nicht `acls`: belegt am 2026-09-30 am Screenshot der Console-Seite
    "Add rule" (Knopf "Save grant", Vorschau `{"ip": ...}`). Der Test prüft die Grants-Form,
    weil das die Form ist, die diese Console erzeugt.
    """
    draft = json.loads(ACL_DRAFT.read_text())
    grants = draft["grants"]
    assert len(grants) == 1, f"erwartet genau einen Grant, gefunden: {grants}"

    grant = grants[0]
    assert grant["src"] == ["tag:sharefyx-edge"], \
        "die Quelle muss der getaggte VPS sein, nicht ein ganzer Benutzer"
    assert grant["dst"] == ["100.93.43.122"], \
        f"das Ziel muss die Heim-VM sein, ist {grant['dst']}"
    assert grant["ip"] == ["tcp:8765"], \
        f"es darf genau TCP 8765 sein, ist {grant['ip']} -- 'tcp:*' oder '*:*' waere die " \
        "andere Regel als die beabsichtigte"
    assert "tagOwners" in draft and "tag:sharefyx-edge" in draft["tagOwners"], \
        "der Tag braucht einen Owner, sonst nimmt Tailscale die Policy nicht an"

    # Die Kommentar-Schluessel duerfen nicht ins Policy-File wandern -- sie sind Meta, und
    # Tailscale lehnt unbekannte Top-Level-Schluessel ab.
    meta = {k for k in draft if k.startswith("_")}
    assert not (meta & {"tagOwners", "grants"}), \
        "Kommentar-Schluessel duerfen die echten Schluessel nicht verdecken"


# --- Wächter für die Caddy-Vorlage (2026-10-01, A4-Vorbereitungsrunde) ---------

def _announced_placeholders(head: str) -> set[str]:
    """Die Platzhalter, die der Kopf als *Wert* ankündigt.

    Nur die Aufzaehlungszeilen (`#   <name>  Beschreibung`), nicht der ganze Kopf: der Kopf
    erklaert inzwischen auch, welcher Platzhalter vorher falsch war — diese Nennung ist eine
    Korrekturnotiz, keine Ankuendigung.
    """
    lines = [line for line in head.splitlines() if re.match(r"^#\s{2,}<[a-z-]+>", line)]
    assert lines, "keine Platzhalter-Zeile im Kopf gefunden — Vorlage ist ungewoehn"
    # Mit Klammern, weil die Wächter gegen die Zeichenfolge in der Datei vergleichen und
    # nicht gegen den Regex-Namen — ein Platzhalter ohne `<` ist kein Platzhalter.
    return {f"<{name}>" for name in re.findall(r"<([a-z-]+)>", "\n".join(lines))}


def _caddy_split() -> tuple[str, str]:
    """Die Vorlage in (Kopf, Konfigurationsteil) — getrennt am globalen Block `{` in Spalte 0."""
    head, sep, body = CADDYFILE.read_text().partition("\n{\n")
    assert sep, "kein globaler `{`-Block in Spalte 0 gefunden — Vorlage ist ungewohnt"
    return head, body


def _directives_only(text: str) -> str:
    """Nur die Anweisungen, ohne Kommentarzeilen.

    [2026-10-01, vierte Wiederholung derselben Falle] P8.6 Block H, P9 Step G und der
    tailscaled-watchdog-Wächter sind alle daran gescheitert, dass ein Kommentar einen Begriff
    nennt, den ein Wächter verbietet. Diese Vorlage erklärt *im Kommentar*, welches der alte,
    falsche Platzhalter war und warum kein `/healthz` konfiguriert wird — beides ist genau das,
    wonach die Wächter suchen. Darum wird hier strukturell getrennt: ein Kommentar darf einen
    Namen nennen, eine Anweisung nicht.
    """
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def test_the_upstream_placeholder_names_the_home_vm():
    """`reverse_proxy` zeigt auf die HEIM-VM, also muss der Platzhalter das auch sagen.

    [2026-10-01, datierter Fund] Der Platzhalter hieß `<vps-tailnet>` und war im Kopfkommentar
    als „Tailscale-Node-Name des VPS" beschrieben — während `reverse_proxy` darunter auf die
    Heim-VM zeigte. Wer nach der Kopfzeile einsetzt, lässt Caddy auf sich selbst proxen: der VPS
    lauscht auf 80/443, nicht auf 8765, also `connection refused` — das Fehlerbild eines toten
    Relays, mitten in der Abnahme (RUNBOOK §0 Befund 9, Schritt A4b).
    """
    head, body = _caddy_split()
    config = _directives_only(body)
    announced = _announced_placeholders(head)

    assert "<vps-tailnet>" not in config, \
        "reverse_proxy darf den alten VPS-Platzhalter nicht mehr benutzen — er zeigt auf die Heim-VM"
    assert "<vps-tailnet>" not in announced, \
        "der Kopf darf den alten Platzhalter nicht mehr als Wert ankündigen"
    assert "<heimvm-tailnet>" in config, \
        "reverse_proxy benutzt den alten Platzhalter nicht (Ziel ist die Heim-VM, nicht der VPS)"
    assert "<heimvm-tailnet>" in announced, \
        "der Kopf kündigt <heimvm-tailnet> nicht als Wert an — das war der Fund vom 2026-10-01"
    assert re.search(r"^\s*reverse_proxy\s+<heimvm-tailnet>:(\d+)\s*$", config, re.MULTILINE), \
        "reverse_proxy muss auf <heimvm-tailnet>:<port> zeigen"


def test_the_template_and_its_header_name_the_same_placeholders():
    """Was der Kopf ankündigt, muss die Anweisung benutzen — und umgekehrt.

    Genau dieser Bruch zwischen Kopfzeile und `reverse_proxy` war der Fund vom 2026-10-01, und
    er wirkt in beide Richtungen: ein Wert, den nur der Kopf nennt, wird beim Einsetzen nicht
    ersetzt (Caddy lehnt die Datei dann ab — erst auf dem VPS sichtbar); ein Platzhalter, den
    nur die Anweisung benutzt, wird durch eine frei erfundene Adresse ersetzt.
    """
    head, body = _caddy_split()
    announced = _announced_placeholders(head)
    used = {f"<{name}>" for name in re.findall(r"<([a-z-]+)>", _directives_only(body))}
    assert announced == used, (
        f"der Kopf kündigt {sorted(announced)} an, die Anweisung benutzt {sorted(used)} — "
        "das war der Fehler vom 2026-10-01"
    )
    assert used, "kein Platzhalter in der Anweisung gefunden — die Vorlage ist vollständig?"


def test_the_upstream_port_is_the_relay_port():
    """Der Upstream-Port muss der Port sein, auf dem das Relay lauscht.

    Sonst antwortet A4 mit `connection refused` auf dem VPS, und der Fehler sieht wie ein
    Firewall- oder ACL-Problem aus — Befund 9 hat schon einmal einen „firewall"-Fehler
    eingeordnet, der in Wahrheit ein fehlendes Programm war.
    """
    _, body = _caddy_split()
    port = re.search(
        r"^\s*reverse_proxy\s+<heimvm-tailnet>:(\d+)\s*$",
        _directives_only(body),
        re.MULTILINE,
    )
    assert port, "reverse_proxy-Zeile nicht gefunden"
    relay_port = _env_value(PROXY_SERVICE.read_text(), "APP_PORT")
    mcp_port = _env_value(MCP_SERVICE.read_text(), "SPACE_PORT")
    assert port.group(1) == relay_port == mcp_port, (
        f"Caddy zielt auf {port.group(1)}, das Relay lauscht auf {relay_port}, die App auf "
        f"{mcp_port} — das sind drei Zahlen, die gleich sein müssen"
    )


def test_no_second_hsts_header_and_no_admin_off():
    """Zwei Dinge, die man „härten" würde und die dabei etwas anderes zerstören.

    * **Kein `Strict-Transport-Security` in Caddy.** Die Anwendung setzt ihn selbst
      (`phase4_auth/authserver/routes.py:66`, `phase5_ui/webui/security.py:56`, beide
      `max-age=63072000; includeSubDomains` hinter `if settings.hsts`, Default `True`).
      Ein zweiter Header ist eine doppelte, abweichende Angabe.
    * **Kein `admin off`.** Gemessen am 2026-10-01 mit dem echten 2.6.2: die Paket-Unit hat
      `ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile --force`, und genau der
      bricht mit `admin off` in `dial tcp 127.0.0.1:2019: connect: connection refused` ab.
      Wer die API abschaltet, kaputt macht `systemctl reload caddy` — und merkt es beim ersten
      Mal, wenn jemand die Konfiguration ändern will.
    """
    _, body = _caddy_split()
    config = _directives_only(body)
    assert "Strict-Transport-Security" not in config, \
        "die Anwendung setzt HSTS selbst (authserver/routes.py:66, webui/security.py:56) — " \
        "ein zweiter Header im Caddy wäre eine abweichende Doppelangabe"
    assert not re.search(r"^\s*admin\s+off\s*$", config, re.MULTILINE), (
        "kein `admin off`: die ExecReload-Zeile der Paket-Unit braucht die Admin-API "
        "(gemessen 2026-10-01: connection refused auf 127.0.0.1:2019)"
    )
    # Und der Host-Header soll *durchgereicht* werden (gemessen 2026-10-01 vor dem Relay), also
    # darf auch kein `header_up` den Umschreiben erzwingen.
    assert "header_up" not in config, \
        "kein header_up: der Host-Header soll durchgereicht werden, sonst antwortet " \
        "TrustedHostMiddleware auf der falschen Domain"


def test_the_substituted_template_has_no_placeholder_left():
    """Nach dem Einsetzen der drei Werte darf in der Anweisung kein `<…>` übrig sein.

    Der Nikinger substituiert auf dem VPS per Hand. Diese Probe macht die Handarbeit prüfbar:
    sie ersetzt genau die dokumentierten Werte und prüft das Ergebnis. Sie validiert nicht die
    Caddy-Syntax — dafür gab es am 2026-10-01 ein echtes `caddy validate` gegen 2.6.2
    (`Valid configuration`, im Runbook Befund 9 festgehalten) — sondern die Lücke zwischen
    Vorlage und Ergebnis.
    """
    values = {
        "<domain>": "sharefyx.eurofyx.com",
        "<heimvm-tailnet>": "100.93.43.122",
        "<kontakt>": "probe@example.invalid",
    }
    substituted = CADDYFILE.read_text()
    for placeholder, value in values.items():
        assert placeholder in substituted, f"{placeholder} steht nicht mehr in der Vorlage"
        substituted = substituted.replace(placeholder, value)

    config = _directives_only(substituted.partition("\n{\n")[2])
    assert "<" not in config, \
        "nach dem Einsetzen steht noch ein Platzhalter in der Anweisung — welche Angabe fehlt?"
    assert "reverse_proxy 100.93.43.122:8765" in config, \
        "nach dem Einsetzen muss `reverse_proxy 100.93.43.122:8765` dastehen"
    assert "/healthz" not in config, \
        "/healthz gibt es nicht (app.py:220) — Befund 2; hier wird der Pfad konfiguriert, " \
        "nicht im Kommentar erklärt"
