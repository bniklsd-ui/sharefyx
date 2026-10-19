#!/usr/bin/env python3
"""M3 (P10-Plan §4, Register PA-1/PA-5/PA-7, [VERIFY] V195/V198): was schickt ein
Nicht-Claude-Client, und woran scheitert er heute?

**Erwartet: rot.** `register_client()` (`authserver/clients.py:52`) wirft bei
`application_type: "native"` ein `invalid_client_metadata`, und `redirect_uri_allowed()`
(:34) verlangt `https` + Allowlist — ein Loopback-Redirect (`http://127.0.0.1:…`) fällt
durch `invalid_redirect_uri`. Laut Spec MCP 2026-07-28 SHOULD ein nativer Client genau das
senden; opencode registriert laut PR #5940 mit `http://127.0.0.1:19876/mcp/oauth/callback`
(V195). Diese Probe hält den echten Request fest, statt ihm zu vertrauen.

**Messaufbau (drei Ebenen):**
1. **Protokollierender TLS-Proxy als Eingang.** Die Wegwerf-App zieht auf den internen Port
   18799 (plain HTTP), der Proxy terminiert TLS auf 8799 (dasselbe selbstsignierte
   Zertifikat) und reicht Bytes durch — für opencode ist der Origin unverändert
   `https://127.0.0.1:8799`, also stimmt der Issuer weiter mit dem Browser-/Client-Origin
   überein, und JEDER Request (inkl. DCR-Body) passiert das Protokoll.
2. **opencode isoliert:** eigenes `XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_CACHE_HOME` (die
   Konfig des Nikingers bleibt unangetastet), `NODE_EXTRA_CA_CERTS` auf das Wegwerf-
   Zertifikat, MCP-Server-Eintrag auf die Proxy-Adresse. Dann `opencode mcp auth` und
   danach `opencode mcp debug` — Ausgabe wird festgehalten.
3. **M3b (optional laut Plan, hier gefahren):** ein Client mit Loopback-Redirect wird DIREKT
   in die Wegwerf-`auth.sqlite3` geschrieben (Wegwerf-Daten, kein Trick gegen Echtes) und
   der OAuth-Dance per httpx zu Ende gespielt (Technik 3 aus
   `sichtpruefung_automation_conventions.md`) — bis `initialize`, dessen Antwort die
   **ausgehandelte Protokollversion** trägt (V198; Dev-venv, `mcp` 1.28.1 — was LIVE
   `mcp 1.30.0` aushandelt, bleibt die Frage der P10.5-Abnahme gegen die echte Instanz).

Ausgabe: JSON auf stdout (Hard Rule 7) + `p10_m3_dcr.json` neben diesem Skript.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
import os
import secrets
import signal
import ssl
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_PY = REPO_ROOT / ".venv" / "bin" / "python"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
CERT = WEGWERF_ROOT / "cert.pem"
KEY = WEGWERF_ROOT / "key.pem"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
PUBLIC_PORT = 8799
INTERNAL_PORT = 18799
PUBLIC_URL = f"https://127.0.0.1:{PUBLIC_PORT}"   # Issuer der App (bleibt https)
CLIENT_URL = f"http://127.0.0.1:{PUBLIC_PORT}"    # was opencode sieht (Proxy = plain http)
DATA_ROOT = str(WEGWERF_ROOT / "data")
OUT_JSON = REPO_ROOT / "phase10_inventory" / "probes" / "p10_m3_dcr.json"

PROXY_LOG: list[dict] = []  # je Zeile: {"dir": "req"/"res", "first_line": …, "body": …}


def _clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    return env


def _stop_standard_wegwerf() -> None:
    subprocess.run([str(PROJECT_PY), str(REPO_ROOT / "phase10_inventory/probes/p10_wegwerf.py"),
                    "stop"], cwd=str(REPO_ROOT), check=False, stdout=subprocess.DEVNULL)


# --- Ebene 1: interne App + TLS-Logging-Proxy -----------------------------------


PLAIN_LAUNCHER = '''"""Die Wegwerf-App auf dem internen Port, plain HTTP — der TLS-Eingang ist der Proxy."""
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"])
from datetime import datetime, timezone
import uvicorn
from authserver.config import load_auth_settings, load_data_encryption_key
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from storage.store import Store
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import load_settings
from mcpserver.logging_setup import configure_logging
from mcpserver.request_log import AccessLogASGI, OAuthLogASGI

settings = load_settings()
configure_logging(settings.log_level)
auth_settings = load_auth_settings()
auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
users = UserDirectory(auth_store, dek=load_data_encryption_key())
oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=users)
app = create_app(settings=settings, store=Store(settings.data_root),
                 allowed_hosts=["127.0.0.1"], oauth=oauth)
app = AccessLogASGI(OAuthLogASGI(app))
uvicorn.run(app, host="127.0.0.1", port=int(os.environ["INTERNAL_PORT"]),
            access_log=False, log_level=settings.log_level.lower())
'''

PROCS: dict[str, subprocess.Popen] = {}


def start_internal_app() -> None:
    launcher = WEGWERF_ROOT / "serve_plain_m3.py"
    launcher.write_text(PLAIN_LAUNCHER, encoding="utf-8")
    env = _clean_env()
    env.update({
        "SPACE_DATA_ROOT": DATA_ROOT,
        "SPACE_AUTH_DB": str(AUTH_DB),
        "SPACE_PUBLIC_BASE_URL": PUBLIC_URL,  # Issuer bleibt die öffentliche Adresse
        "SPACE_PORT": str(INTERNAL_PORT),
        "CREDENTIALS_DIRECTORY": str(WEGWERF_ROOT),
        "PYTHONPATH": str(REPO_ROOT),
        "REPO_ROOT": str(REPO_ROOT),
        "INTERNAL_PORT": str(INTERNAL_PORT),
        # M3b: die Allowlist bekommt den https-Loopback-Ersatz — die Frage von M3b ist die
        # Protokoll-Aushandlung, nicht die Redirect-Politik (PA-1 ist zu dem Zeitpunkt schon
        # an BEIDEN Gates belegt: register_client UND flows.py:98 rufen dieselbe
        # `redirect_uri_allowed()`).
        "SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS": "https://127.0.0.1:19876",
    })
    log = (WEGWERF_ROOT / "serve_m3_internal.log").open("ab")
    PROCS["app"] = subprocess.Popen(
        [str(PROJECT_PY), str(launcher)], env=env, cwd=str(REPO_ROOT),
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    for _ in range(40):
        try:
            httpx.get(f"http://127.0.0.1:{INTERNAL_PORT}/health", timeout=1).raise_for_status()
            print(f"interne App gesund auf {INTERNAL_PORT}", file=sys.stderr)
            return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("interne App wurde nicht gesund")


async def _pump(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            chunk = await reader.read(65536)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def _read_head_and_body(reader: asyncio.StreamReader) -> tuple[bytes, bytes]:
    """Kopf bis \\r\\n\\r\\n lesen (readuntil, nicht read(n) — das würde auf die vollen 64 KB
    warten und den Client verhungern lassen), dann genau Content-Length Body-Bytes."""
    head = await reader.readuntil(b"\r\n\r\n")
    lines = head.decode("latin-1").split("\r\n")
    length = 0
    for line in lines[1:]:
        if line.lower().startswith("content-length:"):
            length = int(line.split(":", 1)[1].strip())
    body = await reader.readexactly(length) if length else b""
    return head, body


async def handle_client(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter) -> None:
    """Plain-HTTP-Eingang mit **Issuer-Rewrite**: die App intern bleibt bei ihrem https-Issuer
    (`_validate_base_url` erzwingt das), aber opencode redet http mit dem Proxy — die TLS-
    Vertrauensfrage stellt sich damit gar nicht (Messbefund 2026-10-18: opencode 1.18.33/Bun
    ehrt keine der drei CA-Umgebungsvariablen im OAuth-Pfad; der normale MCP-Fetch schon).

    Der Proxy übersetzt in den Antworten auf `.well-known`-GETs und auf dem DCR-POST den
   Issuer `https://127.0.0.1:8799` → `http://127.0.0.1:8799` (und korrigiert
    Content-Length). Der SERVER sieht unveränderten Traffic; nur was der CLIENT liest,
    wird auf die http-Sicht getrimmt — ein Messinstrument, klar dokumentiert, kein Eingriff
    in Serververhalten. DCR-Requests (und ihre Antworten) werden zusätzlich festgehalten."""
    try:
        app_reader, app_writer = await asyncio.open_connection("127.0.0.1", INTERNAL_PORT)
    except Exception:
        client_writer.close()
        return
    state = {"rewrite_response": False, "capture_response": False}

    def _rewrite(head: bytes, body: bytes) -> tuple[bytes, bytes]:
        # Kopf UND Body: die 401-Challenge trägt resource_metadata im WWW-Authenticate-Header —
        # nur im Body zu ersetzen ließ opencode weiter auf https laufen (gemessen).
        head = head.replace(b"https://127.0.0.1:8799", b"http://127.0.0.1:8799")
        body = body.replace(b"https://127.0.0.1:8799", b"http://127.0.0.1:8799")
        lines = head.decode("latin-1").split("\r\n")
        while lines and lines[-1] == "":
            lines.pop()  # split hält die Abschluss-\r\n als Leerzeilen — sonst endet der
            # rekonstruierte Kopf mit \r\n\r\n\r\n und der Client liest den Body verschoben.
        out = [lines[0]]
        for line in lines[1:]:
            if line.lower().startswith("content-length:"):
                out.append(f"Content-Length: {len(body)}")
            else:
                out.append(line)
        return "\r\n".join(out).encode("latin-1") + b"\r\n\r\n", body

    async def upstream() -> None:
        try:
            while True:
                head = await client_reader.readuntil(b"\r\n\r\n")
                length = 0
                for line in head.decode("latin-1").split("\r\n")[1:]:
                    if line.lower().startswith("content-length:"):
                        length = int(line.split(":", 1)[1].strip())
                body = await client_reader.readexactly(length) if length else b""
                first_line = head.decode("latin-1").split("\r\n")[0]
                PROXY_LOG.append({"dir": "conn", "first_line": first_line})
                print(f"[proxy] {first_line}", file=sys.stderr)
                path = first_line.split(" ")[1] if " " in first_line else ""
                if path.startswith("/.well-known/"):
                    state["rewrite_response"] = True
                elif first_line.startswith("POST /oauth/register"):
                    PROXY_LOG.append({"dir": "request", "first_line": first_line,
                                      "body": body.decode("utf-8", "replace")})
                    state["capture_response"] = True
                    state["rewrite_response"] = True
                app_writer.write(head + body)
                await app_writer.drain()
        except (asyncio.IncompleteReadError, asyncio.LimitOverrunError, ConnectionResetError):
            pass
        except Exception:
            pass
        finally:
            try:
                app_writer.close()
            except Exception:
                pass

    async def downstream() -> None:
        async def _read_chunked(reader: asyncio.StreamReader) -> bytes:
            body = b""
            while True:
                size_line = await reader.readuntil(b"\r\n")
                size = int(size_line.split(b";")[0].strip() or b"0", 16)
                if size == 0:
                    await reader.readuntil(b"\r\n")
                    return body
                body += await reader.readexactly(size)
                await reader.readexactly(2)

        try:
            while True:
                head = await app_reader.readuntil(b"\r\n\r\n")
                head_l = head.decode("latin-1")
                length = 0
                chunked = "transfer-encoding:" in head_l.lower()
                has_cl = "content-length:" in head_l.lower()
                for line in head_l.split("\r\n")[1:]:
                    if line.lower().startswith("content-length:"):
                        length = int(line.split(":", 1)[1].strip())
                if "text/event-stream" in head_l.lower():
                    # Echtes SSE (POST /mcp): Kopf durchreichen, dann roh pumpen — diese
                    # Verbindung trägt keine weiteren geparsten Antworten.
                    client_writer.write(head)
                    await client_writer.drain()
                    while True:
                        chunk = await app_reader.read(65536)
                        if not chunk:
                            break
                        client_writer.write(chunk)
                        await client_writer.drain()
                    return
                if chunked:
                    # uvicorn schickt auch kleine 401-JSONs chunked — dechunkieren, damit
                    # der Issuer-Rewrite greift, und mit Content-Length neu ausliefern.
                    body = await _read_chunked(app_reader)
                    lines = [l for l in head_l.split("\r\n")[1:]
                             if l.strip() and not l.lower().startswith("transfer-encoding:")
                             and not l.lower().startswith("content-length:")]
                    lines.append(f"Content-Length: {len(body)}")
                    head = (head_l.split("\r\n")[0] + "\r\n" + "\r\n".join(lines) + "\r\n\r\n").encode("latin-1")
                elif has_cl:
                    body = await app_reader.readexactly(length)
                else:
                    # Kein Body (204 o. ä.) — nur Kopf durchreichen, Verbindung bleibt im
                    # Keep-Alive-Loop.
                    client_writer.write(head)
                    await client_writer.drain()
                    continue
                if state.pop("capture_response", False):
                    first_line = head_l.split("\r\n")[0]
                    PROXY_LOG.append({"dir": "response", "first_line": first_line,
                                      "body": body.decode("utf-8", "replace")})
                    print(f"[proxy] {first_line}", file=sys.stderr)
                if state.pop("rewrite_response", False) or b"https://127.0.0.1:8799" in head:
                    head, body = _rewrite(head, body)
                client_writer.write(head + body)
                await client_writer.drain()
        except (asyncio.IncompleteReadError, asyncio.LimitOverrunError, ConnectionResetError):
            pass
        except Exception:
            pass
        finally:
            try:
                client_writer.close()
            except Exception:
                pass

    await asyncio.gather(upstream(), downstream())


async def _log_dcr_response(app_reader: asyncio.StreamReader, client_writer) -> None:
    """Die Antwort auf den protokollierten DCR-Request: Kopf + Body festhalten, dann pumpen."""
    try:
        head, body = await _read_head_and_body(app_reader)
        first_line = head.decode("latin-1").split("\r\n")[0]
        PROXY_LOG.append({"dir": "response", "first_line": first_line,
                          "body": body.decode("utf-8", "replace")})
        print(f"[proxy] {first_line}", file=sys.stderr)
        client_writer.write(head + body)
        await client_writer.drain()
        await _pump(app_reader, client_writer)
    except (asyncio.IncompleteReadError, ConnectionResetError):
        pass
    except Exception:
        pass


async def run_proxy() -> object:
    server = await asyncio.start_server(handle_client, "127.0.0.1", PUBLIC_PORT)
    PROXY_SERVER["obj"] = server
    print(f"Logging-Proxy (plain http) auf {PUBLIC_PORT} -> {INTERNAL_PORT}", file=sys.stderr)
    return server


PROXY_SERVER: dict[str, object] = {}


def start_proxy() -> None:
    loop = asyncio.new_event_loop()

    async def _main():
        server = await run_proxy()
        async with server:
            await server.serve_forever()

    PROCS["proxy_thread"] = loop  # Marker; der Loop läuft im Thread unten
    import threading
    t = threading.Thread(target=loop.run_until_complete, args=(_main(),), daemon=True)
    t.start()
    PROCS["proxy"] = t
    time.sleep(0.8)


def stop_m3_stack() -> None:
    for key in ("app",):
        proc = PROCS.get(key)
        if proc and proc.poll() is None:
            os.kill(proc.pid, signal.SIGTERM)
            for _ in range(20):
                if proc.poll() is not None:
                    break
                time.sleep(0.25)
    loop = PROCS.get("proxy_thread")
    if loop is not None and loop.is_running():
        server = PROXY_SERVER.get("obj")

        def _close():
            if server is not None:
                server.close()

        loop.call_soon_threadsafe(_close)
        # Der Socket muss zu sein, BEVOR der Standard-Wegwerf 8799 wieder bindet.
        for _ in range(40):
            import socket
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", PUBLIC_PORT)) != 0:
                    break
            time.sleep(0.25)
        loop.call_soon_threadsafe(loop.stop)


# --- Ebene 2: opencode isoliert ---------------------------------------------------

OC_BIN = "/home/savefyx/.nvm/versions/node/v24.18.0/bin/opencode"
OC_CONFIG = Path("/tmp/opencode/p10-m3-opencode/config")
OC_DATA = Path("/tmp/opencode/p10-m3-opencode/data")
OC_CACHE = Path("/tmp/opencode/p10-m3-opencode/cache")
OC_STATE = Path("/tmp/opencode/p10-m3-opencode/state")


def opencode_env() -> dict[str, str]:
    for p in (OC_CONFIG, OC_DATA, OC_CACHE, OC_STATE):
        p.mkdir(parents=True, exist_ok=True)
    # opencode liest `$XDG_CONFIG_HOME/opencode/opencode.json` — die Config gehört in den
    # Unterordner, nicht direkt nach XDG_CONFIG_HOME (erster Lauf: „No OAuth-capable MCP
    # servers configured", weil die Datei eine Ebene zu hoch lag).
    config_dir = OC_CONFIG / "opencode"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "opencode.json").write_text(json.dumps({
        "$schema": "https://opencode.ai/config.json",
        "mcp": {
            "sharefyx": {"type": "remote", "url": f"{CLIENT_URL}/mcp", "enabled": True},
        },
    }, indent=2))
    env = _clean_env()
    env.update({
        "XDG_CONFIG_HOME": str(OC_CONFIG),
        "XDG_DATA_HOME": str(OC_DATA),
        "XDG_CACHE_HOME": str(OC_CACHE),
        "XDG_STATE_HOME": str(OC_STATE),
    })
    return env


def run_opencode(args: list[str], timeout_s: int = 120) -> dict:
    try:
        proc = subprocess.run(
            [OC_BIN, *args, "--print-logs", "--log-level", "DEBUG"],
            env=opencode_env(), cwd=str(REPO_ROOT), capture_output=True, text=True,
            timeout=timeout_s,
        )
        return {"exit": proc.returncode, "stdout": proc.stdout[-20000:], "stderr": proc.stderr[-20000:]}
    except subprocess.TimeoutExpired as e:
        return {"exit": None, "stdout": (e.stdout or "")[-20000:], "stderr": (e.stderr or "")[-20000:],
                "timeout": True}


# --- Ebene 3: M3b — vorregistrierter Loopback-Client bis initialize ----------------


def register_loopback_client() -> str:
    code = (
        "from authserver.store import AuthStore\n"
        "from datetime import datetime, timezone\n"
        f"s = AuthStore({str(AUTH_DB)!r}, now_fn=lambda: datetime.now(timezone.utc))\n"
        "c = s.create_client(client_name='p10-m3b', application_type='web',\n"
        "                    redirect_uris=['https://127.0.0.1:19876/callback'])\n"
        "print(c.client_id)\n"
    )
    env = _clean_env()
    env["PYTHONPATH"] = str(REPO_ROOT)
    out = subprocess.run([str(PROJECT_PY), "-c", code], check=True, env=env,
                         cwd=str(REPO_ROOT), capture_output=True, text=True)
    return out.stdout.strip()


def _totp(secret_b32: str) -> str:
    import hmac
    import struct
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    return f"{(struct.unpack('>I', digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def oauth_dance_to_initialize(client_id: str, creds: dict) -> dict:
    """Technik 3: der volle OAuth-2.1-Flow per httpx, dann initialize gegen /mcp."""
    import re as _re
    secs = int(time.time()) % 30
    time.sleep(35 - secs + 1)  # frisches TOTP-Fenster (Replay-Schutz verbraucht Codes)

    base = CLIENT_URL  # der Proxy ist plain http; die App antwortet mit https-Issuer
    origin = PUBLIC_URL  # CSRF-Origin-Gleichheit zählt den Header, nicht das Kabel
    with httpx.Client(verify=False, timeout=30, follow_redirects=False) as c:
        pr = c.get(f"{base}/.well-known/oauth-protected-resource/mcp").json()
        issuer = pr["authorization_servers"][0]
        as_meta = c.get(f"{base}/.well-known/oauth-authorization-server").json()
        authorize_url = as_meta["authorization_endpoint"]
        token_url = as_meta["token_endpoint"]

        verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        state = secrets.token_urlsafe(16)
        redirect_uri = "https://127.0.0.1:19876/callback"

        r = c.get(authorize_url, params={
            "response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri,
            "scope": "space", "state": state, "code_challenge": challenge,
            "code_challenge_method": "S256",
        }, headers={"Origin": origin})
        if r.status_code != 200:
            return {"stage": "authorize_get", "status": r.status_code, "body": r.text[:500]}
        rid_m = _re.search(r'name="request_id" value="([^"]+)"', r.text)
        if not rid_m:
            return {"stage": "authorize_form", "problem": "kein request_id-Feld", "body": r.text[:500]}
        r = c.post(authorize_url, data={
            "request_id": rid_m.group(1), "space": creds["space"],
            "password": creds["password"], "totp": _totp_from_uri(creds["otpauth_uri"]),
            "action": "allow",
        }, headers={"Origin": origin})
        if r.status_code not in (302, 303):
            return {"stage": "authorize_post", "status": r.status_code, "body": r.text[:500]}
        location = r.headers.get("location", "")
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(location).query)
        if "code" not in qs:
            return {"stage": "redirect", "location": location[:300]}
        r = c.post(token_url, data={
            "grant_type": "authorization_code", "code": qs["code"][0],
            "redirect_uri": redirect_uri, "client_id": client_id,
            "code_verifier": verifier,
        }, headers={"Origin": origin})
        if r.status_code != 200:
            return {"stage": "token", "status": r.status_code, "body": r.text[:500]}
        access = r.json()["access_token"]

        init = c.post(f"{base}/mcp/", headers={
            "Authorization": f"Bearer {access}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }, json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "p10-m3b-native", "version": "0.0.1"},
        }})
        text = init.text
        payload = None
        if "event:" in text or text.startswith("event:"):
            for line in text.splitlines():
                if line.startswith("data:"):
                    payload = json.loads(line[5:].strip())
                    break
        else:
            try:
                payload = init.json()
            except Exception:
                payload = {"raw": text[:500]}
        return {
            "stage": "initialize",
            "initialize_status": init.status_code,
            "content_type": init.headers.get("content-type", ""),
            "requested_protocol_version": "2025-03-26",
            "negotiated_protocol_version": (payload or {}).get("result", {}).get("protocolVersion"),
            "server_info": (payload or {}).get("result", {}).get("serverInfo"),
        }


def _totp_from_uri(uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlsplit(uri).query)
    return _totp(qs["secret"][0])


# --- Hauptlauf --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--skip-m3b", action="store_true")
    args = parser.parse_args(argv)

    creds = json.loads(CREDS_FILE.read_text())["users"][0]
    result: dict = {"probe": "p10_m3_dcr", "public_url": PUBLIC_URL,
                    "opencode_version": "1.18.33"}

    _stop_standard_wegwerf()
    try:
        start_internal_app()
        start_proxy()

        print("opencode mcp auth sharefyx ...", file=sys.stderr)
        result["mcp_auth"] = run_opencode(["mcp", "auth", "sharefyx"], timeout_s=150)
        print("opencode mcp debug sharefyx ...", file=sys.stderr)
        result["mcp_debug"] = run_opencode(["mcp", "debug", "sharefyx"], timeout_s=90)

        dcr = [e for e in PROXY_LOG if e["dir"] == "request"]
        dcr_res = [e for e in PROXY_LOG if e["dir"] == "response"]
        result["dcr_requests_seen"] = len(dcr)
        result["dcr_request"] = dcr[0]["body"] if dcr else None
        result["dcr_response_line"] = dcr_res[0]["first_line"] if dcr_res else None
        result["dcr_response_body"] = dcr_res[0]["body"] if dcr_res else None
        result["all_proxy_traffic"] = PROXY_LOG[:50]

        if dcr:
            try:
                body = json.loads(dcr[0]["body"])
                result["dcr_parsed"] = {k: body.get(k) for k in (
                    "client_name", "application_type", "redirect_uris",
                    "token_endpoint_auth_method", "grant_types", "response_types",
                    "client_uri", "scope",
                )}
            except Exception as exc:
                result["dcr_parse_error"] = str(exc)

        if not args.skip_m3b:
            print("M3b: Loopback-Client registrieren + OAuth-Dance ...", file=sys.stderr)
            client_id = register_loopback_client()
            result["m3b_client_id"] = client_id
            result["m3b"] = oauth_dance_to_initialize(client_id, creds)
    finally:
        stop_m3_stack()
        # Standard-Wegwerf (TLS auf 8799) wieder hochziehen — das Porto gehört der Instanz.
        subprocess.run([str(PROJECT_PY), str(REPO_ROOT / "phase10_inventory/probes/p10_wegwerf.py"),
                        "start"], cwd=str(REPO_ROOT), check=False, stdout=subprocess.DEVNULL)

    rejected = bool(result.get("dcr_response_line")) and (
        result["dcr_response_line"].startswith("HTTP/1.1 400")
        and bool(result.get("dcr_response_body"))
        and ("invalid_client_metadata" in result["dcr_response_body"]
             or "invalid_redirect_uri" in result["dcr_response_body"])
    )
    result["dcr_rejected_as_expected"] = rejected
    print(json.dumps(result, ensure_ascii=False, indent=1))
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
