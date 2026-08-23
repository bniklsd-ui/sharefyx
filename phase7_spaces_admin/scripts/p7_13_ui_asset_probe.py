#!/usr/bin/env python3
"""P6.5-8-Teilprobe (Web-UI-Fläche statt Browser-Klick): `testnutzer-p7` loggt sich über
`/ui/login` ein (Cookie-Session, P5-D), holt den Asset-Bytes-Endpunkt eines ihm per
`share_write` freigegebenen fremden Bildes ab (erwartet: `200`, echte Bytes) — danach dieselbe
URL ganz ohne Session (erwartet: kein Zugriff).

**Bewusst kein `claude-in-chrome`-Klick-Nachweis dieser Sitzung:** die Login-Form-Werte
(Passwort/TOTP) aus `testcred.py` in eine `computer`-Type-Aktion zu tippen hätte sie in den
sichtbaren Werkzeugaufruf-Verlauf dieser Sitzung geschrieben — genau die Klartext-Exposition,
die Hard Rule 1 vermeiden soll (`testcred.py`s eigener Docstring: „ein Geheimnis gehört nie in
eine Antwort"). Dieses Skript erreicht denselben HTTP-Endpunkt, den ein Browser auch anspricht,
ohne dass ein Geheimnis je in einer für Claude Code sichtbaren Antwort auftaucht — dieselbe
Disziplin wie `p7_10_write_probe.py`/`p7_13_asset_share_gate_probe.py`, nur gegen `/ui/login`
statt `/oauth/authorize`. Ein echter Browser-Render-Beweis (Bild sichtbar im DOM) bleibt damit
für diese Probe ehrlich offen, wie schon P7-1/P7-5 in dieser Phase.
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

import httpx

from authserver import totp as totp_mod

BASE_URL = "https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net"
SPACE = "testnutzer-p7"


def _load_testcred():
    script_path = Path(__file__).with_name("testcred.py")
    spec = importlib.util.spec_from_file_location("testcred", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def run(testcred, item_id: str, asset_id: str) -> dict:
    creds = testcred._load()
    if creds is None:
        raise SystemExit("ABBRUCH: kein testcred-Eintrag — erst 'testcred.py store' laufen lassen.")
    password = creds["password"]
    totp_secret = creds["totp_secret"]

    asset_url = f"/api/v1/items/{item_id}/assets/{asset_id}"

    # Unauthentifizierter Zugriff zuerst, in einem eigenen Client ohne Cookie-Jar.
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as anon:
        anon_resp = await anon.get(asset_url)
        anon_status = anon_resp.status_code

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        totp_code = totp_mod.totp_at(totp_secret, int(time.time()) // 30)
        login_resp = await client.post(
            "/ui/login",
            data={"space": SPACE, "password": password, "totp": totp_code},
        )
        login_resp.raise_for_status()
        match = re.search(r'name="csrf"[^>]*value="([^"]+)"', login_resp.text)
        # `csrf_token` steht nur zum Beweis der Login-Route im Body, wird hier nicht weiter
        # gebraucht (ein reines GET auf den Asset-Endpunkt ist nicht CSRF-geschützt, nur
        # zustandsändernde POST/PATCH/DELETE sind es, P5-H).
        logged_in = match is not None

        authed_resp = await client.get(asset_url)
        authed_status = authed_resp.status_code
        authed_content_type = authed_resp.headers.get("content-type")
        authed_bytes = len(authed_resp.content)

    return {
        "logged_in": logged_in,
        "anonymous_status": anon_status,
        "authenticated_status": authed_status,
        "authenticated_content_type": authed_content_type,
        "authenticated_bytes": authed_bytes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_13_ui_asset_probe",
        description="testnutzer-p7 holt ein Asset über /ui-Cookie-Session, mit/ohne Session.",
    )
    parser.add_argument("item_id")
    parser.add_argument("asset_id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    testcred = _load_testcred()
    result = asyncio.run(run(testcred, args.item_id, args.asset_id))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
