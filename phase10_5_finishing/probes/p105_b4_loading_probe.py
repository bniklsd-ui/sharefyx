#!/usr/bin/env python3
"""P10.5, Block 4, Schritt 4.6 — die Browser-Probe für den Ladezustand (Z2, Z3, Z4).

**Drei Zusagen, drei Messungen** (Plan Block 4, Schritt 4.6):

| Zusage | Was | Wie |
|---|---|---|
| **Z3** | Die Shell steht ≤ 1 s | `DOMContentLoaded` von `/ui/` |
| **Z4** | Der Ladezustand steht **genau ab 200 ms** | Endpunkt 150 ms → **kein** `is-loading`; Endpunkt 400 ms → `is-loading` sichtbar |
| **Z2** | Kein Request wartet hinter `/overview` | `/overview` per Route um 2 s verzögert; Space-Wechsel und Item-Öffnen müssen ≤ 1 s dauern |

**Der Kern von Z4** ist die *Grenze*, nicht das „ja, es gibt einen Ladezustand": ein
Ladezustand, der nach 50 ms auftaucht, flackert bei jedem schnellen Abruf, und einer, der
nach 3 s auftaucht, hilft niemandem. `loading.js` setzt die Klasse deshalb erst nach
`delayMs` (200 ms) — und die Probe misst **beide** Seiten der Grenze.

**Gegenlauf (der eigentliche Beweis):** dieselbe Route, derselbe Ablauf, **ein** Parameter
anders — 150 ms statt 400 ms. Der Platzhalter muss **verschwinden**. Ein Test, der nur
prüft „irgendwann steht ein `is-loading` da", wäre die halbe Wahrheit.

**Warum die asynchrone Playwright-API:** im synchronen API läuft der Route-Handler im
Haupt-Thread — ein `time.sleep(2)` dort würde die **Messung** blockieren, nicht den Server.
Mit `await asyncio.sleep()` im Handler wartet nur der Request.

**Die Wege, an denen der Ladezustand hängt** (Plan §4.4, vier Stellen): Übersicht
(`#list-overview`), Liste (`#list-rows`), Item-Öffnen (`#detail`), Karte (`#overview-graph`).
Die Probe zählt **alle** Elemente mit der Klasse `is-loading` — sie sucht keinen der vier
heraus, damit ein umgehängter Zustand nicht unbemerkt durchrutscht.

**Wegwerf-Instanz:** Port 8799, tmp-`DATA_ROOT`, tmp-`auth.sqlite3` (Plan §2.3). Niemals gegen
den echten `DATA_ROOT`, die echte `auth.sqlite3` oder den Keyring.

**Ausgabe:** genau ein JSON-Objekt auf stdout (Hard Rule 7), Rohwerte als JSON daneben.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import struct
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
BASE = "https://127.0.0.1:8799"
OUT = Path(__file__).with_name("p105_b4_loading.json")

VERZOEGERUNG_S = 2.0        # Z2: das `/overview` hängt 2 s
GRENZE_AKTION_S = 1.0       # Z2: Space-Wechsel und Item-Öffnen ≤ 1 s
SCHNELL_MS = 150            # Z4 (Gegenlauf): unter der Grenze → kein Platzhalter
LANGSAM_MS = 400            # Z4: über der Grenze → Platzhalter sichtbar
GRENZE_Z3_MS = 1000         # Z3: `DOMContentLoaded` ≤ 1 s
FRIST_Z4_SCHNELL_MS = 900   # Z4-Gegenlauf: so lange muss man warten, um sicher zu sein


def totp(uri: str) -> str:
    sec = urllib.parse.parse_qs(urllib.parse.urlparse(uri).query)["secret"][0]
    key = base64.b32decode(sec + "=" * (-len(sec) % 8))
    d = hmac.new(key, struct.pack(">q", int(time.time() // 30)), hashlib.sha1).digest()
    o = d[-1] & 15
    return f"{(struct.unpack('>I', d[o:o + 4])[0] & 0x7FFFFFFF) % 10**6:06d}"


async def login(page, creds) -> None:
    wait = 31 - (int(time.time()) % 30)
    await asyncio.sleep(wait)  # frisches TOTP-Fenster
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', creds["space"])
    await page.fill('input[name="password"]', creds["password"])
    await page.fill('input[name="totp"]', totp(creds["otpauth_uri"]))
    async with page.expect_response("**/ui/login**") as r:
        await page.click('button[type="submit"]')
    response = await r.value
    assert response.status in (200, 303), response.status
    await page.wait_for_selector("button.tree__folder[data-space='alpha']", timeout=60000)


class Verzoegerung:
    """Die `/overview`-Route mit **kontrollierter** Antwortzeit.

    Zwei Feinheiten, die den Unterschied zwischen „gemessen" und „behauptet" machen:

    1. **Ein** Handler fuer alle Faelle — `page.unroute()` waehrend eines laufenden Handlers
       bricht mit „Route is already handled!" ab. Die Wartezeit wird pro Fall umgestellt.
    2. Die Antwort wird **ausgeliefert** (`route.fulfill`), nicht nur verzögert: ein
       `route.continue_()` nach `sleep(N)` haette die Wartezeit **zur Serverzeit addiert**
       (die `/overview` braucht bei 500 Items selbst ~260 ms) — die gemessene Dauer waere
       dann N + Serverzeit und die 200-ms-Grenze waere nicht pruefbar. Der erste Abruf holt
       die echte Antwort, alle folgenden bekommen dieselbe nach genau N Millisekunden.
    """

    def __init__(self) -> None:
        self.sekunden = 0.0
        self._antwort: dict | None = None

    async def handler(self, route) -> None:
        if self.sekunden <= 0:
            await route.continue_()
            return
        await asyncio.sleep(self.sekunden)
        await route.fulfill(**self._antwort)

    async def antwort_fangen(self, page) -> None:
        """Holt die echte Antwort **einmal** ueber den API-Request-Kontext (mit den Cookies
        der Sitzung) — nicht ueber die Route. Sonst waere der **erste** Route-Aufruf der
        Fang: er liefe die volle Serverzeit (bei 500 Items ~260 ms) und damit ueber der
        200-ms-Grenze, ohne dass die eingestellte Verzoegerung ueberhaupt eine Rolle
        gespielt haette. Der erste Fall der Probe waere damit nie die 150-ms-Messung."""
        api_response = await page.request.get(f"{BASE}/api/v1/overview")
        self._antwort = {
            "status": api_response.status,
            "headers": api_response.headers,
            "body": await api_response.body(),
        }


async def _route_installieren(page, verzoegerung: Verzoegerung) -> None:
    await page.route("**/api/v1/overview", verzoegerung.handler)


async def _warte_ohne_loading(page, timeout_ms: int = 5000) -> bool:
    """Wartet, bis kein Element mehr `is-loading` traegt — sonst misst der Z4-Fall nebenbei
    den Ladezustand der Karte (der Graph laedt beim Bootstrap und ist mit 500 Items nicht in
    null Sekunden fertig)."""
    try:
        await page.wait_for_function(
            "() => document.querySelectorAll('.is-loading').length === 0", timeout=timeout_ms
        )
        return True
    except Exception:  # noqa: BLE001 — Timeout heisst: es haengt noch etwas
        return False


async def _zaehle_loading(page) -> list[dict]:
    """Alle Elemente mit der Klasse `is-loading` — und ob sie sichtbar sind."""
    return await page.evaluate(
        """() => Array.from(document.querySelectorAll('.is-loading')).map((el) => {
             const r = el.getBoundingClientRect();
             const s = getComputedStyle(el);
             return {
               id: el.id || el.className,
               sichtbar: r.width > 0 && r.height > 0
                 && s.visibility !== 'hidden' && s.display !== 'none',
             };
           })"""
    )


async def main() -> int:
    creds = json.loads((ROOT / "credentials.json").read_text())["users"][0]
    result: dict = {
        "probe": "p105_b4_loading",
        "datum": time.strftime("%Y-%m-%d"),
        "grenzen": {
            "z2_verzoegerung_s": VERZOEGERUNG_S,
            "z2_grenze_s": GRENZE_AKTION_S,
            "z4_schnell_ms": SCHNELL_MS,
            "z4_langsam_ms": LANGSAM_MS,
            "z3_grenze_ms": GRENZE_Z3_MS,
        },
    }

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": 1440, "height": 900}, ignore_https_errors=True
        )
        page = await ctx.new_page()
        await login(page, creds)

        # -- Z3: die Shell steht in ≤ 1 s --------------------------------------------------
        # Gemessen wird `DOMContentLoaded` — die Shell darf nicht auf dem Server warten.
        t0 = time.perf_counter()
        await page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
        z3_ms = round((time.perf_counter() - t0) * 1000, 1)
        await page.wait_for_selector("button.tree__folder[data-space='alpha']", timeout=60000)
        result["z3_domcontentloaded_ms"] = z3_ms
        result["z3_erfuellt"] = z3_ms <= GRENZE_Z3_MS

        # Die Route wird **einmal** eingaengt und ihre Wartezeit pro Fall umgestellt.
        verzoegerung = Verzoegerung()
        await verzoegerung.antwort_fangen(page)
        await _route_installieren(page, verzoegerung)

        # -- Z4: die Grenze bei 200 ms ------------------------------------------------------
        # Der Ladezustand hängt am **Abruf**, nicht an der Route: deshalb wird hier die
        # Route-Zeit variiert und der Zustand über die Klasse gemessen. Der Auslöser ist der
        # Aktualisieren-Knopf der Übersicht (`loadOverview()` **ohne** die 10-s-Mindestpause
        # des Pollers — der Poller wäre gedrosselt und die Messung würde ins Leere laufen).
        # Der Graph laedt beim Bootstrap (`app.js :: init()` → `loadGraphPanel()`) und ist mit
        # 500 Items nicht in null Sekunden fertig — sonst wuerde der Z4-Fall nebenbei
        # **dessen** Ladezustand messen. `networkidle` wartet auf das Ende **aller**
        # Bootstrap-Anfragen; `_warte_ohne_loading()` allein waere zu frueh, weil der
        # Graph-Abruf erst **nach** `/items` startet und die Klasse vorher noch gar nicht
        # gesetzt ist.
        await page.wait_for_load_state("networkidle", timeout=60000)
        await _warte_ohne_loading(page, 10000)

        result["z4"] = {}
        for label, ms, erwartet in (
            ("schnell", SCHNELL_MS, False),
            ("langsam", LANGSAM_MS, True),
        ):
            verzoegerung.sekunden = ms / 1000.0
            # Der Ausloeser ist der **Poll** (ein `focus`-Event) — derselbe Weg, den die
            # Oberflaeche im Betrieb nimmt. Der Aktualisieren-Knopf waere ungeeignet: er holt
            # zugleich die Karte (`loadGraphPanel({force: true})`), und die Karte hat ihre
            # eigene Ladezustandsstelle.
            await page.evaluate("window.dispatchEvent(new Event('focus'))")
            try:
                await page.wait_for_selector(
                    ".is-loading", state="attached", timeout=FRIST_Z4_SCHNELL_MS
                )
                erschienen = True
            except Exception:  # noqa: BLE001 — Timeout ist hier das erwartete Ergebnis
                erschienen = False
            zustand = await _zaehle_loading(page)
            sichtbar = any(z["sichtbar"] for z in zustand)
            result["z4"][label] = {
                "verzoegerung_ms": ms,
                "is_loading_erschienen": erschienen,
                "is_loading": zustand,
                "sichtbar": sichtbar,
                "erwartet_sichtbar": erwartet,
                "erfuellt": sichtbar == erwartet,
            }
            # Der Aufruf muss durch sein, bevor der naechste Fall startet (sonst haengt der
            # vorherige Request noch in der Route).
            await asyncio.sleep(0.5)
            # **Die Mindestpause des Pollers (10 s, PF-4):** der zweite Fall darf den Poll
            # nicht schlucken. Das ist die wartezeit, die die Pause dem Menschen erspart — sie
            # steht hier als Kosten der Probe im Klartext.
            if label == "schnell":
                await asyncio.sleep(11.0)

        result["z4_grenze_erfuellt"] = all(case["erfuellt"] for case in result["z4"].values())

        # -- Z2: ein hängendes `/overview` darf keine andere Aktion blockieren ----------------
        verzoegerung.sekunden = VERZOEGERUNG_S
        t1 = time.perf_counter()
        await page.locator("button.tree__folder[data-space='alpha'][data-bucket]").first.click()
        await page.wait_for_selector("button.list__row[data-id]", timeout=60000)
        z2_raumwechsel_s = round(time.perf_counter() - t1, 3)
        result["z2_raumwechsel_s"] = z2_raumwechsel_s
        result["z2_raumwechsel_erfuellt"] = z2_raumwechsel_s <= GRENZE_AKTION_S

        # Item öffnen, während das `/overview` hängt: der Klick darf nicht warten.
        t2 = time.perf_counter()
        await page.locator("button.list__row[data-id]").first.click()
        await page.wait_for_selector(
            "#detail-editor:not([hidden]), #detail-readonly:not([hidden])", timeout=60000
        )
        z2_item_s = round(time.perf_counter() - t2, 3)
        result["z2_item_oeffnen_s"] = z2_item_s
        result["z2_item_oeffnen_erfuellt"] = z2_item_s <= GRENZE_AKTION_S
        result["z2_erfuellt"] = (
            result["z2_raumwechsel_erfuellt"] and result["z2_item_oeffnen_erfuellt"]
        )

        await browser.close()

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
