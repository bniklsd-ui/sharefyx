#!/usr/bin/env python3
"""Deploy-B-Probe — die **Generalprobe** vor `v3.1.6` (Deploy B, nach Block 5–6).

**Wozu sie da ist.** Der Nikinger hat Deploy B am 2026-10-23 zurückgestellt: „die nächste
Session testet zuerst gründlich an der Wegwerf-Instanz". Diese Probe ist die Antwort darauf —
sie prüft **den Stand, der deployt werden soll** (`main` mit Block 5 + 6, `fastmcp 4.1.3`) an
einer Wegwerf-Instanz: eigener Port **8799**, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, selbstsigniertes
TLS, File-Keyring. **Nie** gegen den echten `DATA_ROOT`, die echte `auth.sqlite3` oder den
Keyring (Wurzel-`CLAUDE.md` §Working style, Freigabe vom 2026-10-22).

**Die fünf Gruppen** (jede Zelle: erwartet · gemessen · ok):

| Gruppe | Was | Warum sie hier steht |
|---|---|---|
| **A** | die Tore aus `phase8_5_picker_release/scripts/health_gate.sh` (1–5 + 7) | **das Tore-Skript selbst läuft live** — ein Deploy, der ein Tor reißt, fällt erst **nach** dem Deploy auf. Gate 4 (`/mcp/` → 401) ist das Tor, das Deploy B hätte reissen können: Block 6 hat `/mcp` **ohne** Slash exakt bedient (`_ExactMcpMount`) — der Mount **mit** Slash muss weiter 401 liefern |
| **B** | Transport `/mcp` (P10.5-25) | kein 307, 401 mit Challenge — die Abnahmezeile des Deploys |
| **C** | der MCP-Weg **über HTTP** (11 Werkzeuge, `append_to_items`) | die Unit-Tests laufen in-process; hier läuft der echte Client-Pfad gegen die laufende App |
| **D** | das Log-Feld `proto` (Block 5.3, V219) | P10.5-22 will es **live** sehen — hier wird zuerst geprüft, dass es überhaupt da ist |
| **E** | der Update-Log-Banner (Befund vom 2026-10-23) | der zweite Deploy **am selben Tag** bekommt die ID `#1` — dieselbe, die der erste schon hatte ⇒ **kein Banner**. Die Probe zählt das **nach** (Alt-Schema gegen das Schema „Zähler von unten") |

**Der Gegenlauf steckt in Gruppe E:** beide Schemata stehen im Ergebnis, damit die Aussage
„der Banner bleibt stumm" **gemessen** ist und nicht behauptet.

Ausgabe: genau ein JSON-Objekt auf stdout (Hard Rule 7), Rohwerte als JSON daneben.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
BASE_URL = "https://127.0.0.1:8799"
OUT_JSON = Path(__file__).resolve().parent / "p105_deploy_b_probe.json"
UPDATE_LOG = REPO_ROOT / "docs" / "UPDATE_LOG.md"
ERWARTETE_VERSION = "v3.1.6"
HEALTH_PORT = 8765  # der Port des **Live**-Dienstes — nur als Vergleichswert im Ergebnis


def _zellen() -> list[dict]:
    return []


def _zelle(zellen: list[dict], zid: str, gruppe: str, erwartet, gemessen, ok: bool) -> None:
    zellen.append({
        "id": zid,
        "gruppe": gruppe,
        "erwartet": erwartet,
        "gemessen": gemessen,
        "ok": bool(ok),
    })


# --------------------------------------------------------------------------------------
# A + B: die Tore des Health-Gates und der Transport
# --------------------------------------------------------------------------------------

def _http() -> "httpx.Client":
    import httpx

    return httpx.Client(base_url=BASE_URL, verify=False, timeout=20.0,
                        follow_redirects=False, trust_env=False)


def _gruppe_a_b(client, zellen: list[dict]) -> None:
    """Die Tore 1–5 des `health_gate.sh` + der Update-Log-Eintrag (Gate 7) — an der
    Wegwerf-Instanz statt live, mit **derselben** Erwartung."""
    r = client.get("/health")
    _zelle(zellen, "A1", "health_gate", 200, r.status_code, r.status_code == 200)
    health = {}
    try:
        health = r.json()
    except Exception:  # noqa: BLE001
        pass
    # **`/health` meldet die Paketversion, nicht das Release-Badge.** Das ist kein Fehler:
    # das Health-Gate prüft das Badge in `app.html` (Gate 5), die Paketversion ist eine andere
    # Größe (Paket `phase2_mcp`). Die Zelle hält beide fest, damit niemand sie verwechselt.
    _zelle(zellen, "A1b", "health_gate", "version-Feld vorhanden (Paketversion, nicht das Badge)",
           health.get("version"), bool(health.get("version")))

    r = client.get("/ui/login")
    _zelle(zellen, "A2", "health_gate", 200, r.status_code, r.status_code == 200)

    r = client.get("/api/v1/me")
    _zelle(zellen, "A3", "health_gate", 401, r.status_code, r.status_code == 401)

    # **Gate 4 — das Tor, das Deploy B hätte reissen können.** `/mcp/` (MIT Slash) muss
    # weiter 401 liefern: Block 6 hat die exakte Route `/mcp` **vor** den Mount gesetzt.
    r = client.get("/mcp/")
    _zelle(zellen, "A4", "health_gate", 401, r.status_code, r.status_code == 401)

    r = client.get("/ui/static/app.html")
    text = r.text
    treffer = re.search(r'rail__version"[^>]*>([^<]+)', text)
    badge = treffer.group(1) if treffer else None
    _zelle(zellen, "A5", "health_gate", ERWARTETE_VERSION, badge, badge == ERWARTETE_VERSION)

    # Gate 7: der oberste Update-Log-Eintrag muss **heute** datiert sein.
    text_log = UPDATE_LOG.read_text(encoding="utf-8")
    treffer = re.search(r"^## (\d{4}-\d{2}-\d{2})$", text_log, re.MULTILINE)
    oben = treffer.group(1) if treffer else None
    heute = datetime.now(timezone.utc).date().isoformat()
    _zelle(zellen, "A6", "health_gate", f"heute ({heute})", oben, oben == heute)


def _gruppe_b(client, zellen: list[dict], token: str | None) -> None:
    """Transport: `/mcp` **ohne** Slash exakt (P10.5-25) — 401 mit Challenge, kein 307."""
    koepfe = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    r = client.post("/mcp", headers=koepfe, content=json.dumps({"jsonrpc": "2.0", "id": 1,
                                                               "method": "tools/list"}))
    challenge = r.headers.get("www-authenticate")
    _zelle(zellen, "B1", "transport", "401 + WWW-Authenticate, kein 307",
           f"{r.status_code} · challenge={'ja' if challenge else 'nein'}",
           r.status_code == 401 and bool(challenge))
    _zelle(zellen, "B1b", "transport", "kein 3xx", r.status_code,
           not (300 <= r.status_code < 400))

    if token:
        auth = dict(koepfe)
        auth["Authorization"] = f"Bearer {token}"
        r = client.post("/mcp", headers=auth, content=json.dumps({"jsonrpc": "2.0", "id": 2,
                                                                "method": "tools/list"}))
        _zelle(zellen, "B2", "transport", "kein 3xx (mit Token)",
               r.status_code, not (300 <= r.status_code < 400))
        r = client.get("/mcp/", headers=auth)
        _zelle(zellen, "B3", "transport", "kein 3xx (GET /mcp/ mit Token)",
               r.status_code, not (300 <= r.status_code < 400))
        r = client.get("/mcp", headers=auth)
        _zelle(zellen, "B4", "transport", "kein 3xx (GET /mcp mit Token)",
               r.status_code, not (300 <= r.status_code < 400))


# --------------------------------------------------------------------------------------
# C + D: der MCP-Weg über HTTP und das Log-Feld `proto`
# --------------------------------------------------------------------------------------

def _rpc(client, methode: str, params: dict | None, token: str, rid: int) -> dict:
    """Ein JSON-RPC-Aufruf gegen `/mcp` (stateless). Antwort kann JSON **oder** SSE sein."""
    koepfe = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {token}",
    }
    r = client.post("/mcp", headers=koepfe, content=json.dumps({
        "jsonrpc": "2.0", "id": rid, "method": methode, "params": params or {},
    }))
    r.raise_for_status()
    text = r.text
    if "text/event-stream" in (r.headers.get("content-type") or ""):
        for zeile in text.splitlines():
            if zeile.startswith("data:"):
                return json.loads(zeile[5:].strip())
        raise AssertionError("SSE-Antwort ohne data-Zeile")
    return json.loads(text)


def _gruppe_c_d(client, zellen: list[dict], token: str) -> dict:
    init = _rpc(client, "initialize", {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "p105-deploy-b-probe", "version": "1"},
    }, token, 10)
    proto = init.get("result", {}).get("protocolVersion")
    _zelle(zellen, "C1", "mcp", "initialize antwortet mit einer Protokollversion",
           proto, bool(proto))
    _zelle(zellen, "C1b", "mcp", "serverInfo vorhanden",
           init.get("result", {}).get("serverInfo", {}).get("name"),
           bool(init.get("result", {}).get("serverInfo")))

    tools = _rpc(client, "tools/list", {}, token, 11).get("result", {}).get("tools", [])
    namen = sorted(t.get("name", "") for t in tools)
    _zelle(zellen, "C2", "mcp", "11 Werkzeuge", len(tools), len(tools) == 11)
    _zelle(zellen, "C2b", "mcp", "append_to_items dabei",
           "append_to_items" in namen, "append_to_items" in namen)
    mit_annotations = [t.get("name") for t in tools if t.get("annotations")]
    _zelle(zellen, "C3", "mcp", "jedes Werkzeug trägt annotations",
           len(mit_annotations), len(mit_annotations) == len(tools))

    spaces = _rpc(client, "tools/call", {"name": "list_spaces", "arguments": {}}, token, 12)
    text_spaces = _text_von(spaces)
    _zelle(zellen, "C4", "mcp", "list_spaces antwortet",
           text_spaces[:120], "alpha" in (text_spaces or ""))

    # `append_to_items` mit **einem** falschen Eintrag (falsche Version) — genau die
    # Smoke-Zelle 17: der Teilerfolg darf die anderen Einträge nicht stoppen.
    # **Die Versionen werden vorher gelesen** (`get_item_meta`): die Probe ist sonst nicht
    # wiederholbar — nach dem ersten Lauf ist das Item eine Version weiter, und der
    # "gute" Eintrag würde dann selbst am Konflikt scheitern (gemessen: die erste Fassung
    # war nach einem Lauf rot).
    ids = json.loads((WEGWERF_ROOT / "ids.json").read_text())["ids"]
    gut = ids["alpha:Alpha Notiz Eins"]
    schlecht = ids["alpha:Alpha Notiz Zwei"]

    def _version(item_id: str) -> int:
        meta = _rpc(client, "tools/call",
                    {"name": "get_item_meta", "arguments": {"item_id": item_id}}, token, 15)
        roh = _text_von(meta) or "{}"
        try:
            return int(json.loads(roh).get("version"))
        except Exception:  # noqa: BLE001
            return 1

    version_gut = _version(gut)
    version_schlecht = _version(schlecht)
    erg = _rpc(client, "tools/call", {
        "name": "append_to_items",
        "arguments": {"entries": [
            {"item_id": gut, "version": version_gut, "text": "\n\nDeploy-B-Probe: Anhang."},
            {"item_id": schlecht, "version": version_schlecht + 1000,
             "text": "\n\nDeploy-B-Probe: Konflikt."},
        ]},
    }, token, 16)
    text_erg = _text_von(erg)
    try:
        quittung = json.loads(text_erg or "{}")
    except Exception:  # noqa: BLE001
        quittung = {}
    _zelle(zellen, "C5", "mcp", "ok:1, failed:1 (Teilerfolg)",
           f"ok={quittung.get('ok')} failed={quittung.get('failed')}",
           quittung.get("ok") == 1 and quittung.get("failed") == 1)

    # Das Log-Feld `proto` (Block 5.3): es muss im **Server-Log** des Wegwerf-Servers
    # stehen — nur der Abschnitt nach diesem Lauf zählt (Append-Log, dieselbe Lehre wie
    # in `p105_b6_opencode_e2e.py`).
    zeit = SERVE_LOG.stat().st_size if SERVE_LOG.exists() else 0
    _rpc(client, "tools/call", {"name": "list_spaces", "arguments": {}}, token, 14)
    time.sleep(0.4)
    neu = ""
    if SERVE_LOG.exists():
        with SERVE_LOG.open("rb") as fh:
            fh.seek(zeit)
            neu = fh.read().decode("utf-8", errors="replace")
    werkzeugzeilen = [z for z in neu.splitlines() if "ev=tool" in z or '"ev":"tool"' in z]
    mit_proto = [z for z in werkzeugzeilen if "proto=" in z or '"proto"' in z]
    _zelle(zellen, "D1", "log", "min. eine ev=tool-Zeile", len(werkzeugzeilen),
           bool(werkzeugzeilen))
    _zelle(zellen, "D2", "log", "die Zeile trägt proto=", mit_proto[:1],
           bool(mit_proto))

    # **D3: das Feld zeigt die *Anfrage*, nicht die Aushandlung.** Im zustandslosen Betrieb
    # ist jeder POST eine eigene Sitzung: ohne den Header `MCP-Protocol-Version` benutzt der
    # Server seinen Standardwert (gemessen: `2025-03-26`), auch wenn der Handshake
    # `2025-11-25` verabredet hatte. **Mit** dem Header steht die Version des Clients im Log.
    # Das ist die Grundlage für P10.5-22 (live: das Log-Feld `proto` zeigt die Ära) — die
    # Aussage gilt also nur, wenn der Client den Header mitsendet (opencode tut das).
    zeit2 = SERVE_LOG.stat().st_size if SERVE_LOG.exists() else 0
    koepfe = {"Content-Type": "application/json",
              "Accept": "application/json, text/event-stream",
              "Authorization": f"Bearer {token}",
              "MCP-Protocol-Version": "2025-11-25"}
    client.post("/mcp", headers=koepfe, content=json.dumps({
        "jsonrpc": "2.0", "id": 20, "method": "tools/call",
        "params": {"name": "list_spaces", "arguments": {}}}))
    time.sleep(0.4)
    neu2 = ""
    if SERVE_LOG.exists():
        with SERVE_LOG.open("rb") as fh:
            fh.seek(zeit2)
            neu2 = fh.read().decode("utf-8", errors="replace")
    zeilen2 = [z for z in neu2.splitlines() if "ev=tool" in z or '"ev":"tool"' in z]
    _zelle(zellen, "D3", "log", "mit MCP-Protocol-Version-Header steht die Version des Clients",
           zeilen2[-1:], any("2025-11-25" in z for z in zeilen2))

    return {"werkzeuge": namen, "protocolVersion": proto,
            "quittung_append_to_items": quittung, "log_werkzeugzeilen": werkzeugzeilen[-5:]}


def _text_von(antwort: dict) -> str | None:
    """Der Text eines `tools/call`-Ergebnisses (Content-Array, erstes Text-Element)."""
    inhalt = antwort.get("result", {}).get("content") or []
    for element in inhalt:
        if isinstance(element, dict) and element.get("type") == "text":
            return element.get("text")
    return None


# --------------------------------------------------------------------------------------
# E: der Update-Log-Banner — der Befund vom 2026-10-23, gemessen
# --------------------------------------------------------------------------------------

def _gruppe_e(zellen: list[dict]) -> dict:
    from webui.updates import parse_update_log

    text = UPDATE_LOG.read_text(encoding="utf-8")
    eintraege = parse_update_log(text)
    # **Beide Schemata werden hier unabhängig vom Ist-Code nachgebaut** — sie hängen nur an
    # den *Daten* der Blöcke, nicht an deren IDs. Der Unterschied zwischen beiden ist der
    # ganze Befund: die Reihenfolge, in der der Zähler läuft.
    daten = [e.date for e in eintraege]

    # Alt-Schema: Zähler von **oben** (Dateireihenfolge) — so vergab der Parser die IDs bis
    # 2026-10-23.
    zaehler_alt: dict[str, int] = {}
    ids_alt: list[str] = []
    for datum in daten:
        zaehler_alt[datum] = zaehler_alt.get(datum, 0) + 1
        ids_alt.append(f"{datum}#{zaehler_alt[datum]}")

    # Schema „Zähler von unten": der älteste Block eines Datums = #1, ein neu **oben**
    # eingefügter Block = die nächste freie Nummer. Die IDs der bestehenden Blöcke bleiben.
    zaehler_neu: dict[str, int] = {}
    ids_neu: list[str] = [""] * len(daten)
    for index in range(len(daten) - 1, -1, -1):
        datum = daten[index]
        zaehler_neu[datum] = zaehler_neu.get(datum, 0) + 1
        ids_neu[index] = f"{datum}#{zaehler_neu[datum]}"

    # Was der Benutzer nach Deploy A gesehen hat: damals gab es **einen** Block dieses
    # Datums, und der Parser vergab "#1".
    heutige = datetime.now(timezone.utc).date().isoformat()
    gleiche_datum = [d for d in daten if d == heutige]
    gesehen_vorher = f"{heutige}#1" if len(gleiche_datum) > 1 else None

    latest_alt = ids_alt[0] if ids_alt else None
    latest_neu = ids_neu[0] if ids_neu else None
    banner_alt = (latest_alt != gesehen_vorher) if gesehen_vorher else None
    banner_neu = (latest_neu != gesehen_vorher) if gesehen_vorher else None

    _zelle(zellen, "E1", "update_log", "oberster Block ist der neueste",
           eintraege[0].lines[0][:80] if eintraege else None, bool(eintraege))
    # **E2 ist der Gegenlauf:** das Alt-Schema (Zähler von oben) reproduziert den Befund —
    # der Banner bleibt stumm. Die Zelle ist grün, wenn der Defekt **reproduziert** ist.
    _zelle(zellen, "E2", "update_log", "Alt-Schema (Zaehler von oben): Banner bleibt STUMM",
           f"latest={latest_alt} seen={gesehen_vorher} banner={banner_alt}",
           banner_alt is False)
    # **E3 zeigt den Weg der Behebung:** das Schema „Zähler von unten" ⇒ der neue Deploy
    # ist hörbar.
    _zelle(zellen, "E3", "update_log", "Schema 'Zaehler von unten': Banner erscheint",
           f"latest={latest_neu} seen={gesehen_vorher} banner={banner_neu}",
           banner_neu is True)

    return {
        "eintraege": [{"id": e.id, "datum": e.date,
                       "erste_zeile": (e.lines[0] if e.lines else "")} for e in eintraege],
        "eintraege_alt_schema": [{"id": ids_alt[i], "datum": e.date}
                                  for i, e in enumerate(eintraege)],
        "eintraege_neu_schema": [{"id": ids_neu[i], "datum": e.date}
                                  for i, e in enumerate(eintraege)],
        "gesehen_vorher": gesehen_vorher,
        "latest_alt": latest_alt,
        "latest_neu": latest_neu,
        "banner_alt": banner_alt,
        "banner_neu": banner_neu,
    }


# --------------------------------------------------------------------------------------

def _token_ausgeben(space: str = "alpha") -> str:
    """Ein Bearer-Token **direkt** aus der Wegwerf-Auth-DB (tmp!) — derselbe Weg wie in
    `phase2_mcp/tests/test_asgi_bearer.py` (`create_family` + `issue_token_pair`).
    Kein Browser, kein OAuth-Tanz: die Probe prüft den Deploy, nicht den Login."""
    from authserver.store import AuthStore

    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    client = store.create_client(client_name="p105-deploy-b-probe", application_type=None,
                                 redirect_uris=["http://127.0.0.1:19876/cb"])
    family = store.create_family(
        space=space, client_id=client.client_id, scope="space",
        # **Die Ressource ist `<base_url>/mcp`** (`AuthSettings.resource`), NICHT der Pfad der
        # Protected-Resource-Metadata — die erste Fassung der Probe trug den Metadata-Pfad
        # und bekam deshalb 401 (der Resolver prüft die Audience, RFC 8707).
        resource=f"{BASE_URL}/mcp",
    )
    access, _refresh = store.issue_token_pair(family, access_ttl_s=3600,
                                              refresh_ttl_s=2_592_000)
    return access


def main() -> int:
    zellen = _zellen()
    ergebnis: dict = {
        "probe": "p105_deploy_b",
        "zeitpunkt": datetime.now(timezone.utc).isoformat(),
        "basis": {"repo_head": "main", "badge_erwartet": ERWARTETE_VERSION,
                  "live_dienst_port": HEALTH_PORT,
                  "wegwerf": str(WEGWERF_ROOT)},
    }
    token = None
    try:
        token = _token_ausgeben()
        ergebnis["token"] = "ausgestellt (tmp-auth.sqlite3, nicht ausgegeben)"
        with _http() as client:
            _gruppe_a_b(client, zellen)
            _gruppe_b(client, zellen, token)
            ergebnis["mcp"] = _gruppe_c_d(client, zellen, token)
    except Exception as exc:  # noqa: BLE001 — die Probe endet nie ohne Ergebnisdatei
        ergebnis["fehler"] = repr(exc)
    ergebnis["update_log"] = _gruppe_e(zellen)

    ergebnis["zellen"] = zellen
    ergebnis["bilanz"] = {
        "gesamt": len(zellen),
        "gruen": sum(1 for z in zellen if z["ok"]),
        "rot": sum(1 for z in zellen if not z["ok"]),
    }
    OUT_JSON.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(ergebnis, ensure_ascii=False, indent=1))
    return 0 if ergebnis["bilanz"]["rot"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
