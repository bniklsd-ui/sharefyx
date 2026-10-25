#!/usr/bin/env python3
"""P10.5 Block 11, Schritt 11.6 — die Format-Konvention (ED-3) an der Wegwerf-Instanz.

**Wegwerf (Plan §2.3):** Port **18814** (eigener Port), eigene Wurzel
`/tmp/opencode/sharefyx-wegwerf-p105-b11-markdown`, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp **nur** über die PID-Datei
(Hard Rule 9).

**Was gemessen wird (Abnahme P10.5-54, ED-3):**

| # | Zelle | Erwartung |
|---|---|---|
| 1 | **Farbe** rendert | `[Text]{.rot}` → ein `span` mit der Klasse `md-c-rot` |
| 2 | **Größe** rendert | `[Text]{.klein}` → ein `span` mit der Klasse `md-s-klein` |
| 3 | **Farbe und Größe** | `[Text]{.rot .gross}` → **beide** Klassen an einem `span` |
| 4 | **Unbekannte Klasse** | `[Text]{.style}` → **wörtlich** (kein `span`, der Text steht da) |
| 5 | **Ausrichtung** (Block) | `::: {.zentriert}` … `:::` → ein `div` mit der Klasse `md-a-zentriert` |
| 6 | **HTML bleibt wörtlich** | `<b>x</b>` → **kein** Element, der Text steht da |
| 7 | **Codespan** | `` `[x]{.rot}` `` → **kein** `span` (im Code wird nichts formatiert) |
| 8 | **Werkzeugleiste** | die drei Felder bieten genau das Vokabular an |
| 9 | **MCP `get_item`** | der Rohtext kommt **unverändert** zurück (der Server kennt die Formate nicht) |

**Der Gegenlauf ist der Kern der Probe.** Zelle 4 („eine unbekannte Klasse bleibt wörtlich")
ist eine **Entscheidung des Codes**: ein Fehler darin wäre still — der Renderer würde eine
Klasse erfinden, die es nicht gibt, und niemand merkte es. Die zweite Messung liefert die
`markdown.js` deshalb **ohne** die wörtlich-Fallback (`return null; // unbekannte Klasse`)
aus (same-origin, also CSP-konform) und erwartet, dass **genau die Zelle 4** rot wird. **Die
anderen Zellen bleiben grün** — sonst wäre der Gegenlauf kein Gegenlauf, sondern ein
Totalausfall.

**Die Belegpflicht (aus Block 11.4 übernommen):** die gepatchte Datei trägt eine **Kennung**
(`window.__p105_markdown_variante`), und der Browser **liest sie zurück**. Ohne diesen Beleg
wäre jede Zahl aus dem Gegenlauf wertlos.

**Der Zustand ist derselbe Server für beide Messungen:** der MCP liest nur, es schreibt
nichts — beide Läufe sehen denselben Bestand.

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b11_markdown_probe.py`
Ergebnis: `phase10_5_finishing/probes/p105_b11_markdown.json`
Gegenlauf: `phase10_5_finishing/probes/p105_b11_markdown_gegenlauf.json`
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import secrets
import shutil
import ssl
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b11-markdown")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18814
BASE = f"https://127.0.0.1:{PORT}"
TLS_KEY = WEGWERF_ROOT / "key.pem"
TLS_CERT = WEGWERF_ROOT / "cert.pem"
SPACE = "alpha"
RESULT = Path(__file__).with_name("p105_b11_markdown.json")
RESULT_GEGENLAUF = Path(__file__).with_name("p105_b11_markdown_gegenlauf.json")

#: Der **Text** des Items. Alle Formen der Konvention, damit der MCP-Text und die
#: Renderer-Ausgabe dieselbe Quelle haben.
BODY = (
    "# Format-Konvention\n"
    "\n"
    "[rot]{.rot}\n"
    "\n"
    "[klein]{.klein}\n"
    "\n"
    "[beides]{.rot .gross}\n"
    "\n"
    "[fremd]{.style}\n"
    "\n"
    "::: {.zentriert}\n"
    "Zentriert.\n"
    ":::\n"
)

#: Die **Erwartung** je Zelle: `zelle` → (Name, Prüfer-Name im Browserergebnis, erwartet).
#: Die Prüfer laufen **im Browser** (siehe `BROWSER_SKILL`); hier steht nur, was grün heißen
#: muss.
ZELLEN = [
    ("farbe", "span_mit_klasse", "md-c-rot"),
    ("groesse", "span_mit_klasse", "md-s-klein"),
    ("farbe_und_groesse", "span_mit_klassen", "md-c-rot md-s-gross"),
    ("unbekannte_klasse_woertlich", "unbekannt_woertlich", True),
    ("ausrichtung", "block_mit_klasse", "md-a-zentriert"),
    ("html_woertlich", "html_woertlich", True),
    ("codespan_unformatiert", "codespan_unformatiert", True),
    ("werkzeugleiste", "werkzeugleiste_vokabular", True),
]


def log(text: str) -> None:
    print(text, file=sys.stderr, flush=True)


SERVE_TLS_LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS."""
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"])
import uvicorn
from phase2_mcp.scripts import serve

_orig_run = uvicorn.run


def _run(*args, **kwargs):
    kwargs["ssl_keyfile"] = os.environ["TLS_KEY"]
    kwargs["ssl_certfile"] = os.environ["TLS_CERT"]
    return _orig_run(*args, **kwargs)


uvicorn.run = _run
serve.main(["--allowed-host", "127.0.0.1"])
'''


#: Die **Browser-Seite** der Probe. Sie laeuft im e2e-venv (Playwright), nicht im Dev-venv.
#:
#: **Zwei Laeufe:** der erste mit dem Original, der zweite mit der gepatchten `markdown.js`
#: (der Gegenlauf). Der Server bleibt derselbe — die Zellen pruefen **relativ**.
BROWSER_SKILL = r'''import json, sys, re

base, workdir, variante = sys.argv[1:4]

from playwright.sync_api import sync_playwright


def js_route(route):
    """Die **Gegenlauf-Fassung** der `markdown.js`: die wörtlich-Fallback fehlt."""
    antwort = route.fetch()
    text = antwort.text()
    text, n = re.subn(
        r"return null;(\s*//\s*unbekannte Klasse:[^\n]*)",
        'return "md-c-rot";  // GEGENLAUF: unbekannte Klasse wird nicht wörtlich',
        text, count=1,
    )
    if n != 1:
        route.fulfill(status=500, body="Anker fehlt: " + str(n))
        return
    # Die **Kennung**: ohne sie waere der Gegenlauf blind (Block 11.4, Lehre).
    text = text.replace(
        "export var FORMAT_VOKABULAR = {",
        'window.__p105_markdown_variante = "gegenlauf";\nexport var FORMAT_VOKABULAR = {',
        1,
    )
    route.fulfill(response=antwort, body=text)


out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = context.new_page()
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))
    if variante == "gegenlauf":
        page.route("**/ui/static/js/markdown.js", js_route)

    # Die Login-Seite genuegt: sie ist oeffentlich, und der Import der `markdown.js`
    # braucht nur **dieselbe Origin** (das Modul selbst wird ausgeliefert).
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    out["variante_ausgeliefert"] = page.evaluate(
        "() => window.__p105_markdown_variante || 'original'"
    )

    out["rendern"] = page.evaluate("""async () => {
      const m = await import('/ui/static/js/markdown.js');
      const NL = String.fromCharCode(10);
      const huelle = (html) => { const d = document.createElement('div'); d.innerHTML = html; return d; };
      const q = (s) => huelle(m.markdownToHtml(s, {}));

      const farbe = q('[rot]{.rot}').querySelector('span');
      const groesse = q('[klein]{.klein}').querySelector('span');
      const beides = q('[beides]{.rot .gross}').querySelector('span');
      const fremd = q('[fremd]{.style}');
      const block = q('::: {.zentriert}' + NL + 'Zentriert.' + NL + ':::');
      const html = q('<b>x</b>');
      const code = q('`[x]{.rot}`');
      const keinBlock = q('::: {.zentriert}' + NL + 'offen');

      return {
        span_mit_klasse: farbe ? farbe.className : null,
        span_mit_klassen: beides ? beides.className : null,
        groesse_klasse: groesse ? groesse.className : null,
        unbekannt_woertlich: fremd.querySelector('span') === null
          && fremd.textContent.indexOf('[fremd]{.style}') !== -1,
        unbekannt_html: fremd.innerHTML,
        block_mit_klasse: (function () {
          const d = block.querySelector('div');
          return d ? d.className : null;
        })(),
        kein_block_woertlich: keinBlock.querySelector('div') === null
          && keinBlock.textContent.indexOf('::: {.zentriert}') !== -1,
        html_woertlich: html.querySelector('b') === null && html.textContent === '<b>x</b>',
        codespan_unformatiert: code.querySelector('span') === null
          && code.querySelector('code') !== null
          && code.textContent === '[x]{.rot}',
      };
    }""")

    # -- Die Werkzeugleiste (die **ausgelieferte** `app.html`) -----------------------
    # **Nicht** die Seite selbst laden: das `app.js` loest den Editor beim Start **aus**
    # dem DOM (`detachable()` — P5-AJ), und die Felder waeren dann weg. Also den Quelltext
    # **holen** und mit `DOMParser` lesen — der Parser fuehrt **kein** Skript aus.
    out["werkzeugleiste"] = page.evaluate("""async () => {
      const antwort = await fetch('/ui/static/app.html');
      const html = await antwort.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const felder = {
        farbe: doc.getElementById('format-farbe'),
        groesse: doc.getElementById('format-groesse'),
        ausrichtung: doc.getElementById('format-ausrichtung'),
      };
      const werte = (el) => el ? Array.from(el.options).map(function (o) { return o.value; })
        .filter(function (v) { return v !== ''; }) : null;
      return {
        status: antwort.status,
        vorhanden: Object.keys(felder).every(function (k) { return !!felder[k]; }),
        farbe: werte(felder.farbe),
        groesse: werte(felder.groesse),
        ausrichtung: werte(felder.ausrichtung),
      };
    }""")
    out["seitenfehler"] = fehler

print(json.dumps(out, ensure_ascii=False))
'''


def _provision(space: str) -> dict:
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-markdown-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode("ascii"), key=dek, aad=space.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    return {"space": space, "password": password, "secret": secret_b32}


def _setup() -> dict:
    shutil.rmtree(WEGWERF_ROOT, ignore_errors=True)
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
    os.chmod(DEK_FILE, 0o600)
    alpha = _provision(SPACE)
    # Der Seed: **ein** Item mit allen Formen der Konvention.
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=True)\n"
        f"it = s.create({SPACE!r}, type='note', title='Format-Item', body={BODY!r})\n"
        "print(it.id)\n"
    )
    ergebnis = subprocess.run(
        [".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")},
        capture_output=True, text=True,
    )
    alpha["item_id"] = ergebnis.stdout.strip().splitlines()[-1]
    return alpha


def _serve() -> subprocess.Popen:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = BASE
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["REPO_ROOT"] = str(REPO_ROOT)
    env["TLS_KEY"] = str(TLS_KEY)
    env["TLS_CERT"] = str(TLS_CERT)
    if not (TLS_KEY.exists() and TLS_CERT.exists()):
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(TLS_KEY),
             "-out", str(TLS_CERT), "-days", "2", "-nodes", "-subj", "/CN=127.0.0.1",
             "-addext", "subjectAltName=IP:127.0.0.1"],
            check=True, capture_output=True,
        )
    launcher = WEGWERF_ROOT / "serve_tls.py"
    launcher.write_text(SERVE_TLS_LAUNCHER, encoding="utf-8")
    log_file = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", str(launcher)],
        env=env, cwd=str(REPO_ROOT), stdout=log_file, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    ctx = ssl._create_unverified_context()
    for _ in range(80):
        try:
            urllib.request.urlopen(f"{BASE}/health", timeout=1, context=ctx).read()
            return proc
        except Exception:
            time.sleep(0.25)
    raise SystemExit("Wegwerf-Server wurde nicht gesund.")


def _browserlauf(variante: str) -> dict:
    """Ein Lauf im Browser — entweder mit dem Original oder mit der gepatchten Datei."""
    skript = WEGWERF_ROOT / f"browser_{variante}.py"
    skript.write_text(BROWSER_SKILL, encoding="utf-8")
    out_file = (WEGWERF_ROOT / f"browser_{variante}.out").open("wb")
    err_file = (WEGWERF_ROOT / f"browser_{variante}.err").open("wb")
    subprocess.run(
        ["/home/savefyx/.claude-code-tools/e2e-venv/bin/python", str(skript),
         BASE, str(WEGWERF_ROOT), variante],
        cwd=str(REPO_ROOT), stdout=out_file, stderr=err_file, timeout=300,
    )
    out_file.close()
    err_file.close()
    text = (WEGWERF_ROOT / f"browser_{variante}.out").read_text(encoding="utf-8").strip()
    if not text:
        log("Browser-Fehler:\n" + (WEGWERF_ROOT / f"browser_{variante}.err").read_text(
            encoding="utf-8")[-4000:])
        raise SystemExit(f"Der Browser hat nichts gemeldet ({variante}).")
    return json.loads(text.splitlines()[-1])


def _mcp_get_item(item_id: str) -> dict:
    """Der MCP liest das Item — und liefert den **Rohtext** (der Server kennt die Formate
    nicht; er speichert und liefert, was dasteht)."""
    import asyncio

    import httpx2
    from mcp import Client
    from mcp.client.streamable_http import streamable_http_client

    from authserver.store import AuthStore

    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    # Der **Resource** muss der des Servers sein: `AuthSettings.resource` = `<base_url>/mcp`
    # (der Auth-Server bindet den Token an genau diese Resource — ein anderer Resource
    # ergibt ein Token, das der MCP nicht akzeptiert: **401**, gemessen am 2026-10-25).
    family_id = store.create_family(
        space=SPACE, client_id="p105_b11_markdown", scope="space", resource=BASE + "/mcp"
    )
    token, _refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2592000)

    class _Transport:
        """Der MCP-Transport mit **eigenem** HTTP-Client — der Bearer-Token muss mit.

        (Der SDK-Transport nimmt in dieser Version nur die URL; der `Authorization`-Header
        kommt ueber den HTTP-Client, sonst kaeme der MCP als **anonym** an.)
        """

        def __init__(self, url: str, headers: dict):
            self._url = url
            self._headers = headers
            self._cm = None

        async def __aenter__(self):
            client = httpx2.AsyncClient(
                base_url=BASE, verify=False, headers=self._headers, timeout=60
            )
            self._cm = streamable_http_client(self._url, http_client=client)
            read, write = await self._cm.__aenter__()
            return read, write

        async def __aexit__(self, *args):
            return await self._cm.__aexit__(*args)

    async def _hole() -> str:
        transport = _Transport(BASE + "/mcp", {"Authorization": f"Bearer {token}"})
        async with Client(transport) as client:
            ergebnis = await client.call_tool("get_item", {"item_id": item_id})
            teile = [t.text for t in ergebnis.content if getattr(t, "text", None)]
            return "\n".join(teile)

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        text = asyncio.run(_hole())
    return {"text": text}


def _bewerte(lauf: dict, mcp: dict) -> dict:
    """Die Zellen aus dem Browserlauf und dem MCP-Ergebnis."""
    r = lauf.get("rendern") or {}
    w = lauf.get("werkzeugleiste") or {}
    zellen = {}

    zellen["farbe"] = {
        "erwartet": "md-c-rot", "gemessen": r.get("span_mit_klasse"),
        "ok": r.get("span_mit_klasse") == "md-c-rot",
    }
    zellen["groesse"] = {
        "erwartet": "md-s-klein", "gemessen": r.get("groesse_klasse"),
        "ok": r.get("groesse_klasse") == "md-s-klein",
    }
    zellen["farbe_und_groesse"] = {
        "erwartet": "md-c-rot md-s-gross", "gemessen": r.get("span_mit_klassen"),
        "ok": r.get("span_mit_klassen") == "md-c-rot md-s-gross",
    }
    zellen["unbekannte_klasse_woertlich"] = {
        "erwartet": True, "gemessen": r.get("unbekannt_woertlich"),
        "ok": r.get("unbekannt_woertlich") is True,
        "html": r.get("unbekannt_html"),
    }
    zellen["ausrichtung"] = {
        "erwartet": "md-a-zentriert", "gemessen": r.get("block_mit_klasse"),
        "ok": r.get("block_mit_klasse") == "md-a-zentriert",
    }
    zellen["html_woertlich"] = {
        "erwartet": True, "gemessen": r.get("html_woertlich"),
        "ok": r.get("html_woertlich") is True,
    }
    zellen["codespan_unformatiert"] = {
        "erwartet": True, "gemessen": r.get("codespan_unformatiert"),
        "ok": r.get("codespan_unformatiert") is True,
    }
    zellen["werkzeugleiste"] = {
        "erwartet": {
            "farbe": ["rot", "blau", "gruen", "gelb"],
            "groesse": ["klein", "normal", "gross"],
            "ausrichtung": ["links", "zentriert", "rechts"],
        },
        "gemessen": {"farbe": w.get("farbe"), "groesse": w.get("groesse"),
                     "ausrichtung": w.get("ausrichtung")},
        "ok": (
            w.get("vorhanden") is True
            and w.get("farbe") == ["rot", "blau", "gruen", "gelb"]
            and w.get("groesse") == ["klein", "normal", "gross"]
            and w.get("ausrichtung") == ["links", "zentriert", "rechts"]
        ),
    }
    # Der MCP: der Rohtext kommt **unverändert** zurück.
    text = mcp.get("text") or ""
    formen = [
        "[rot]{.rot}",
        "[klein]{.klein}",
        "[beides]{.rot .gross}",
        "[fremd]{.style}",
        "::: {.zentriert}",
    ]
    fehlend = [f for f in formen if f not in text]
    zellen["mcp_get_item_rohtext"] = {
        "erwartet": "alle Formen woertlich im Text",
        "gemessen": {"fehlend": fehlend, "laenge": len(text)},
        "ok": not fehlend,
    }
    return zellen


def _main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nur-gegenlauf", action="store_true")
    args = ap.parse_args()

    alpha = _setup()
    proc = _serve()
    try:
        normal = _browserlauf("original")
        gegen = _browserlauf("gegenlauf")
        mcp = _mcp_get_item(alpha["item_id"])
    finally:
        # **Nur** die eigene Wegwerf-Instanz, ueber die PID-Datei (Hard Rule 9).
        try:
            pid = int(SERVE_PID.read_text().strip())
            os.kill(pid, 15)
            for _ in range(40):
                time.sleep(0.1)
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    break
        except Exception:
            pass

    zellen = _bewerte(normal, mcp)
    zellen_gegen = _bewerte(gegen, mcp)
    # **Der Gegenlauf bricht genau eine Zelle** — die, die er brechen soll. Alles andere
    # muss grün bleiben, sonst waere er kein Gegenlauf, sondern ein Totalausfall.
    gebrochen = [k for k, v in zellen_gegen.items() if not v["ok"]]
    erwartet_gebrochen = ["unbekannte_klasse_woertlich"]
    varianten_belege = {
        "original": {"ausgeliefert": normal.get("variante_ausgeliefert"),
                     "ist_die_variante": normal.get("variante_ausgeliefert") == "original"},
        "gegenlauf": {"ausgeliefert": gegen.get("variante_ausgeliefert"),
                      "ist_die_variante": gegen.get("variante_ausgeliefert") == "gegenlauf"},
    }
    befund = {
        "zellen": zellen,
        "alle_gruen": all(v["ok"] for v in zellen.values()),
        "gegenlauf": {
            "zellen": zellen_gegen,
            "gebrochen": gebrochen,
            "erwartet_gebrochen": erwartet_gebrochen,
            "bricht_genau_die_erwartete": sorted(gebrochen) == sorted(erwartet_gebrochen),
            "die_anderen_bleiben_gruen": all(
                v["ok"] for k, v in zellen_gegen.items() if k not in erwartet_gebrochen
            ),
        },
        "varianten_belege": varianten_belege,
        "alle_varianten_ausgeliefert": all(
            b["ist_die_variante"] for b in varianten_belege.values()
        ),
        "seitenfehler": normal.get("seitenfehler"),
        "mcp_text_laenge": len(mcp.get("text") or ""),
    }
    RESULT.write_text(json.dumps(befund, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RESULT_GEGENLAUF.write_text(
        json.dumps(zellen_gegen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log(json.dumps({
        "alle_gruen": befund["alle_gruen"],
        "zellen": {k: v["ok"] for k, v in zellen.items()},
        "gegenlauf_gebrochen": gebrochen,
        "bricht_genau_die_erwartete": befund["gegenlauf"]["bricht_genau_die_erwartete"],
    }, ensure_ascii=False, indent=2))
    return 0 if (befund["alle_gruen"] and befund["gegenlauf"]["bricht_genau_die_erwartete"]) else 1


if __name__ == "__main__":
    sys.exit(_main())
