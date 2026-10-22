#!/usr/bin/env python3
"""P10.5 Block 2, Schritt 2.5 — Rechte-Matrix Web × MCP (Abnahme P10.5-9/10/11).

**Wegwerf (Plan §2.3):** Port 8799, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b2`,
tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
Stopp nur über die PID-Datei (Hard Rule 9). Die Maschinerie (Provisionierung, TLS-Start,
PID-Stopp) kommt aus `phase10_inventory/probes/p10_wegwerf.py`; dieses Skript biegt nur deren
Pfadkonstanten auf die eigene Wurzel um — die P10-Wurzel bleibt unberührt.

**Datenlage (Akteur ist immer `alpha`):**
  - `alpha` — Home-Space von A (eigener Space)
  - `beta`  — Home-Space von B, `.share.yml` `read:`+`write: [alpha]` — der Fall
              „fremder Home-Space **mit** Schreibrecht". Ohne `write:` bliebe jedes ❌ an der
              älteren P6-AE-Prüfung („kein Schreibzugriff") hängen und bewiese nichts über
              RE-1/RE-2/P10-I/P10.5-N.
  - `gamma` — Team-Space (niemandes Home), `read:`+`write: [alpha]`
  - `delta` — Team-Space, nur `read: [alpha]` — AL-1 Zeile 14 (geteilter read-Space)

**Matrix:** Ordner anlegen · Ordner wechseln · Verschieben (Team ✅ / in fremden Home ❌ / aus
fremdem Home ❌) · geteilter read-Space (Schreiben ❌, fremder Body gewrappt). Jede ✅-Zelle
wird von der Platte zurückgelesen (Datei = Wahrheit, Hard Rule 2: Pfad `<space>/<ordner>/
<id>__*.md`), jede ❌-Zelle muss mit dem **erwarteten Text** scheitern, nicht nur irgendwie.

**MCP „Ordner anlegen":** die Agentenfläche hat kein eigenes Werkzeug dafür; der einzige Weg,
einen Ordner entstehen zu lassen, ist `create_item(space=, folder=<neu>)`. Diese Zellen (und ihr
Web-Zwilling `POST /api/v1/items` mit neuem Ordner) sind als **Messung** markiert, nicht als
Soll — der Plan nennt dafür kein Soll, und ein Item in einem Space mit `write:` anzulegen ist
Hard Rule 4 gemäß erlaubt.

Aufruf (Projekt-venv): `setup` → `start` → `rights` → `stop` (`cleanup` räumt die Wurzel ab).
Ausgabe: JSON auf stdout (Hard Rule 7) und `p105_b2_rights.json` daneben; Logs auf stderr.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
import p10_wegwerf as w  # noqa: E402

ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b2")
w.WEGWERF_ROOT = ROOT
w.DATA_ROOT = ROOT / "data"
w.AUTH_DB = ROOT / "auth.sqlite3"
w.KEYRING_FILE = ROOT / "keyring.json"
w.DEK_FILE = ROOT / "auth-dek"
w.CREDS_FILE = ROOT / "credentials.json"
w.SERVE_PID = ROOT / "serve.pid"
w.SERVE_LOG = ROOT / "serve.log"
w.TLS_KEY = ROOT / "key.pem"
w.TLS_CERT = ROOT / "cert.pem"
IDS_FILE = ROOT / "ids.json"
OUT_JSON = Path(__file__).with_name("p105_b2_rights.json")
BASE = w.BASE_URL  # https://127.0.0.1:8799


REDIRECT = "https://127.0.0.1:19877/callback"


def _clean_env() -> dict[str, str]:
    """Wie die Vorlage, plus `SPACE_*` (Plan §2.1 Punkt 5) — die Vorlage ließ diese stehen.
    Danach genau eine Zeile zurück: die Loopback-Rücksprungadresse des OAuth-Tanzes muss auf
    der Allowlist stehen (Muster `p10_m3_dcr_probe.py`), sonst lehnt `/oauth/authorize` ab."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("SHAREFYX_", "SFX_", "SPACE_"))}
    env["SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS"] = "https://127.0.0.1:19877"
    return env


w._clean_env = _clean_env


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# --- Setup ------------------------------------------------------------------------------

SEED = [
    # (Schlüssel, Space, Titel, Ordner)
    ("a_folder_web", "alpha", "A Ordner Web", ""),
    ("a_folder_mcp", "alpha", "A Ordner MCP", ""),
    ("a_to_team_web", "alpha", "A nach Team Web", ""),
    ("a_to_team_mcp", "alpha", "A nach Team MCP", ""),
    ("a_to_beta_web", "alpha", "A nach Beta Web", ""),
    ("a_to_beta_mcp", "alpha", "A nach Beta MCP", ""),
    ("g_folder_web", "gamma", "G Ordner Web", ""),
    ("g_folder_mcp", "gamma", "G Ordner MCP", ""),
    ("b_folder_web", "beta", "B Ordner Web", ""),
    ("b_folder_mcp", "beta", "B Ordner MCP", ""),
    ("b_to_alpha_web", "beta", "B nach Alpha Web", ""),
    ("b_to_alpha_mcp", "beta", "B nach Alpha MCP", ""),
    ("b_to_team_web", "beta", "B nach Team Web", ""),
    ("b_to_team_mcp", "beta", "B nach Team MCP", ""),
    ("d_read", "delta", "D Lesen", ""),
]


def cmd_setup(_args: argparse.Namespace) -> int:
    w.cmd_setup(_args)  # zwei Principale alpha + beta in der tmp-auth.sqlite3
    w._install_keyring()
    w._spacectl("create-space", "alpha")
    w._spacectl("create-space", "beta")
    w._spacectl("add-member", "--read", "beta", "alpha")
    w._spacectl("add-member", "--write", "beta", "alpha")
    w._spacectl("create-space", "gamma")
    w._spacectl("add-member", "--read", "gamma", "alpha")
    w._spacectl("add-member", "--write", "gamma", "alpha")
    w._spacectl("create-space", "delta")
    w._spacectl("add-member", "--read", "delta", "alpha")

    from storage.store import Store
    store = Store(str(w.DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids = {}
    for key, space, title, folder in SEED:
        body = f"Inhalt von {title} — Wegwerf P10.5 B2."
        ids[key] = store.create(space, type="note", title=title, body=body, folder=folder).id
    store.rebuild_index()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    log(f"Seed: {len(ids)} Items in alpha/beta/gamma/delta -> {IDS_FILE}")
    return 0


# --- Hilfen -----------------------------------------------------------------------------

_last_counter: dict[str, int] = {}


def fresh_totp(user: dict) -> str:
    """Jeder TOTP-Code ist einmal verbrauchbar (Replay-Schutz) — je Anmeldung ein neues Fenster."""
    secret = urllib.parse.parse_qs(urllib.parse.urlsplit(user["otpauth_uri"]).query)["secret"][0]
    while True:
        counter = int(time.time() // 30)
        # mindestens 2 s Abstand zur Fenstergrenze, sonst kippt der Code unterwegs
        if counter != _last_counter.get(user["space"]) and (time.time() % 30) < 26:
            break
        time.sleep(1)
    _last_counter[user["space"]] = counter
    key = base64.b32decode(secret + "=" * (-len(secret) % 8))
    import hmac
    import struct
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    off = digest[-1] & 0x0F
    return f"{(struct.unpack('>I', digest[off:off + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def where(item_id: str) -> dict | None:
    """Datei = Wahrheit: in welchem Space/Ordner liegt das Item auf der Platte?"""
    hits = [p for p in w.DATA_ROOT.rglob(f"{item_id}__*.md")
            if not p.relative_to(w.DATA_ROOT).parts[0].startswith(".")]
    if len(hits) != 1:
        return None
    parts = hits[0].relative_to(w.DATA_ROOT).parts
    return {"space": parts[0], "folder": "/".join(parts[1:-1])}


def folder_exists(space: str, folder: str) -> bool:
    return (w.DATA_ROOT / space / folder).is_dir()


# --- Web --------------------------------------------------------------------------------

class Web:
    def __init__(self, user: dict) -> None:
        self.user = user
        self.c = httpx.Client(base_url=BASE, verify=False, timeout=30)
        self.csrf = ""
        self.grant = None

    def login(self) -> None:
        r = self.c.post("/ui/login", data={
            "space": self.user["space"], "password": self.user["password"],
            "totp": fresh_totp(self.user)})
        m = re.search(r'id="bootstrap-csrf" name="csrf" value="([^"]+)"', r.text)
        if r.status_code != 200 or not m:
            raise RuntimeError(f"Web-Login fehlgeschlagen: HTTP {r.status_code}")
        self.csrf = m.group(1)
        log("Web: angemeldet als alpha")

    def _h(self) -> dict:
        return {"Origin": BASE, "X-CSRF-Token": self.csrf}

    def reauth(self) -> None:
        r = self.c.post("/api/v1/reauth", headers=self._h(), json={
            "password": self.user["password"], "totp": fresh_totp(self.user)})
        r.raise_for_status()
        self.grant = r.json().get("reauth_grant") or r.json().get("grant")
        log(f"Web: Reauth-Grant {'erhalten' if self.grant else 'FEHLT: ' + r.text[:200]}")

    def get(self, item_id: str) -> dict:
        r = self.c.get(f"/api/v1/items/{item_id}")
        r.raise_for_status()
        return r.json()

    def call(self, method: str, path: str, body: dict) -> dict:
        r = self.c.request(method, path, headers=self._h(), json=body)
        return {"status": r.status_code, "body": r.text[:400]}

    def patch(self, item_id: str, **fields) -> dict:
        body = {"version": self.get(item_id)["version"], **fields}
        if "space" in fields and self.grant:
            body["reauth_grant"] = self.grant
        return self.call("PATCH", f"/api/v1/items/{item_id}", body)


# --- MCP --------------------------------------------------------------------------------

class Mcp:
    def __init__(self, user: dict) -> None:
        self.user = user
        self.c = httpx.Client(base_url=BASE, verify=False, timeout=30, follow_redirects=False)
        self.token = ""
        self.n = 0

    def oauth(self) -> None:
        """Technik 3 aus `sichtpruefung_automation_conventions.md` (Vorlage `p10_m3_dcr_probe.py
        :: oauth_dance_to_initialize`), direkt gegen die TLS-Instanz statt über einen Proxy."""
        env = _clean_env()
        env["PYTHONPATH"] = str(REPO_ROOT)
        code = (
            "from authserver.store import AuthStore\n"
            "from datetime import datetime, timezone\n"
            f"s = AuthStore({str(w.AUTH_DB)!r}, now_fn=lambda: datetime.now(timezone.utc))\n"
            "c = s.create_client(client_name='p105-b2', application_type='web',\n"
            "                    redirect_uris=[" + repr(REDIRECT) + "])\n"
            "print(c.client_id)\n")
        client_id = subprocess.run([str(REPO_ROOT / ".venv/bin/python"), "-c", code], env=env,
                                   cwd=str(REPO_ROOT), check=True, capture_output=True,
                                   text=True).stdout.strip()
        meta = self.c.get("/.well-known/oauth-authorization-server").json()
        verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        redirect = REDIRECT
        h = {"Origin": BASE}
        r = self.c.get(meta["authorization_endpoint"], headers=h, params={
            "response_type": "code", "client_id": client_id, "redirect_uri": redirect,
            "scope": "space", "state": "s", "code_challenge": challenge,
            "code_challenge_method": "S256"})
        rid = re.search(r'name="request_id" value="([^"]+)"', r.text).group(1)
        r = self.c.post(meta["authorization_endpoint"], headers=h, data={
            "request_id": rid, "space": self.user["space"], "password": self.user["password"],
            "totp": fresh_totp(self.user), "action": "allow"})
        loc = r.headers.get("location", "")
        auth_code = urllib.parse.parse_qs(urllib.parse.urlsplit(loc).query)["code"][0]
        r = self.c.post(meta["token_endpoint"], headers=h, data={
            "grant_type": "authorization_code", "code": auth_code, "redirect_uri": redirect,
            "client_id": client_id, "code_verifier": verifier})
        r.raise_for_status()
        self.token = r.json()["access_token"]
        self._rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "p105-b2", "version": "0"}})
        log("MCP: Bearer erhalten, initialize ok")

    def _rpc(self, method: str, params: dict) -> dict:
        self.n += 1
        r = self.c.post("/mcp/", headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"},
            json={"jsonrpc": "2.0", "id": self.n, "method": method, "params": params})
        text = r.text
        if "data:" in text:
            text = next(line[5:].strip() for line in text.splitlines() if line.startswith("data:"))
        return json.loads(text)

    def tool(self, name: str, **args) -> dict:
        res = self._rpc("tools/call", {"name": name, "arguments": args}).get("result", {})
        text = "".join(c.get("text", "") for c in res.get("content", []))
        return {"is_error": bool(res.get("isError")), "text": text}

    def version(self, item_id: str) -> int:
        out = self.tool("get_item_meta", item_id=item_id)
        m = re.search(r'"version":\s*(\d+)', out["text"]) or re.search(r"version:\s*(\d+)", out["text"])
        return int(m.group(1))


# --- Matrix -----------------------------------------------------------------------------

RESULTS: list[dict] = []


def cell(row: str, surface: str, case: str, expect: str, raw: dict, *, ok_when: bool,
         deny_text: str | None = None) -> None:
    """`expect`: "ok" / "deny" / "measure". Bei "deny" muss `deny_text` in der Antwort stehen —
    sonst scheitert die Zelle an einer anderen Prüfung als der, die sie belegen soll."""
    blob = raw.get("body") or raw.get("text") or ""
    if expect == "ok":
        passed = ok_when
    elif expect == "deny":
        denied = raw.get("is_error") is True or raw.get("status", 200) >= 400
        passed = denied and (deny_text is None or deny_text in blob)
    else:
        passed = None
    RESULTS.append({"row": row, "surface": surface, "case": case, "expect": expect,
                    "pass": passed, "raw": raw})
    mark = {True: "PASS", False: "FAIL", None: "MESS"}[passed]
    log(f"  [{mark}] {row} · {surface} · {case}")


RE1_TEXT = "Ordner können nur im eigenen Space oder in einem Team-Space"
WEB_FOLDER_TEXT = "folder ist nur vom Eigentümer-Space änderbar"
MCP_FOLDER_TEXT = "folder ist nur im eigenen Space oder in einem Team-Space"
MOVE_TEXT = "Verschieben in oder aus dem Home-Space eines anderen"


def run_matrix(web: Web, mcp: Mcp, ids: dict) -> None:
    # 1. Ordner anlegen
    for space, expect in (("alpha", "ok"), ("gamma", "ok"), ("beta", "deny"), ("delta", "deny")):
        raw = web.call("POST", f"/api/v1/spaces/{space}/folders", {"folder": "Neu Web"})
        cell("RE-1 Ordner anlegen", "web", space, expect, raw,
             ok_when=raw["status"] < 400 and folder_exists(space, "neu-web"),
             deny_text=RE1_TEXT if space == "beta" else None)
    for space in ("alpha", "gamma", "beta", "delta"):
        raw = mcp.tool("create_item", type="note", title=f"Neu MCP {space}",
                       space=space, folder="Ordner MCP")
        raw["folder_on_disk"] = folder_exists(space, "ordner-mcp")
        cell("Ordner anlegen (implizit, create_item)", "mcp", space,
             "deny" if space == "delta" else "measure", raw, ok_when=False)
        raw = web.call("POST", "/api/v1/items", {"type": "note", "title": f"Neu Web {space}",
                                                 "space": space, "folder": "Ordner Item Web"})
        raw["folder_on_disk"] = folder_exists(space, "ordner-item-web")
        cell("Ordner anlegen (implizit, POST /items)", "web", space,
             "deny" if space == "delta" else "measure", raw, ok_when=False)

    # 2. Ordner wechseln
    for key, space, expect in (("a_folder", "alpha", "ok"), ("g_folder", "gamma", "ok"),
                               ("b_folder", "beta", "deny")):
        raw = web.patch(ids[f"{key}_web"], folder="Ziel Web")
        loc = where(ids[f"{key}_web"])
        cell("RE-1/RE-2 Ordner wechseln", "web", space, expect, {**raw, "on_disk": loc},
             ok_when=raw["status"] < 400 and loc == {"space": space, "folder": "ziel-web"},
             deny_text=WEB_FOLDER_TEXT)
        iid = ids[f"{key}_mcp"]
        raw = mcp.tool("update_item", item_id=iid, version=mcp.version(iid), folder="Ziel MCP")
        loc = where(iid)
        cell("RE-2 Ordner wechseln", "mcp", space, expect, {**raw, "on_disk": loc},
             ok_when=not raw["is_error"] and loc == {"space": space, "folder": "ziel-mcp"},
             deny_text=MCP_FOLDER_TEXT)

    # 3. Verschieben (P10-I / P10.5-N; AL-1 Zeile 29 = MCP alpha -> gamma)
    moves = (("a_to_team", "gamma", "ok", "alpha"), ("a_to_beta", "beta", "deny", "alpha"),
             ("b_to_alpha", "alpha", "deny", "beta"), ("b_to_team", "gamma", "deny", "beta"))
    for key, target, expect, source in moves:
        row = {"a_to_team": "P10-I Team-Ziel (Gegenlauf)", "a_to_beta": "P10-I in fremden Home",
               "b_to_alpha": "P10.5-N aus fremdem Home", "b_to_team": "P10.5-N aus fremdem Home"}[key]
        iid = ids[f"{key}_web"]
        raw = web.patch(iid, space=target)
        loc = where(iid)
        cell(row, "web", f"{source}->{target}", expect, {**raw, "on_disk": loc},
             ok_when=raw["status"] < 400 and loc == {"space": target, "folder": ""},
             deny_text=MOVE_TEXT)
        if expect == "deny":
            RESULTS[-1]["still_in_source"] = loc == {"space": source, "folder": ""}
        iid = ids[f"{key}_mcp"]
        raw = mcp.tool("update_item", item_id=iid, version=mcp.version(iid), space=target)
        loc = where(iid)
        cell(row + (" · AL-1 Zeile 29" if key == "a_to_team" else ""), "mcp",
             f"{source}->{target}", expect, {**raw, "on_disk": loc},
             ok_when=not raw["is_error"] and loc == {"space": target, "folder": ""},
             deny_text=MOVE_TEXT)
        if expect == "deny":
            RESULTS[-1]["still_in_source"] = loc == {"space": source, "folder": ""}

    # 4. Geteilter read-Space (AL-1 Zeile 14)
    d = ids["d_read"]
    cell("Zeile 14 read-Space schreiben", "web", "PATCH title", "deny",
         web.patch(d, title="X"), ok_when=False, deny_text="Kein Schreibzugriff")
    cell("Zeile 14 read-Space schreiben", "mcp", "update_item title", "deny",
         mcp.tool("update_item", item_id=d, version=mcp.version(d), title="X"), ok_when=False)
    cell("Zeile 14 read-Space schreiben", "mcp", "append_to_item", "deny",
         mcp.tool("append_to_item", item_id=d, version=mcp.version(d), text="X"), ok_when=False)
    for key, space in (("d_read", "delta"), ("g_folder_mcp", "gamma"), ("b_folder_mcp", "beta")):
        out = mcp.tool("get_item", item_id=ids[key])
        cell("Zeile 14 fremder Body gewrappt (get_item)", "mcp", space, "ok", out,
             ok_when=f'<untrusted_content space="{space}">' in out["text"])
    out = mcp.tool("get_item", item_id=ids["a_folder_mcp"])
    cell("Zeile 14 Gegenlauf: eigener Body ungewrappt", "mcp", "alpha", "ok", out,
         ok_when=not out["is_error"] and "<untrusted_content" not in out["text"])
    out = mcp.tool("search_items", space="delta")
    cell("Zeile 14 fremder Snippet gewrappt (search_items)", "mcp", "delta", "ok", out,
         ok_when='<untrusted_content space=\\"delta\\">' in out["text"]
         or '<untrusted_content space="delta">' in out["text"])


def cmd_rights(_args: argparse.Namespace) -> int:
    ids = json.loads(IDS_FILE.read_text())
    alpha = json.loads(w.CREDS_FILE.read_text())["users"][0]
    assert alpha["space"] == "alpha"
    mcp = Mcp(alpha)
    mcp.oauth()
    web = Web(alpha)
    web.login()
    web.reauth()  # Grant lebt 90 s — direkt vor der Matrix
    run_matrix(web, mcp, ids)
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                         capture_output=True, text=True).stdout.strip()
    graded = [r for r in RESULTS if r["pass"] is not None]
    result = {
        "probe": "p105_b2_rights", "head": sha, "base_url": BASE,
        "seed": {"beta": "home B, read+write alpha", "gamma": "team, read+write alpha",
                 "delta": "team, read alpha"},
        "graded": len(graded), "passed": sum(1 for r in graded if r["pass"]),
        "measured": [r for r in RESULTS if r["pass"] is None],
        "cells": RESULTS,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("cells", "measured")}))
    return 0 if result["passed"] == result["graded"] else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="P10.5 B2 Rechte-Matrix (Wegwerf 8799)")
    p.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "health", "rights"])
    args = p.parse_args(argv)
    return {"setup": cmd_setup, "start": w.cmd_start, "stop": w.cmd_stop,
            "cleanup": w.cmd_cleanup, "health": w.cmd_health, "rights": cmd_rights}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
