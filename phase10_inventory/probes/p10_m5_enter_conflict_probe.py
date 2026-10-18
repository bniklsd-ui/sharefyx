#!/usr/bin/env python3
"""M5 (P10-Plan §4, Register BG-2/BG-3): halten P9-124 und P9-127 im Browser?

**BG-2 (P9-124 ⚠️ — Konfliktkopie nie im Browser gefahren):** `dialogs.js:1079` setzt
`payload.space = state.conflictCurrent.space` (P9-BI) — die Kopie aus „Meine Fassung als
neues Item anlegen" soll im Space des Konflikt-Items landen, nicht still im Home-Space.
Gemessen wird der **Request**: Konflikt an einem Item in `gamma` (Team-Space, schreibbar),
dann POST `/api/v1/items` — `body["space"] == "gamma"` und die Antwort trägt denselben Space.
**Gegenläufe:** (a) derselbe Konflikt, aber „Aktuelle Fassung laden" — es darf **kein** POST
firen (die Schwester-Route ist Laden, nicht Kopieren); (b) der Konflikt-Dialog ist laut
`app.js :: enterTable()` bewusst von Enter **ausgenommen** (zwei gleichrangige Wege) — Enter
bei offenem Dialog darf nichts auslösen.

**BG-3 (P9-127 ⚠️ — Enter nur für vier von elf Overlays belegt):** die Enter-Tabelle
(`app.js:252`) mappt neun erreichbare Ziele (Konflikt- und Link-Picker-Dialog sind bewusst
`null`); die Einstellungen-Kette trägt drei Unterregeln (`SETTINGS_ENTER`). Diese Probe fährt
**alle** in der Wegwerf-Instanz erreichbaren Stationen im echten Chromium — jede mit
Gegenlauf (falsches Feld, leeres Feld oder abgebrochener Weg ⇒ die Primäraktion darf **nicht**
firen):

| Station | Positiv (Enter → Aktion) | Gegenlauf |
|---|---|---|
| create | Titel + Enter → POST /items | leerer Titel + Enter → kein POST |
| new-folder | Name + Enter → POST folders | leerer Name + Enter → kein POST |
| move | Re-Auth-TOTP + Enter → PATCH space=gamma | Enter im Space-`<select>` → kein PATCH |
| share | Re-Auth-TOTP + Enter → PATCH share_write | Enter im Space-`<select>` → kein PATCH |
| trash | exakter Titel + Enter → DELETE | falscher Titel (Knopf disabled) + Enter → kein DELETE |
| confirm (Archivieren) | Enter (kein Eingabefeld) → PATCH archived | „Abbrechen" am Zweititem → kein PATCH |
| settings-password | TOTP-Feld + Enter → POST account/password | Enter im Passwortfeld (nicht erlaubt) → kein POST |
| settings-spaces | Name + Enter → POST /spaces | leerer Name + Enter → kein POST |
| settings-space-detail | Re-Auth-TOTP + Enter → POST members | leerer Name + Enter → kein POST |
| space-remove | Name + Re-Auth-TOTP + Enter → DELETE /spaces | leerer Bestätigungsname + Enter → kein DELETE |
| legacy-host | **im Wegwerf nicht erreichbar** — `SPACE_UI_LEGACY_ORIGIN` verlangt laut Fail-closed-Parser (`mcpserver/config.py:48`) `https://`; ein http-Wegwerf hat nie eine passende Legacy-Origin, der Dialog kann nie erscheinen | — |

Re-Auth-Mechanik (P6 Step 7a): jede rechteerweiternde Aktion (move auf gamma, share_write,
Mitglied hinzufügen, Space entfernen, Passwort ändern) bekommt ihr eigenes `reauth_required`
und damit ihre eigenen TOTP-Felder — Enter ist in genau diesen Feldern erlaubt
(`enterTable`-Feldlisten). Der TOTP-Code wird pro Verify verbraucht (strikt steigender Zähler),
deshalb wartet jede Station ein frisches 30-s-Fenster ab.

Wegwerf-Instanz: `p10_wegwerf.py` (Port 8799, zwei Principals — hier loggt sich `alpha` ein;
der „andere Client" für den Konflikt ist ein direkter `store.update()` auf dem Wegwerf-`DATA_ROOT`,
dieselbe Kategorie wie die P9-trace-Browser-Probe). Ausgabe: JSON auf stdout (Hard Rule 7) +
`p10_m5_enter_conflict.json` neben diesem Skript.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import os
import struct
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_PY = REPO_ROOT / ".venv" / "bin" / "python"
CREDS_FILE = Path("/tmp/opencode/sharefyx-wegwerf-p10/credentials.json")
IDS_FILE = Path("/tmp/opencode/sharefyx-wegwerf-p10/ids.json")
DATA_ROOT = "/tmp/opencode/sharefyx-wegwerf-p10/data"
BASE_URL = "https://127.0.0.1:8799"  # TLS-Wegwerf, siehe p10_wegwerf.py (CSRF-Origin-Gleichheit)
OUT_JSON = REPO_ROOT / "phase10_inventory" / "probes" / "p10_m5_enter_conflict.json"

TEAM_SPACE = "gamma"


# --- Login + TOTP (Muster p86 / M4) -------------------------------------------


def _generate_totp(otpauth_uri: str) -> str:
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    msg = struct.pack(">q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code_int = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code_int:06d}"


def wait_fresh_window() -> None:
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"  warte {wait}s auf frisches TOTP-Fenster ...", file=sys.stderr)
    time.sleep(wait)


def totp_now(otpauth_uri: str) -> str:
    return _generate_totp(otpauth_uri)


def login(page: Page, space: str, password: str, otpauth_uri: str) -> None:
    wait_fresh_window()
    for window in range(2):
        page.goto(f"{BASE_URL}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill(space)
        page.locator('input[name="password"]').fill(password)
        code = totp_now(otpauth_uri)
        print(f"  Login Fenster {window + 1}: TOTP {code}", file=sys.stderr)
        page.locator('input[name="totp"]').fill(code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        if resp_info.value.status in (200, 303):
            time.sleep(2.0)
            return
        if resp_info.value.status == 401:
            time.sleep(35)
            continue
        raise RuntimeError(f"Login fehlgeschlagen: HTTP {resp_info.value.status}")
    raise RuntimeError("Login: TOTP-Fenster erschöpft")


class RequestLog:
    """Fängt Methode + URL + Body aller Requests ab Station X — die Stationen zählen
    Differenzen (mark/since), nicht absolute Listen."""

    def __init__(self, page: Page) -> None:
        self.entries: list[tuple[str, str, str]] = []
        page.on("request", self._on_request)

    def _on_request(self, req) -> None:
        self.entries.append((req.method, req.url, req.post_data or ""))

    def mark(self) -> int:
        return len(self.entries)

    def since(self, mark: int, method: str, url_suffix: str) -> list[tuple[str, str, str]]:
        return [
            e for e in self.entries[mark:]
            if e[0] == method and e[1].endswith(url_suffix)
        ]


def b_side_update_team_aufgaben(new_body: str) -> None:
    """Der „andere Client": direkte `store.update()`-Aufrufe auf dem Wegwerf-DATA_ROOT (eigenes
    tmp-Verzeichnis, kein Trick gegen Echtes). Erhöht gezielt ALLE Items mit dem Titel
    „Team Aufgabe" in gamma — nach der ersten Kopie trägt die Kopie denselben Titel, und der
    Konflikt muss auf dem Item entstehen, das A gerade offen hat, nicht auf seinem Zwillig."""
    code = (
        "from storage.store import Store\n"
        f"s = Store({DATA_ROOT!r}, git=False)\n"
        "for it in s.search(space='gamma', limit=200).items:\n"
        "    if it.title == 'Team Aufgabe':\n"
        "        s.update(it.id, version=it.version, body=" + repr(new_body) + ")\n"
    )
    env = {"PYTHONPATH": str(REPO_ROOT), "PATH": os.environ.get("PATH", "")}
    subprocess.run([str(PROJECT_PY), "-c", code], check=True, env=env,
                   cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL)


def settle(seconds: float = 1.5) -> None:
    time.sleep(seconds)


# --- UI-Helfer -----------------------------------------------------------------


def open_settings_panel(page: Page, data_panel: str) -> None:
    page.locator("#account-button").click()
    page.locator(f'[data-panel="{data_panel}"]').click()


def open_bucket(page: Page, space: str, bucket: str) -> None:
    """Navigation geht im Baum über die Eimer-Zeilen (`tree.js :: renderFolders`), nicht über
    die Space-Zeile — die klappt nur auf/zu (renderSpaceNode, :256). Erst expandieren (falls
    nötig), dann die Eimer-Zeile klicken."""
    row = page.locator(f'.tree__folder[data-space="{space}"][data-bucket="{bucket}"]')
    if row.count() == 0:
        page.locator(".tree__space", has_text=space).first.click()
        settle(0.5)
    page.locator(f'.tree__folder[data-space="{space}"][data-bucket="{bucket}"]').first.click()
    settle(1.2)


def open_item_in_list(page: Page, title: str) -> None:
    page.locator(".list__rows > li", has_text=title).first.click()
    settle(1.0)
    page.locator("#toggle-preview").click()  # Vorschau → Bearbeiten
    settle(0.3)


def press_enter(page: Page) -> None:
    page.keyboard.press("Enter")
    time.sleep(0.4)


def dialog_visible(page: Page, dialog_id: str) -> bool:
    return page.evaluate(f"!document.getElementById({dialog_id!r}).hidden")


def ensure_list_view(page: Page) -> None:
    """Editor schließen, falls er (evtl. mit Entwurf) offen steht. Der Baum navigiert bei
    ungespeicherten Änderungen sonst NICHT (`closeEditor().then(proceed => …)` bricht ab,
    tree.js:81) — dann bliebe `data-view="detail"` stehen und jeder Listenkopf wäre unsichtbar."""
    view = page.evaluate("document.querySelector('.shell')?.dataset.view || ''")
    if view != "detail":
        return
    page.locator("#close-button").click()
    settle(0.4)
    if dialog_visible(page, "confirm-dialog"):
        page.locator("#confirm-ok").click()  # Entwurf verwerfen
        settle(0.6)


# --- Stationen ------------------------------------------------------------------


def station_conflict_copy(page: Page, log: RequestLog) -> dict:
    """BG-2: Konflikt an gamma-Item, Kopie muss nach gamma; Gegenläufe (a) Ladeweg ohne
    POST, (b) Enter im Konflikt-Dialog ist bewusst wirkungslos."""
    out: dict = {}

    def _make_conflict(my_text: str, b_text: str) -> None:
        open_bucket(page, TEAM_SPACE, "open")
        open_item_in_list(page, "Team Aufgabe")  # .first in open_item_in_list
        page.locator("#editor-textarea").fill(my_text)
        b_side_update_team_aufgaben(b_text)  # anderer Client erhöht die Version unter A's Hand
        with page.expect_response(lambda r: "/api/v1/items/" in r.url and r.request.method == "PATCH"):
            page.locator("#save-button").click()
        page.wait_for_selector("#conflict-dialog:not([hidden])", timeout=8000)
        settle(0.3)

    # (a) Kopie: POST /items trägt space=gamma, Antwort ebenfalls.
    _make_conflict("Fassung von A (Kopieweg)\n", "Fassung von B, Runde 1\n")
    mark = log.mark()
    with page.expect_request(lambda r: r.method == "POST" and r.url.endswith("/api/v1/items")) as ri:
        page.locator("#conflict-save-as-new").click()
    req = ri.value
    settle(1.5)
    payload = json.loads(req.post_data)
    response = req.response()
    body = response.json() if response is not None else {}
    out["copy_request_space"] = payload.get("space")
    out["copy_response_space"] = body.get("space")
    out["copy_status"] = response.status if response is not None else None
    out["copy_no_stray_posts"] = len(log.since(mark, "POST", "/api/v1/items")) == 1
    page.wait_for_selector("#conflict-dialog[hidden]", state="attached", timeout=8000)

    # (b) Ladeweg: kein POST. (c) Enter im Konflikt-Dialog: bewusst wirkungslos.
    _make_conflict("Fassung von A (Ladeweg)\n", "Fassung von B, Runde 2\n")
    mark = log.mark()
    page.locator("#conflict-load-current").click()
    settle(1.5)
    out["load_current_posts"] = len(log.since(mark, "POST", "/api/v1/items"))
    out["dialog_closed_after_load"] = not dialog_visible(page, "conflict-dialog")

    # Dialog noch einmal offen machen, um (c) an echtem Dialog zu messen: Konflikt Runde 3.
    _make_conflict("Fassung von A (Enter-Sperrtest)\n", "Fassung von B, Runde 3\n")
    mark = log.mark()
    page.locator("#conflict-message").click()  # Fokus in den Dialog, auf kein Eingabefeld
    press_enter(page)
    settle(1.0)
    out["enter_in_conflict_posts"] = len(log.since(mark, "POST", "/api/v1/items"))
    out["enter_in_conflict_dialog_stays_open"] = dialog_visible(page, "conflict-dialog")
    page.locator("#conflict-cancel").click()
    settle(0.5)
    return out


def station_create(page: Page, log: RequestLog) -> dict:
    out: dict = {}
    ensure_list_view(page)
    open_bucket(page, "alpha", "note")  # deterministisches Ziel: der Dialog nimmt state.activeSpace
    page.locator("#new-item-button").click()
    settle(0.3)
    # Gegenlauf: leerer Titel + Enter — der Handler bricht früh ab, kein POST.
    mark = log.mark()
    page.locator("#create-title-input").click()
    press_enter(page)
    settle(0.8)
    out["counter_posts_with_empty_title"] = len(log.since(mark, "POST", "/api/v1/items"))
    # Positiv: Titel + Enter → POST /items.
    mark = log.mark()
    page.locator("#create-title-input").fill("M5 Enter-Notiz")
    press_enter(page)
    settle(1.5)
    posts = log.since(mark, "POST", "/api/v1/items")
    out["positive_posts"] = len(posts)
    out["positive_status_ok"] = bool(posts) and dialog_visible(page, "create-dialog") is False
    return out


def station_new_folder(page: Page, log: RequestLog) -> dict:
    out: dict = {}
    ensure_list_view(page)
    open_bucket(page, "alpha", "open")
    page.locator(".tree__new-folder").first.click()
    settle(0.3)
    mark = log.mark()
    page.locator("#new-folder-name-input").click()
    press_enter(page)
    settle(0.8)
    out["counter_posts_with_empty_name"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and "/folders" in e[1]]
    )
    mark = log.mark()
    page.locator("#new-folder-name-input").fill("M5 Ordner")
    press_enter(page)
    settle(1.5)
    out["positive_posts"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and "/folders" in e[1]]
    )
    out["dialog_closed"] = not dialog_visible(page, "new-folder-dialog")
    return out


def _reauth_fields_visible(page: Page, prefix: str) -> bool:
    return page.evaluate(f"!document.getElementById({prefix + '-reauth-fields'!r}).hidden")


def station_move(page: Page, log: RequestLog, password: str, otpauth_uri: str) -> dict:
    """Move alpha→gamma ist ein Widen (P6 Step 7a) → reauth_required → Enter im TOTP-Feld
    ist der erlaubte Weg. Gegenlauf: Enter im Space-<select> feuert nichts."""
    out: dict = {}
    ensure_list_view(page)
    open_bucket(page, "alpha", "note")
    row = page.locator(".list__rows > li", has_text="M5 Enter-Notiz").first
    row.hover()
    row.locator(".list__row-move").click()
    settle(0.4)
    page.locator("#move-space-select").select_option(TEAM_SPACE)
    settle(0.3)
    # Gegenlauf: Fokus im <select> — SELECT ist von Enter ausgenommen.
    mark = log.mark()
    page.locator("#move-space-select").focus()
    press_enter(page)
    settle(0.8)
    out["counter_patches_from_select"] = len(
        [e for e in log.entries[mark:] if e[0] == "PATCH" and "/api/v1/items/" in e[1]]
    )
    # Positiv: erst Submit-Klick (löst reauth_required), dann TOTP + Enter.
    page.locator("#move-submit").click()
    settle(0.8)
    out["reauth_appeared"] = _reauth_fields_visible(page, "move")
    wait_fresh_window()
    page.locator("#move-reauth-password").fill(password)
    mark = log.mark()
    page.locator("#move-reauth-totp").fill(totp_now(otpauth_uri))
    page.locator("#move-reauth-totp").focus()
    press_enter(page)
    settle(2.0)
    patches = [
        e for e in log.entries[mark:] if e[0] == "PATCH" and "/api/v1/items/" in e[1]
    ]
    out["positive_patches"] = len(patches)
    out["positive_patch_space"] = next(
        (json.loads(e[2]).get("space") for e in patches if e[2]), None
    )
    out["dialog_closed"] = not dialog_visible(page, "move-dialog")
    return out


def station_share(page: Page, log: RequestLog, password: str, otpauth_uri: str) -> dict:
    out: dict = {}
    ensure_list_view(page)
    open_bucket(page, "alpha", "open")
    # Bewusst ein Wurzel-Item: die Liste zeigt den gewählten Baumknoten, und „Konfliktkandidat"
    # liegt in der alpha-Wurzel (Seed) — ein Ordner-Item wäre in dieser Sicht gar nicht sichtbar.
    row = page.locator(".list__rows > li", has_text="Konfliktkandidat").first
    row.hover()
    row.locator(".list__row-share").click()
    settle(0.4)
    select = page.locator('#share-rows select[data-space="gamma"]')
    select.select_option("write")
    settle(0.3)
    mark = log.mark()
    select.focus()
    press_enter(page)
    settle(0.8)
    out["counter_patches_from_select"] = len(
        [e for e in log.entries[mark:] if e[0] == "PATCH" and "/api/v1/items/" in e[1]]
    )
    page.locator("#share-submit").click()
    settle(0.8)
    out["reauth_appeared"] = _reauth_fields_visible(page, "share")
    wait_fresh_window()
    page.locator("#share-reauth-password").fill(password)
    mark = log.mark()
    page.locator("#share-reauth-totp").fill(totp_now(otpauth_uri))
    page.locator("#share-reauth-totp").focus()
    press_enter(page)
    settle(2.0)
    patches = [
        e for e in log.entries[mark:] if e[0] == "PATCH" and "/api/v1/items/" in e[1]
    ]
    out["positive_patches"] = len(patches)
    out["positive_patch_share_write"] = next(
        (json.loads(e[2]).get("share_write") for e in patches if e[2]), None
    )
    out["dialog_closed"] = not dialog_visible(page, "share-dialog")
    return out


def station_trash(page: Page, log: RequestLog) -> dict:
    out: dict = {}
    ensure_list_view(page)
    open_bucket(page, "alpha", "open")
    row = page.locator(".list__rows > li", has_text="Konfliktkandidat").first
    title_in_dialog = "Konfliktkandidat"
    row.hover()
    row.locator(".list__row-trash").click()
    settle(0.4)
    # Zwei-Stufen-Fluss (dialogs.js:359): erst der generische Confirm („Weiter"), DANN der
    # Titel-Dialog.
    page.wait_for_selector("#confirm-dialog:not([hidden])", timeout=8000)
    page.locator("#confirm-ok").click()
    page.wait_for_selector("#trash-dialog:not([hidden])", timeout=8000)
    settle(0.3)
    # Gegenlauf: falscher Titel — Knopf bleibt disabled, Enter darf nichts firen.
    page.locator("#trash-confirm-input").fill("falscher Titel")
    settle(0.2)
    out["submit_disabled_on_wrong_title"] = page.locator("#trash-submit").is_disabled()
    mark = log.mark()
    page.locator("#trash-confirm-input").focus()
    press_enter(page)
    settle(0.8)
    out["counter_deletes"] = len(
        [e for e in log.entries[mark:] if e[0] == "DELETE" and "/api/v1/items/" in e[1]]
    )
    # Positiv: exakter Titel + Enter im Bestätigungsfeld.
    mark = log.mark()
    page.locator("#trash-confirm-input").fill(title_in_dialog)
    settle(0.2)
    page.locator("#trash-confirm-input").focus()
    press_enter(page)
    settle(2.0)
    out["positive_deletes"] = len(
        [e for e in log.entries[mark:] if e[0] == "DELETE" and "/api/v1/items/" in e[1]]
    )
    out["dialog_closed"] = not dialog_visible(page, "trash-dialog")
    return out


def station_confirm_archive(page: Page, log: RequestLog) -> dict:
    out: dict = {}
    # Opfer-Item für den Gegenlauf zuerst anlegen (Wurzel-Item im aktiven Space alpha).
    open_bucket(page, "alpha", "note")
    page.locator("#new-item-button").click()
    settle(0.3)
    page.locator("#create-title-input").fill("M5 Archiv-Kandidat")
    page.locator("#create-title-input").focus()
    press_enter(page)
    settle(1.5)
    # Positiv: Item öffnen, Archivieren, Enter (kein Eingabefeld im Dialog) → POST …/archive.
    ensure_list_view(page)
    open_bucket(page, "alpha", "open")
    open_item_in_list(page, "Alpha Aufgabe offen")
    page.locator("#archive-button").click()
    settle(0.4)
    page.locator("#confirm-title").click()  # Fokus in den Dialog, kein INPUT
    mark = log.mark()
    press_enter(page)
    settle(2.0)
    archives = [
        e for e in log.entries[mark:] if e[0] == "POST" and e[1].endswith("/archive")
    ]
    out["positive_archive_posts"] = len(archives)
    # Gegenlauf: Zweititem, diesmal „Abbrechen" statt Bestätigen — kein PATCH.
    open_bucket(page, "alpha", "note")
    open_item_in_list(page, "M5 Archiv-Kandidat")
    page.locator("#archive-button").click()
    settle(0.4)
    mark = log.mark()
    page.locator("#confirm-cancel").click()
    settle(1.0)
    out["counter_archive_posts_after_cancel"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and e[1].endswith("/archive")]
    )
    return out


def station_settings_spaces(page: Page, log: RequestLog) -> dict:
    out: dict = {}
    open_settings_panel(page, "spaces")
    settle(0.3)
    # Gegenlauf: leerer Name + Enter → kein POST.
    mark = log.mark()
    page.locator("#space-create-name-input").click()
    press_enter(page)
    settle(0.8)
    out["counter_posts_with_empty_name"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and e[1].endswith("/api/v1/spaces")]
    )
    # Positiv: Name + Enter → POST /spaces, Zeile erscheint (spaces.js:214 lädt nach).
    mark = log.mark()
    page.locator("#space-create-name-input").fill("delta")
    press_enter(page)
    settle(2.0)
    out["positive_posts"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and e[1].endswith("/api/v1/spaces")]
    )
    rows = page.locator("#space-admin-list .settings-space-row")
    out["delta_row_present"] = rows.count() > 0 and "delta" in rows.all_inner_texts().__str__()
    return out


def station_space_detail_member(page: Page, log: RequestLog, password: str, otpauth_uri: str) -> dict:
    out: dict = {}
    page.locator("#space-admin-list .settings-space-row", has_text="delta").click()
    settle(1.0)
    out["detail_open"] = page.evaluate(
        "!document.getElementById('settings-space-detail').hidden"
    )
    # Gegenlauf: leerer Name + Enter → kein POST.
    mark = log.mark()
    page.locator("#space-member-name-input").click()
    press_enter(page)
    settle(0.8)
    out["counter_posts_with_empty_name"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and "/members" in e[1]]
    )
    # Positiv: Mitglied + Enter (Submit feuert, kommt mit reauth_required zurück),
    # dann Passwort+TOTP und Enter im TOTP-Feld.
    page.locator("#space-member-write-select").select_option("write")
    page.locator("#space-member-name-input").fill("alpha")
    page.locator("#space-member-name-input").focus()
    mark = log.mark()
    press_enter(page)
    settle(1.0)
    out["first_submit_posts"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and "/members" in e[1]]
    )
    out["reauth_appeared"] = _reauth_fields_visible(page, "space-member")
    wait_fresh_window()
    page.locator("#space-member-reauth-password").fill(password)
    mark = log.mark()
    page.locator("#space-member-reauth-totp").fill(totp_now(otpauth_uri))
    page.locator("#space-member-reauth-totp").focus()
    press_enter(page)
    settle(2.0)
    out["positive_member_posts"] = len(
        [e for e in log.entries[mark:] if e[0] == "POST" and "/members" in e[1]]
    )
    members = page.locator("#space-member-list").inner_text()
    out["alpha_listed_as_member"] = "alpha" in members
    return out


def station_space_remove(page: Page, log: RequestLog, password: str, otpauth_uri: str) -> dict:
    """Zerstörungsinstrument bleibt im Wegwerf: gamma wird am Ende entfernt (seine Items
    archivieren nach alpha — das ist der getestete Weg selbst)."""
    out: dict = {}
    page.locator("#space-admin-list .settings-space-row", has_text=TEAM_SPACE).click()
    settle(1.0)
    page.locator("#space-remove-open").click()
    settle(0.4)
    # Gegenlauf: leerer Bestätigungsname + Enter — der Submit firet hier (anders als beim
    # Löschen-Dialog gibt es keinen clientseitigen Riegel), der Server lehnt ab
    # (`_spaces_delete`: 'confirm' muss exakt dem Space-Namen entsprechen) — gemessen wird,
    # dass der Space **überlebt**: die Zeile bleibt in der Liste.
    mark = log.mark()
    page.locator("#space-remove-confirm-input").click()
    press_enter(page)
    settle(1.0)
    out["counter_delete_attempts"] = len(
        [e for e in log.entries[mark:] if e[0] == "DELETE" and "/api/v1/spaces/" in e[1]]
    )
    out["gamma_survives_counter_enter"] = page.locator(
        "#space-admin-list .settings-space-row", has_text=TEAM_SPACE
    ).count() > 0
    # Positiv: Name + Enter (Submit → reauth_required), dann TOTP + Enter → DELETE.
    page.locator("#space-remove-confirm-input").fill(TEAM_SPACE)
    page.locator("#space-remove-confirm-input").focus()
    mark = log.mark()
    press_enter(page)
    settle(1.0)
    out["first_submit_deletes_or_reauth"] = len(
        [e for e in log.entries[mark:] if e[0] == "DELETE" and "/api/v1/spaces/" in e[1]]
    )
    out["reauth_appeared"] = _reauth_fields_visible(page, "space-remove")
    wait_fresh_window()
    page.locator("#space-remove-reauth-password").fill(password)
    mark = log.mark()
    page.locator("#space-remove-reauth-totp").fill(totp_now(otpauth_uri))
    page.locator("#space-remove-reauth-totp").focus()
    press_enter(page)
    settle(3.0)
    out["positive_deletes"] = len(
        [e for e in log.entries[mark:] if e[0] == "DELETE" and "/api/v1/spaces/" in e[1]]
    )
    return out


def station_settings_password(
    page: Page, log: RequestLog, current_password: str, otpauth_uri: str
) -> tuple[dict, str]:
    """Passwortwechsel: Positiv ändert alpha's Passwort — der Rückgabewert ist das neue
    Passwort, damit die Legacy-/Folgenutzung (und der Credentials-File-Update) damit leben."""
    out: dict = {}
    new_password = "wegwerf-p10-rot-" + datetime.datetime.now().strftime("%H%M%S")
    open_settings_panel(page, "password")
    settle(0.3)
    # Gegenlauf: Enter im neuen-Passwort-Feld (NICHT in der Erlaubtliste) → kein POST.
    mark = log.mark()
    page.locator("#account-new").click()
    press_enter(page)
    settle(0.8)
    out["counter_posts_from_wrong_field"] = len(
        [e for e in log.entries[mark:] if "/account/password" in e[1]]
    )
    # Positiv: alle Felder, Enter im TOTP-Feld (der einzige erlaubte Eingabeweg).
    page.locator("#account-current").fill(current_password)
    page.locator("#account-new").fill(new_password)
    page.locator("#account-repeat").fill(new_password)
    wait_fresh_window()
    page.locator("#account-totp").fill(totp_now(otpauth_uri))
    mark = log.mark()
    page.locator("#account-totp").focus()
    press_enter(page)
    settle(2.0)
    posts = [e for e in log.entries[mark:] if "/account/password" in e[1]]
    out["positive_posts"] = len(posts)
    out["toast_or_error_visible"] = page.evaluate(
        "!document.getElementById('account-error').hidden"
    )
    return out, new_password


# --- Hauptlauf -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.parse_args(argv)

    creds = json.loads(CREDS_FILE.read_text())["users"][0]
    assert creds["space"] == "alpha"

    stations: dict[str, dict] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
        )
        page = context.new_page()
        login(page, creds["space"], creds["password"], creds["otpauth_uri"])
        with page.expect_response("**/api/v1/overview"):
            page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
        settle(1.0)
        log = RequestLog(page)

        print("Station BG-2 (Konfliktkopie) ...", file=sys.stderr)
        stations["bg2_conflict_copy"] = station_conflict_copy(page, log)
        print("Station create ...", file=sys.stderr)
        stations["create"] = station_create(page, log)
        print("Station new-folder ...", file=sys.stderr)
        stations["new_folder"] = station_new_folder(page, log)
        print("Station move (TOTP) ...", file=sys.stderr)
        stations["move"] = station_move(page, log, creds["password"], creds["otpauth_uri"])
        print("Station share (TOTP) ...", file=sys.stderr)
        stations["share"] = station_share(page, log, creds["password"], creds["otpauth_uri"])
        print("Station trash ...", file=sys.stderr)
        stations["trash"] = station_trash(page, log)
        print("Station confirm/archive ...", file=sys.stderr)
        stations["confirm_archive"] = station_confirm_archive(page, log)
        print("Station settings-spaces ...", file=sys.stderr)
        stations["settings_spaces"] = station_settings_spaces(page, log)
        print("Station space-detail member (TOTP) ...", file=sys.stderr)
        stations["space_detail_member"] = station_space_detail_member(
            page, log, creds["password"], creds["otpauth_uri"]
        )
        print("Station space-remove gamma (TOTP) ...", file=sys.stderr)
        stations["space_remove"] = station_space_remove(
            page, log, creds["password"], creds["otpauth_uri"]
        )
        print("Station settings-password (TOTP) ...", file=sys.stderr)
        stations["settings_password"], new_password = station_settings_password(
            page, log, creds["password"], creds["otpauth_uri"]
        )

        browser.close()

    # Passwort-Rotation im Wegwerf nachziehen (File liegt außerhalb des Repos).
    creds["password"] = new_password
    CREDS_FILE.write_text(json.dumps({"users": [creds]}, indent=2))

    stations["legacy_host"] = {
        "reachable_in_wegwerf": False,
        "reason": (
            "SPACE_UI_LEGACY_ORIGIN verlangt laut Fail-closed-Parser "
            "(mcpserver/config.py:48) https://-Form; ein http-Wegwerf hat nie eine "
            "passende Legacy-Origin — der Dialog kann nie erscheinen."
        ),
    }

    checks = {
        "bg2_copy_space_is_item_space": (
            stations["bg2_conflict_copy"]["copy_request_space"] == TEAM_SPACE
            and stations["bg2_conflict_copy"]["copy_response_space"] == TEAM_SPACE
        ),
        "bg2_copy_single_post": stations["bg2_conflict_copy"]["copy_no_stray_posts"],
        "bg2_load_current_no_post": stations["bg2_conflict_copy"]["load_current_posts"] == 0,
        "bg2_enter_in_conflict_inert": (
            stations["bg2_conflict_copy"]["enter_in_conflict_posts"] == 0
            and stations["bg2_conflict_copy"]["enter_in_conflict_dialog_stays_open"]
        ),
        "enter_create": (
            stations["create"]["counter_posts_with_empty_title"] == 0
            and stations["create"]["positive_posts"] == 1
        ),
        "enter_new_folder": (
            stations["new_folder"]["counter_posts_with_empty_name"] == 0
            and stations["new_folder"]["positive_posts"] == 1
        ),
        "enter_move": (
            stations["move"]["counter_patches_from_select"] == 0
            and stations["move"]["reauth_appeared"]
            and stations["move"]["positive_patches"] >= 1
            and stations["move"]["positive_patch_space"] == TEAM_SPACE
        ),
        "enter_share": (
            stations["share"]["counter_patches_from_select"] == 0
            and stations["share"]["reauth_appeared"]
            and stations["share"]["positive_patches"] >= 1
        ),
        "enter_trash": (
            stations["trash"]["submit_disabled_on_wrong_title"]
            and stations["trash"]["counter_deletes"] == 0
            and stations["trash"]["positive_deletes"] == 1
        ),
        "enter_confirm": (
            stations["confirm_archive"]["positive_archive_posts"] == 1
            and stations["confirm_archive"]["counter_archive_posts_after_cancel"] == 0
        ),
        "enter_settings_spaces": (
            stations["settings_spaces"]["counter_posts_with_empty_name"] == 0
            and stations["settings_spaces"]["positive_posts"] == 1
            and stations["settings_spaces"]["delta_row_present"]
        ),
        "enter_space_detail": (
            stations["space_detail_member"]["counter_posts_with_empty_name"] == 0
            and stations["space_detail_member"]["reauth_appeared"]
            and stations["space_detail_member"]["positive_member_posts"] >= 1
            and stations["space_detail_member"]["alpha_listed_as_member"]
        ),
        "enter_space_remove": (
            stations["space_remove"]["gamma_survives_counter_enter"]
            and stations["space_remove"]["reauth_appeared"]
            and stations["space_remove"]["positive_deletes"] == 1
        ),
        "enter_settings_password": (
            stations["settings_password"]["counter_posts_from_wrong_field"] == 0
            and stations["settings_password"]["positive_posts"] == 1
        ),
    }
    result = {
        "probe": "p10_m5_enter_conflict",
        "stations": stations,
        "checks": checks,
        "all_passed": all(checks.values()),
    }
    print(json.dumps(result, ensure_ascii=False, indent=1))
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
