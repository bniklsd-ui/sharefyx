#!/usr/bin/env python3
"""P10.5 Block 18, Schritt 18.5 — die Live-Zeilen **P10.5-18** und **P10.5-49** als Wegwerf-Probe.

Plan: `docs/concepts/phase10_5_block18_live_fixes_plan.md` §3 (Schritt 18.5), §4 (E4). Nikinger
2026-11-01: „die Live-Zeilen werden Wegwerf-Proben — automatisch und bleibend; Netzwerk-Werkzeuge
beim Testen (lokaler Caddy) sind erlaubt".

| Zeile | Was | gruen, wenn |
|---|---|---|
| **P10.5-18a** (`waiting`) | `/api/v1/overview`, Browser, `PerformanceResourceTiming.responseStart - requestStart` (zehn Abrufe) | **groesster** Wert <= 300 ms |
| **P10.5-18b** (`wechsel`) | Klick auf einen Space **waehrend** ein `/overview`-Abruf laeuft (Knopf „aktualisieren") bis die erste Listenzeile steht, fuenfmal | **groesster** Wert <= 1000 ms |
| **P10.5-49** (`ereignis`) | zwei Browser-Kontexte, eine Sitzung: der eine **schreibt** (`POST /api/v1/items`), im anderen kommt das `changed`-Ereignis an **und** die Zeile steht da, fuenfmal | **groesster** Wert <= 2000 ms, alle fuenf angekommen |

**Beide Eingaenge** (Plan §3, 18.5): `direkt` = Loopback-TLS auf den Dienst (so zeigt der Funnel auf
den Dienst, `phase3_edge/`) und `caddy` = ein **lokaler Caddy 2.6.2** (die Live-Version, V199) davor,
Konfiguration nach `phase9_hardening/step_a/Caddyfile.template` (Upstream-Block mit `dial_timeout`,
`lb_try_*`); statt Let's-Encrypt-Domain `tls internal` auf `127.0.0.1:<port>`. `SPACE_PUBLIC_BASE_URL`
steht je Eingang auf **dessen** Adresse (`require_csrf` vergleicht den Origin damit) — darum zwei
Serverlaeufe nacheinander, nicht einer mit zwei Toren.

**Wegwerf-Instanz** (Root-`CLAUDE.md`): freier Port je Lauf, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, TLS,
bereinigte Umgebung, Stopp **nur** ueber PID/`Popen` der eigenen Prozesse (Hard Rule 9). Server, Konto und
Saat (263 Items, 5 Spaces) kommen aus den Bloecken 14/18 (`p105_b14_layout_probe.py`,
`p105_b18_karte_messung.py`, als Module geladen — eine Quelle, keine Kopie). Caddy-Binary:
`~/.claude-code-tools/caddy/caddy` (v2.6.2, Release-Archiv von github.com/caddyserver/caddy).

**Gegenlaeufe** (`--gegenlauf=NAME`, schreiben in `p105_b18_live_zeilen_gegenlauf_NAME.json`):

| Name | Eingriff | muss rot machen |
|---|---|---|
| `poll` | der Start-Wrapper haelt die Ereignisschleife bei jedem `/overview` 600 ms an (das Bild des Staus hinter dem eigenen Poll, Z2) | `waiting` **und** `wechsel` |
| `stream` | der Start-Wrapper verzoegert jedes Stueck des Ereignis-Streams um 3 s | `ereignis` |
| `caddy_puffer` | nur Eingang `caddy`: `buffer_responses` im `reverse_proxy` (ein Proxy, der Antworten sammelt) | `ereignis` (kommt nie an); `waiting` rot als Nebenwirkung |

`poll` macht ausserdem `ereignis` rot (am Eingang `caddy`): die angehaltene Schleife verzoegert auch das Nachladen
nach dem Ereignis — gemessen, nicht gewollt. `stream` laeuft an **beiden** Eingaengen und macht **nur** `ereignis` rot.

**Befund (2026-11-02):** der Plan nannte „Caddy mit `flush_interval` aus ⇒ 49 rot". Mit Caddy 2.6.2 gemessen: `encode gzip`
**und** `flush_interval 30s` zusammen puffern den Stream **nicht** (`ereignis` blieb gruen, 0,1–1,0 s). Vermutete Ursache
(Schluss, nicht nachgelesen): Go's `ReverseProxy` spuelt `text/event-stream`/chunked-Antworten immer sofort. Ein echter
Puffer in 2.6.2 ist `buffer_responses` (`caddy validate` nimmt ihn) — das ist der Gegenlauf `caddy_puffer`.

**Abweichungen vom Betrieb (datiert 2026-11-02, ohne Einfluss auf die Aussage):** (1) Betrieb: die App spricht **Klartext-http** auf
127.0.0.1:8765, davor der Funnel bzw. Caddy → socat-Relay (`phase3_edge/CLAUDE.md`, `sharefyx-tail-proxy.service`); die Wegwerf-
Instanz spricht **TLS** (`require_csrf()` verlangt https), also geht Caddy per `https` + `tls_insecure_skip_verify` zum Upstream.
(2) Der Probe-Caddy hat `admin off` — die Vorlage lehnt das fuer den Dienst ausdruecklich ab (`systemctl reload` braucht die
Admin-API); fuer einen Wegwerf-Lauf ohne Reload gleichgueltig. (3) `skip_install_trust`: sonst versucht `tls internal`, die
Wurzel ins System-/NSS-Verzeichnis zu schreiben (nachgesehen: nichts ausserhalb `/tmp` entstanden).

Aufruf:   `.venv/bin/python phase10_5_finishing/probes/p105_b18_live_zeilen_probe.py [--gegenlauf=NAME]`
Ergebnis: `phase10_5_finishing/probes/p105_b18_live_zeilen.json`
"""
from __future__ import annotations

import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
RESULT = HIER / "p105_b18_live_zeilen.json"

CADDY = Path.home() / ".claude-code-tools/caddy/caddy"
E2E = Path.home() / ".claude-code-tools/e2e-venv/bin/python"

WAITING_MAX_MS = 300      # P10.5-18
WECHSEL_MAX_MS = 1000     # P10.5-18
EREIGNIS_MAX_MS = 2000    # P10.5-49 (Frist wie P10.5-46)
N_WAITING = 10
N_WECHSEL = 5
N_EREIGNIS = 5

GEGENLAEUFE = ("poll", "stream", "caddy_puffer")
GEGENLAUF = None
for _a in sys.argv[1:]:
    if _a.startswith("--gegenlauf="):
        GEGENLAUF = _a.split("=", 1)[1]
        if GEGENLAUF not in GEGENLAEUFE:
            raise SystemExit("unbekannter Gegenlauf: %s (erlaubt: %s)" % (GEGENLAUF, ", ".join(GEGENLAEUFE)))

# -- b14/b18 als Module laden (ohne ihre Kommandozeile zu erben) ----------------------------------
_argv = sys.argv
sys.argv = [_argv[0]]
for _name, _datei in (("p105_b14_layout_probe", "p105_b14_layout_probe.py"),
                      ("p105_b18_karte_messung", "p105_b18_karte_messung.py")):
    _spec = importlib.util.spec_from_file_location(_name, HIER / _datei)
    globals()[_name] = importlib.util.module_from_spec(_spec)
    sys.modules[_name] = globals()[_name]
    _spec.loader.exec_module(globals()[_name])
sys.argv = _argv
b14 = p105_b14_layout_probe
b18 = p105_b18_karte_messung
REPO_ROOT = b14.REPO_ROOT

# -- der Start-Wrapper fuer die Gegenlaeufe ---------------------------------------------------------
# Er haengt sich **hinter** den Produktivaufbau (`AccessLogASGI(OAuthLogASGI(app))`) und tut ohne die
# Umgebungsvariablen nichts. Er steht in der Wegwerf-Kopie des Starters, nie im Produktcode.
WRAPPER = '''
_slow_ov = int(os.environ.get("PROBE_SLOW_OVERVIEW_MS", "0"))
_slow_st = int(os.environ.get("PROBE_SLOW_STREAM_MS", "0"))
if _slow_ov or _slow_st:
    import asyncio, time as _time
    _inner = app
    async def app(scope, receive, send):
        if scope["type"] == "http":
            pfad = scope["path"]
            if _slow_ov and pfad == "/api/v1/overview":
                _time.sleep(_slow_ov / 1000.0)      # blockiert die Ereignisschleife -- Absicht (Stau)
            if _slow_st and pfad == "/api/v1/events":
                async def _send(msg):
                    if msg["type"] == "http.response.body":
                        await asyncio.sleep(_slow_st / 1000.0)
                    await send(msg)
                return await _inner(scope, receive, _send)
        return await _inner(scope, receive, send)
'''
ANKER = "app = AccessLogASGI(OAuthLogASGI(app))\n"
if ANKER not in b14.SERVE_TLS_LAUNCHER:
    raise SystemExit("Anker des Starters nicht gefunden -- b14.SERVE_TLS_LAUNCHER hat sich geaendert")
b14.SERVE_TLS_LAUNCHER = b14.SERVE_TLS_LAUNCHER.replace(ANKER, ANKER + WRAPPER)

# -- Caddy ----------------------------------------------------------------------------------------


def caddyfile(cport: int, upstream_port: int, puffer: bool = False) -> str:
    """Die Vorlage `phase9_hardening/step_a/Caddyfile.template`, auf Loopback gebogen: dieselbe
    `reverse_proxy`-Form (Upstream-Block mit `dial_timeout`, `lb_try_*`), `tls internal` statt ACME."""
    return (
        "{\n\tadmin off\n\tauto_https disable_redirects\n\tlocal_certs\n\tskip_install_trust\n}\n\n"
        "127.0.0.1:%d {\n\ttls internal\n"
        "\treverse_proxy https://127.0.0.1:%d {\n\t\ttransport http {\n\t\t\tdial_timeout 10s\n"
        "\t\t\ttls_insecure_skip_verify\n\t\t}\n\t\tlb_try_duration 15s\n\t\tlb_try_interval 1s\n%s\t}\n}\n"
    ) % (cport, upstream_port, "\t\tbuffer_responses\n" if puffer else "")


def caddy_start(cport: int, upstream_port: int) -> subprocess.Popen:
    wurzel = b14.WEGWERF_ROOT
    datei = wurzel / ("Caddyfile-%d" % b14.PID)
    datei.write_text(caddyfile(cport, upstream_port, GEGENLAUF == "caddy_puffer"), encoding="utf-8")
    env = b14._saubere_umgebung()
    env["XDG_DATA_HOME"] = str(wurzel / ("caddy-data-%d" % b14.PID))      # Zertifikatsspeicher bleibt in /tmp
    env["XDG_CONFIG_HOME"] = str(wurzel / ("caddy-cfg-%d" % b14.PID))
    pruef = subprocess.run([str(CADDY), "validate", "--config", str(datei), "--adapter", "caddyfile"],
                           env=env, capture_output=True, text=True)
    if pruef.returncode != 0:
        raise SystemExit("caddy validate:\n" + pruef.stderr[-1500:])
    log = (wurzel / ("caddy-%d.log" % b14.PID)).open("ab")
    return subprocess.Popen([str(CADDY), "run", "--config", str(datei), "--adapter", "caddyfile"],
                            env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def caddy_stop(proc: subprocess.Popen | None) -> None:
    """Stopp ueber das eigene `Popen` (Hard Rule 9: nie ein Muster im Cmdline)."""
    if proc is None or proc.poll() is not None:
        return
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


# -- Browser-Teil -----------------------------------------------------------------------------------

BROWSER_MAIN = r'''
def median(xs):
    s = sorted(xs)
    return s[len(s) // 2] if s else None


EVENTSOURCE = """
(function () {
  const Orig = window.EventSource;
  function Patched(url, opts) {
    const es = new Orig(url, opts);
    window.__es = es;
    window.__changed = 0;
    window.__changedAt = [];
    es.addEventListener("changed", function () { window.__changed++; window.__changedAt.push(Date.now()); });
    return es;
  }
  Patched.OPEN = Orig.OPEN; Patched.CONNECTING = Orig.CONNECTING; Patched.CLOSED = Orig.CLOSED;
  window.EventSource = Patched;
})();
"""


def main():
    out = {"eingang": AUFTRAG["eingang"], "base": BASE}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx_a = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
        ctx_a.add_init_script(EVENTSOURCE)
        # Das Film-Startbild (Block 17) liegt sonst ueber der frischen Instanz (Muster: b18-Messung).
        ctx_a.add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")
        a = ctx_a.new_page()
        fehler = []
        a.on("pageerror", lambda exc: fehler.append(str(exc)))
        login(a)
        a.wait_for_timeout(1500)

        # -- P10.5-18a: Waiting von /api/v1/overview -----------------------------------------------
        a.evaluate("() => performance.clearResourceTimings()")
        waiting = []
        for i in range(AUFTRAG["n_waiting"]):
            wert = a.evaluate("""async (i) => {
              await fetch('/api/v1/overview?probe=' + i, {credentials: 'same-origin'}).then(r => r.text());
              const e = performance.getEntriesByType('resource').filter(x => x.name.indexOf('/api/v1/overview?probe=' + i) !== -1).pop();
              return e ? {waiting: e.responseStart - e.requestStart, total: e.responseEnd - e.startTime} : null;
            }""", i)
            waiting.append(wert)
            a.wait_for_timeout(150)
        out["waiting_ms"] = [round(w["waiting"], 1) for w in waiting if w]
        out["gesamt_ms"] = [round(w["total"], 1) for w in waiting if w]

        # -- P10.5-18b: Space-Wechsel waehrend ein /overview laeuft ---------------------------------
        a.wait_for_selector(".overview__space-open", timeout=20000)
        wechsel = []
        zaehler = []
        for i in range(AUFTRAG["n_wechsel"]):
            a.click("#home-button")
            a.wait_for_selector(".overview__space-open", timeout=20000)
            a.wait_for_timeout(500)
            # `epsilon` (ein Item, eine Notiz) hat unter „Offen" keine Zeile -- er taugt nicht als Ziel.
            namen = a.locator(".overview__space-name-label").all_inner_texts()
            kandidaten = [k for k, nm in enumerate(namen) if nm.strip() != "epsilon"]
            ziel = a.locator(".overview__space-open").nth(kandidaten[i % len(kandidaten)])
            # Die Zeilen des **vorigen** Space stehen noch im DOM -- gewartet wird auf eine Zeile des
            # **Ziel**-Space (Titel der Saat: "<Space> 001"), sonst misst man den alten Stand.
            name = ziel.locator(".overview__space-name-label").inner_text().strip().capitalize()
            # Der Abruf laeuft los (Knopf), und **ohne Wartezeit** folgt der Klick auf den Space.
            a.evaluate("""(name) => { window.__t0 = performance.now(); window.__zeile = null;
              const tick = () => {
                const hit = Array.from(document.querySelectorAll('.list__row')).some(r => r.textContent.indexOf(name + ' ') !== -1);
                if (hit) { window.__zeile = performance.now(); } else { requestAnimationFrame(tick); } };
              document.getElementById('overview-refresh').click(); window.__tick = tick; }""", name)
            ziel.click()
            a.evaluate("() => window.__tick()")
            try:
                a.wait_for_function("() => window.__zeile !== null", timeout=15000)
            except Exception:
                print("WECHSEL-TIMEOUT name=%r zustand=%r zeilen=%r" % (name, a.evaluate(
                    "() => ({view: document.getElementById('shell').dataset.view, buttons: document.querySelectorAll('.overview__space-open').length, "
                    "url: location.href, rowsAll: document.querySelectorAll('.list__row').length, listText: (document.getElementById('list')||document.body).innerText.slice(0,200)})"), a.evaluate(
                    "() => Array.from(document.querySelectorAll('.list__row')).slice(0, 3).map(r => r.textContent.trim().slice(0, 60))")),
                    file=sys.stderr)
                raise
            wechsel.append(round(a.evaluate("() => window.__zeile - window.__t0"), 1))
            zaehler.append(a.locator(".list__row").count())
            a.wait_for_timeout(300)
        out["wechsel_ms"] = wechsel
        out["wechsel_zeilen"] = zaehler

        # -- P10.5-49: zwei Kontexte, eine Sitzung --------------------------------------------------
        a.click("#home-button")
        a.wait_for_selector(".overview__space-open", timeout=20000)
        a.locator(".overview__space-open").first.click()
        a.wait_for_selector(".list__row", timeout=20000)
        a.wait_for_timeout(1000)
        cookies = ctx_a.cookies()
        csrf = a.evaluate("() => sessionStorage.getItem('sfx:csrf')")
        ctx_b = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
        ctx_b.add_cookies(cookies)
        ctx_b.add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")
        ctx_b.add_init_script("sessionStorage.setItem('sfx:csrf', %s);" % json.dumps(csrf))
        b = ctx_b.new_page()
        b.on("pageerror", lambda exc: fehler.append("B: " + str(exc)))
        b.goto(BASE + "/ui/", wait_until="domcontentloaded")
        b.wait_for_selector("#shell", timeout=30000)
        b.wait_for_timeout(1500)
        out["stream_a"] = a.evaluate("() => window.__es ? window.__es.readyState : -1")
        ereignis = []
        for i in range(AUFTRAG["n_ereignis"]):
            titel = "Probe-Ereignis-%d-%d" % (int(time.time()), i)
            a.evaluate("""(t) => { window.__neu = null; window.__vorher = window.__changedAt.length;
              const timer = setInterval(function () {
                const hit = Array.from(document.querySelectorAll('.list__row')).find(r => r.textContent.indexOf(t) !== -1);
                if (hit) { window.__neu = Date.now(); clearInterval(timer); }
              }, 20); }""", titel)
            t0 = b.evaluate("""async (titel) => {
              const t0 = Date.now();
              const r = await fetch('/api/v1/items', {method: 'POST', credentials: 'same-origin',
                headers: {'Content-Type': 'application/json', 'X-CSRF-Token': sessionStorage.getItem('sfx:csrf')},
                body: JSON.stringify({type: 'task', title: titel, body: 'Wegwerf'})});
              return {t0: t0, status: r.status};
            }""", titel)
            erreicht = True
            try:
                a.wait_for_function("() => window.__neu !== null", timeout=8000)
            except Exception:
                erreicht = False
            sicht = a.evaluate("() => window.__neu")
            ev = a.evaluate("() => window.__changedAt.slice(window.__vorher)")
            ereignis.append({
                "titel": titel, "status": t0["status"],
                "ereignis_ms": (ev[0] - t0["t0"]) if ev else None,
                "zeile_ms": (sicht - t0["t0"]) if sicht else None, "angekommen": erreicht and bool(ev),
            })
            a.wait_for_timeout(300)
        out["ereignisse"] = ereignis
        out["seitenfehler"] = fehler
        browser.close()
    Path(AUFTRAG["result"]).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False)[:3000])


main()
'''


def browser_skript() -> str:
    kopf = b14.BROWSER_SKILL.split("\ndef main():\n", 1)[0]
    return kopf + BROWSER_MAIN


def ein_eingang(eingang: str, creds: dict) -> dict:
    """Ein Serverlauf (frische Saat, frischer Port) + optional Caddy davor + der Browser-Teil."""
    items = b18.spec()
    b14.PORT = b14._freier_port()
    caddy = None
    if eingang == "caddy":
        cport = b14._freier_port()
        b14.BASE = "https://127.0.0.1:%d" % cport     # die Adresse, die der Browser sieht -- und die CSRF vergleicht
        caddy = caddy_start(cport, b14.PORT)
    else:
        b14.BASE = "https://127.0.0.1:%d" % b14.PORT
    b18.seed(items)
    resultat = HIER / ("p105_b18_live_zeilen_%s_roh_%d.json" % (eingang, b14.PID))
    try:
        # b14._serve prueft /health unter b14.BASE -- beim Caddy-Eingang also **durch** Caddy.
        b14._serve()
        auftrag = {
            "base": b14.BASE, "space": b14.SPACE, "password": creds["password"], "secret": creds["secret"],
            "repo_root": str(REPO_ROOT), "auth_db": str(b14.AUTH_DB), "result": str(resultat),
            "wachser_space": "epsilon", "extra_items": 0, "pid": b14.PID, "spaces": b18.SPACES,
            "eingang": eingang, "n_waiting": N_WAITING, "n_wechsel": N_WECHSEL, "n_ereignis": N_EREIGNIS,
        }
        b14.AUFTRAG_DATEI.write_text(json.dumps(auftrag), encoding="utf-8")
        skript = b14.WEGWERF_ROOT / ("browser_b18_5_%d.py" % b14.PID)
        skript.write_text(browser_skript(), encoding="utf-8")
        proc = subprocess.run([str(E2E), str(skript), str(b14.AUFTRAG_DATEI)], cwd=str(REPO_ROOT),
                              capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            print(proc.stdout[-3000:], proc.stderr[-4000:], file=sys.stderr)
            raise SystemExit("Browser-Teil (%s) fehlgeschlagen" % eingang)
    finally:
        b14._stop()
        caddy_stop(caddy)
    roh = json.loads(resultat.read_text(encoding="utf-8"))
    resultat.unlink()
    return roh


def zellen(roh: dict) -> dict:
    ev = roh["ereignisse"]
    return {
        "waiting": max(roh["waiting_ms"]) <= WAITING_MAX_MS and len(roh["waiting_ms"]) == N_WAITING,
        "wechsel": max(roh["wechsel_ms"]) <= WECHSEL_MAX_MS and all(n > 0 for n in roh["wechsel_zeilen"]),
        "ereignis": (len(ev) == N_EREIGNIS and all(e["angekommen"] and e["status"] == 201 for e in ev)
                     and max(e["ereignis_ms"] for e in ev if e["ereignis_ms"] is not None) <= EREIGNIS_MAX_MS
                     and max(e["zeile_ms"] for e in ev if e["zeile_ms"] is not None) <= EREIGNIS_MAX_MS),
    }


def main() -> int:
    if not CADDY.exists():
        raise SystemExit("Caddy fehlt: %s (v2.6.2 aus dem GitHub-Release-Archiv dort ablegen)" % CADDY)
    version = subprocess.run([str(CADDY), "version"], capture_output=True, text=True).stdout.split()[0]
    if GEGENLAUF == "poll":
        os.environ["PROBE_SLOW_OVERVIEW_MS"] = "600"
    elif GEGENLAUF == "stream":
        os.environ["PROBE_SLOW_STREAM_MS"] = "3000"
    creds = b14._setup()
    eingaenge = ["caddy"] if GEGENLAUF == "caddy_puffer" else ["direkt", "caddy"]
    beleg = {"caddy_version": version, "gegenlauf": GEGENLAUF, "saat_items": len(b18.spec()),
             "schwellen_ms": {"waiting": WAITING_MAX_MS, "wechsel": WECHSEL_MAX_MS, "ereignis": EREIGNIS_MAX_MS},
             "eingaenge": {}}
    for e in eingaenge:
        roh = ein_eingang(e, creds)
        roh["zellen"] = zellen(roh)
        beleg["eingaenge"][e] = roh
        print(e, roh["zellen"], "waiting max", max(roh["waiting_ms"]), "wechsel max", max(roh["wechsel_ms"]),
              "ereignis", [x["ereignis_ms"] for x in roh["ereignisse"]], file=sys.stderr)
    beleg["zellen"] = {z: all(v["zellen"][z] for v in beleg["eingaenge"].values())
                       for z in ("waiting", "wechsel", "ereignis")}
    ziel = RESULT if not GEGENLAUF else HIER / ("p105_b18_live_zeilen_gegenlauf_%s.json" % GEGENLAUF)
    ziel.write_text(json.dumps(beleg, indent=1, ensure_ascii=False), encoding="utf-8")
    print("ZELLEN:", beleg["zellen"], "| Gegenlauf:", GEGENLAUF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
