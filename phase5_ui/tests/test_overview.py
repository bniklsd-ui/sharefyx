"""`GET /api/v1/overview` (Step 7b, autonom geschlossene Plan-Lücke — siehe `webui/api.py`s
Moduldocstring). Speist die Übersichtsseite und die Zähler-Plaketten im Navigationsbaum.

Die Zähler sind hier bewusst prüfbar: der Plan lässt JavaScript ungetestet, deshalb liegt die
Zählung serverseitig und nicht in `app.js`. Die zentrale Aussage der Datei ist, dass ein Zähler
exakt so viele Items meint, wie die Liste beim Klick auf denselben Ordner zeigt — jede andere
Zahl wäre schlimmer als gar keine.

**[P10.5, Block 4, 2026-10-22]** Die Zählung ist auf **einen** `store.search()`-Durchgang
umgestellt (Lock P10.5-G) — vorher kostete sie je sichtbarem Space fünf Bucket-Zählungen
plus eine Liste, bei 4 Spaces/197 Items 2,4 s (P10 §1.3). Die Zusage bleibt dieselbe: die
Zähler sind **paritätisch** zu dem, was `store.search(**filters).total` je Eimer liefert.
Diese Datei trägt den Beweis dafür; der Tempogewinn ist die Aufgabe des M2-Benchs
(Abnahme P10.5-14).
"""
from __future__ import annotations

import asyncio
import re
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from mcpserver.permissions import SharePolicy
from starlette.applications import Starlette
from storage.store import Store

from webui.account import account_routes
from webui.api import _BUCKETS, api_routes
from webui.routes_auth import ui_auth_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
FOREIGN_SPACE = "fabian"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> None:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200


@pytest.fixture
def ticking_store(tmp_path) -> Store:
    """Eigener `Store` mit einer schrittweise laufenden Uhr — `item_store` aus `conftest.py`
    benutzt die Systemuhr, und die löst innerhalb eines Tests nicht fein genug auf, um eine
    Sortierung nach `updated` überhaupt beobachtbar zu machen."""
    state = {"now": datetime(2026, 8, 5, 9, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        state["now"] += timedelta(minutes=1)
        return state["now"]

    data_root = tmp_path / "data"
    data_root.mkdir()
    return Store(data_root, git=False, now_fn=now_fn)


@pytest.fixture
def overview_app(ui_settings, store, confirmed_users, sessions, ticking_store) -> Starlette:
    routes = (
        ui_auth_routes(ui_settings, store, confirmed_users, sessions)
        + account_routes(ui_settings, store, confirmed_users, sessions)
        + api_routes(
            ui_settings,
            ticking_store,
            sessions,
            # P10.5, Block 2 (2026-10-22): Home-Space-Prädikat, dieselbe Quelle wie live
            # (`mcpserver/app.py :: create_app()`) — `store` ist hier der `AuthStore`.
            SharePolicy(
                ticking_store.acl_reader,
                is_home_space=lambda space: store.get_user(space) is not None,
            ),
            store,
            confirmed_users,
        )
    )
    return Starlette(routes=routes)


@pytest.fixture
def seeded(ticking_store, tmp_path) -> Store:
    """Ein Item je Ordner plus ein zweites im Archiv, dazu ein fremder Space. P6 Step 5: ohne
    `.share.yml` wäre `FOREIGN_SPACE` seit P6-U für `SPACE` unsichtbar — die `.share.yml`
    macht ihn lesbar, damit `test_foreign_space_is_visible_but_marked_not_own` überhaupt
    etwas zu prüfen hat; die drei anderen Tests, die `seeded` benutzen, sehen nur `SPACE` und
    bleiben davon unberührt.

    **[P9 Block doing, 2026-10-02, T8]** Der „In Arbeit"-Task steht hier **und** ist die
    **erste** Anweisung. Zwei Gründe, beide nicht Geschmack:
    - Ohne ihn liefe `test_counts_match_the_item_list_for_the_same_bucket` für `doing`
      **vakuös** (0 == 0) — der älteste Konsistenztest der Datei hätte den neuen Eimer
      ungeprüft passieren lassen.
    - `ticking_store` rückt pro Schreibvorgang eine Minute vor, und `_RECENT_LIMIT = 5`.
      Als ältestes Item verdrängt es keins der bisherigen aus `recent`, der Datenstand der
      übrigen `seeded`-Tests bleibt damit unverändert. `assignee=SPACE` ist gesetzt, damit
      T5 (P9-W: das UI-Speichern verliert die Zuweisung nicht) denselben Datenstand benutzt.
    """
    ticking_store.create(SPACE, type="task", title="laufende Aufgabe", status="doing",
                         assignee=SPACE)
    ticking_store.create(SPACE, type="task", title="offene Aufgabe")
    ticking_store.create(SPACE, type="task", title="erledigte Aufgabe", status="done")
    ticking_store.create(SPACE, type="note", title="aktive Notiz")
    archived = ticking_store.create(SPACE, type="note", title="alte Notiz")
    ticking_store.archive(archived.id, version=archived.version)
    archived_task = ticking_store.create(SPACE, type="task", title="alte Aufgabe")
    ticking_store.archive(archived_task.id, version=archived_task.version)
    ticking_store.create(FOREIGN_SPACE, type="note", title="Fabians Notiz", body="fremder Text")
    (tmp_path / "data" / FOREIGN_SPACE / ".share.yml").write_text(
        f"read: [{SPACE}]\n", encoding="utf-8"
    )
    return ticking_store


def _space(payload, name):
    return next(entry for entry in payload if entry["name"] == name)


@pytest.mark.asyncio
async def test_counts_match_the_item_list_for_the_same_bucket(overview_app, seeded, totp_code):
    """Der eigentliche Zweck der Datei: Zähler und Liste dürfen nie auseinanderlaufen. Geprüft
    wird nicht gegen erwartete Zahlen, sondern gegen `/api/v1/items` mit genau den Filtern, die
    `_BUCKETS` für denselben Ordner definiert."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        overview = (await client.get("/api/v1/overview")).json()
        own = _space(overview, SPACE)
        for bucket, filters in _BUCKETS.items():
            listing = await client.get(
                "/api/v1/items", params={**filters, "space": SPACE, "limit": 200},
            )
            assert listing.status_code == 200
            assert own["counts"][bucket] == listing.json()["total"], bucket


@pytest.mark.asyncio
async def test_archived_task_lands_in_archive_and_done_task_is_not_lost(overview_app, seeded, totp_code):
    """Der Fund, der den vierten Ordner nötig machte: eine auf `done` gesetzte Aufgabe war in
    keinem der drei Mockup-Ordner mehr auffindbar. Zusätzlich: eine ARCHIVIERTE Aufgabe zählt
    zum Archiv, nicht zu „Offen" (deshalb ist `archived` typunabhängig).

    **[P9 Block doing, 2026-10-02, T8]** `counts["doing"] == 1` kam hinzu, und die Zeile
    `counts["open"] == 1` bleibt deshalb stehen: sie belegt, dass `doing` **nicht** in „Offen"
    mitzählt. Zusammen sind das die zwei Richtungen von P9-61 — die Aufgabe landet in ihrem
    eigenen Eimer **und** in keinem anderen."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        counts = _space((await client.get("/api/v1/overview")).json(), SPACE)["counts"]

    assert counts["open"] == 1
    assert counts["doing"] == 1
    assert counts["done"] == 1
    assert counts["note"] == 1
    assert counts["archived"] == 2


@pytest.mark.asyncio
async def test_doing_task_counts_in_doing_and_nowhere_else(overview_app, seeded, totp_code):
    """T3 / P9-59: eine `doing`-Aufgabe zählt in „In Arbeit" und in **keinem** anderen Eimer.

    Drei Prüfungen, weil die Zahl allein zu wenig beweist — und jede davon wurde an einem
    **eingebauten Verstoß** rot, nicht aus angenommenem Nutzen (Gegenlauf §5):
    1. **Dict-Gleichheit** über alle fünf Zähler. „`doing` zählt 1" wäre auch grün, wenn dieselbe
       Aufgabe zusätzlich in „Offen" mitzählte — genau das hätte die Mengen-Variante
       „Offen = {open, doing}" eingeführt (Mini-Plan §2.1). Wer die Gleichheit liest, bekommt die
       Verteilung mitgeliefert.
    2. **Summe == `item_count`** (`store.py :: list_spaces()` zählt jede Indexzeile des Space):
       kein Item fällt durch, keins zählt doppelt.
    3. **Mengen-Disjunktheit** der Eimer-Mitgliedschaften. Die ersten beiden Prüfungen allein
       haben einen Fehler **nicht** gesehen: mit `_BUCKETS["doing"] = {"status": "open"}`
       (Verstoß G3, ein Duplikat) bleiben alle fünf Zahlen exakt gleich, weil der Seed je eine
       offene und eine laufende Aufgabe hat — der Zähler bleibt einfach „die Zahl der Aufgaben
       mit Status X". Nur die **Mitgliedschaft** unterscheidet sich, und die wird hier
       tatsächlich geholt: fünf Listenabfragen, ihre Item-Mengen müssen sich ausschließen und
       zusammen alle sechs Items des Space abdecken.
    """
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        own = _space((await client.get("/api/v1/overview")).json(), SPACE)
        mitglieder: dict[str, set] = {}
        for bucket, filters in _BUCKETS.items():
            listing = await client.get(
                "/api/v1/items", params={**filters, "space": SPACE, "limit": 200},
            )
            assert listing.status_code == 200
            mitglieder[bucket] = {row["id"] for row in listing.json()["items"]}

    assert own["counts"] == {"open": 1, "doing": 1, "done": 1, "note": 1, "archived": 2}
    assert sum(own["counts"].values()) == own["item_count"] == 6

    namen = list(mitglieder)
    for i, a in enumerate(namen):
        assert len(mitglieder[a]) == own["counts"][a], (
            f"{a}: Zähler {own['counts'][a]} != {len(mitglieder[a])} Listen-Einträge"
        )
        for b in namen[i + 1:]:
            assert not mitglieder[a] & mitglieder[b], f"{a} und {b} enthalten dasselbe Item"
    vereinigt = set().union(*mitglieder.values())
    assert len(vereinigt) == own["item_count"] == 6, (
        f"nur {len(vereinigt)} von 6 Items liegen in einem Eimer — der Rest ist unauffindbar"
    )


@pytest.mark.asyncio
async def test_doing_counter_equals_doing_list(overview_app, seeded, totp_code):
    """T4 / P9-60: Zähler == Liste für „In Arbeit" — und zwar am **konkreten Item**, nicht nur an
    der Zahl. Zwei gleitende Zahlen (0 == 0, 1 == 1 falscher Zuordnung) sind die eine Fehlerklasse;
    diese Assertion deckt die andere ab: der Zähler könnte sich auf ein anderes Item beziehen als
    der, das der Ordner anzeigt."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        counts = _space((await client.get("/api/v1/overview")).json(), SPACE)["counts"]
        listing = await client.get(
            "/api/v1/items", params={"type": "task", "status": "doing", "space": SPACE},
        )
        assert listing.status_code == 200
        body = listing.json()

    assert body["total"] == counts["doing"] == 1
    assert [row["title"] for row in body["items"]] == ["laufende Aufgabe"]
    assert body["items"][0]["status"] == "doing"


@pytest.mark.asyncio
async def test_ui_shaped_patch_keeps_doing_and_assignee(overview_app, ticking_store, totp_code):
    """T5 / P9-65: der Schreibpfad der Oberfläche darf die Maschinenebene nicht zerstören.

    Der Body ist **exakt** der Feldsatz, den `editor.js :: currentFormValues()` über
    `saveItem()` schickt: `version, format, title, body, status, due, tags, links` — und
    **kein** `assignee`, weil der Editor kein Feld dafür hat. `Store.update()` ändert nur
    übergebene Felder, also müsste `assignee` unangetastet bleiben. Genau das ist die
    Eigenschaft, an der P9-W hängt: die Rail darf „In Arbeit" heißen, während REST und MCP
    weiter `status: "doing"` und `assignee` ausliefern — ein angeschlossenes LLM liest daraus,
    wem die Aufgabe zugeteilt ist. Verlöre der Editor-Pfad das `assignee`, wäre die Übersetzung
    kein Sprachproblem, sondern ein Datenverlust.

    Geprüft über **beide** Lesepfade, weil nur der Server die Wahrheit kennt: die API-Antwort
    und `store.search(status="doing")` direkt aus dem Store."""
    created = ticking_store.create(SPACE, type="task", title="laufende Aufgabe",
                                   status="doing", assignee=SPACE)
    async with _client(overview_app) as client:
        csrf = _CSRF_RE.search((await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )).text).group(1)
        response = await client.patch(
            f"/api/v1/items/{created.id}",
            json={
                "version": created.version, "format": "markdown", "title": "umbenannt",
                "body": created.body, "status": "doing", "due": None, "tags": [], "links": [],
            },
            headers={"Origin": BASE_URL, "X-CSRF-Token": csrf},
        )
        assert response.status_code == 200
        payload = response.json()
        read_back = (await client.get(f"/api/v1/items/{created.id}")).json()

    assert payload["status"] == "doing" and payload["assignee"] == SPACE
    assert read_back["status"] == "doing" and read_back["assignee"] == SPACE
    # Und der Store, unabhängig von jeder Serialisierung.
    in_store = ticking_store.search(space=SPACE, status="doing").items
    assert [(i.status, i.assignee) for i in in_store] == [("doing", SPACE)]


@pytest.mark.asyncio
async def test_recent_is_newest_first_and_carries_no_snippet(overview_app, seeded, totp_code):
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        own = _space((await client.get("/api/v1/overview")).json(), SPACE)

    updated = [row["updated"] for row in own["recent"]]
    assert updated == sorted(updated, reverse=True)
    assert len(own["recent"]) <= 5
    # Rule 4 dem Geiste nach: die Übersicht zeigt keinen Fließtext, auch nicht aus dem eigenen
    # Space — sonst wäre die Fläche für fremde Spaces eine Sonderregel statt einer Eigenschaft.
    assert all("snippet" not in row for row in own["recent"])


@pytest.mark.asyncio
async def test_foreign_space_is_visible_but_marked_not_own(overview_app, seeded, totp_code):
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    foreign = _space(payload, FOREIGN_SPACE)
    assert foreign["own"] is False
    assert foreign["writable"] is False  # only "read:" granted, not "write:"
    assert _space(payload, SPACE)["own"] is True
    assert _space(payload, SPACE)["writable"] is True
    assert all(row["readonly"] is True for row in foreign["recent"])


@pytest.mark.asyncio
async def test_own_space_appears_even_without_a_single_item(overview_app, totp_code):
    """Derselbe B1-Sonderfall wie in `/api/v1/spaces` (P2-Adapter-Abnahme): ein Space ohne Items
    taucht in `Store.list_spaces()` gar nicht auf — die Übersicht wäre sonst beim allerersten
    Login leer, ohne Zähler und ohne Anlegen-Einstieg."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    own = _space(payload, SPACE)
    assert own["own"] is True
    assert own["recent"] == []
    assert set(own["counts"]) == set(_BUCKETS)
    assert all(count == 0 for count in own["counts"].values())


@pytest.mark.asyncio
async def test_overview_requires_a_session(overview_app):
    async with _client(overview_app) as client:
        response = await client.get("/api/v1/overview")
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"


@pytest.mark.asyncio
async def test_overview_ignores_a_bearer_token(overview_app):
    """P5-F: `/api` akzeptiert niemals Bearer-Token, nur die Cookie-Sitzung (Akzeptanzkriterium
    19) — für den neuen Endpunkt genauso festgehalten wie für die aus Step 5."""
    async with _client(overview_app) as client:
        response = await client.get(
            "/api/v1/overview", headers={"Authorization": "Bearer irgendein-token"},
        )
    assert response.status_code == 401


# -- P10.5, Block 4 (2026-10-22): der Ein-Durchgang-Weg -------------------------------------
#
# Vier Tests für Lock P10.5-G. Die Zusage des Locks ist **Parität**, kein Fix: die neuen
# Zähler müssen genau das liefern, was `store.search(**filters).total` je Eimer liefert —
# der alte Weg war genau das, und der Zähler soll weiterhin mit der Liste übereinstimmen
# (das ist die Zusage der ganzen Datei seit Step 7b).


@pytest.mark.asyncio
async def test_one_pass_counts_equal_per_bucket_search_totals(
    overview_app, seeded, tmp_path, totp_code
):
    """P10.5-15: die Zähler des Ein-Durchgang-Wegs sind **identisch** mit den Zählern des
    alten Wegs (`store.search(**filters).total` je Eimer und Space).

    Geprüft wird gegen den **Store**, nicht gegen fest verdrahtete Zahlen: der Store ist die
    Quelle, und die Gleichheit ist die eigentliche Zusage. Eine Zahl, die nur „plausibel"
    aussieht, würde hier durchgehen und genau die Eigenschaft zerstören, die die Datei seit
    Step 7b hält (Zähler == Liste).

    Der Bestand deckt alle fünf Eimer ab (offen, in Arbeit, erledigt, Notiz, Archiv), zwei
    Spaces (der eigene und ein geteilter) und einen Space **ohne** Item — der Sonderfall B1,
    der sonst in `list_spaces()` gar nicht auftaucht und in der Übersicht mit lauter Nullen
    erscheinen muss."""
    # Ein Space ohne Item: `store.list_spaces()` zählt Verzeichnisse mit, nicht nur Indexzeilen
    # (B1) — ohne `.share.yml` wäre er für den Principal unsichtbar.
    (tmp_path / "data" / "leerer-space").mkdir()
    (tmp_path / "data" / "leerer-space" / ".share.yml").write_text(
        f"read: [{SPACE}]\n", encoding="utf-8"
    )

    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    assert len(payload) == 3, "drei sichtbare Spaces: eigener, geteilter, leerer"
    for entry in payload:
        for bucket, filters in _BUCKETS.items():
            expected = seeded.search(
                space=entry["name"], limit=1, offset=0, **filters,
            ).total
            assert entry["counts"][bucket] == expected, (entry["name"], bucket)

    leer = _space(payload, "leerer-space")
    assert all(count == 0 for count in leer["counts"].values())
    assert leer["recent"] == []


@pytest.mark.asyncio
async def test_overview_falls_back_beyond_fetch_limit(overview_app, seeded, monkeypatch, totp_code):
    """P10.5-G, Rückfall: ist der Store größer als die Fetch-Grenze, ist die **eine** Liste
    unvollständig — ein Zähler aus einer unvollständigen Liste wäre eine Lüge. `_overview()`
    fällt dann auf den alten Weg zurück (je Bucket ein eigener `store.search()`-Aufruf), und
    die Zähler bleiben dieselben.

    Die Grenze wird **klein gemacht** (hier 2 Items statt 5000), damit der Fall ohne
    5001-Testitems eintritt. Geprüft wird nicht, dass der Rückfall *benutzt* wird — dafür
    wäre ein Blick in die Implementierung nötig —, sondern dass die **Zahlen** stimmen, obwohl
    der Weg ein anderer ist. Genau das ist die Zusage, die ein Benutzer merkt."""
    import webui.api as api_module

    monkeypatch.setattr(api_module, "_STORE_FETCH_LIMIT", 2)
    assert seeded.search(space=SPACE, limit=1, offset=0).total > 2, (
        "der Bestand muss größer sein als die künstlich verkleinerte Grenze"
    )

    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    for entry in payload:
        for bucket, filters in _BUCKETS.items():
            expected = seeded.search(
                space=entry["name"], limit=1, offset=0, **filters,
            ).total
            assert entry["counts"][bucket] == expected, (entry["name"], bucket)


@pytest.mark.asyncio
async def test_overview_entries_carry_folders_and_members(overview_app, seeded, totp_code):
    """PF-4 (Schritt 4.3): der Client holt nur noch `/overview` — deshalb müssen `folders` und
    `members` **in** dieser Antwort stehen. Vorher kamen sie aus `/spaces` und wurden im
    Client zusammengeführt (ein zweiter Vollabruf).

    Der Vergleich läuft gegen `/api/v1/spaces`: das ist die Quelle, aus der auch der
    Zusammenbau im alten Client stammte. Ein Space ohne Ordner und ohne Mitglieder trägt
    zwei leere Listen — keine fehlenden Felder."""
    async with _client(overview_app) as client:
        await _login(client, totp_code)
        overview = (await client.get("/api/v1/overview")).json()
        spaces = (await client.get("/api/v1/spaces")).json()

    by_name = {entry["name"]: entry for entry in spaces}
    assert by_name, "die Spaces-Liste ist nicht leer — sonst prüft der Test nichts"
    for entry in overview:
        assert "folders" in entry and "members" in entry, entry["name"]
        assert isinstance(entry["folders"], list)
        assert isinstance(entry["members"], list)
        assert entry["folders"] == by_name[entry["name"]]["folders"], entry["name"]
        assert entry["members"] == by_name[entry["name"]]["members"], entry["name"]


@pytest.mark.asyncio
async def test_overview_runs_search_off_the_event_loop(overview_app, seeded, monkeypatch, totp_code):
    """Z2 (P10.5-16): der Store liest Dateien — der Zugriff darf den Event-Loop nicht
    blockieren, sonst wartet `/health` hinter `/overview` (M1: 4,8 s).

    Geprüft wird **beides**: dass der Zugriff über `asyncio.to_thread` läuft (sonst blockiert
    er) und dass es **genau ein** Store-Aufruf ist (sonst ist der Ein-Durchgang-Weg nicht
    gebaut, sondern nur schneller geworden — das wäre die halbe Wahrheit).

    `asyncio.to_thread` wird gezählt, nicht `store.search` selbst: der Test soll die
    Verdrahtung beweisen (die Suchfunktion *im* Thread), nicht eine bestimmte
    Implementierung des Ladens."""
    calls: list[str] = []
    real_to_thread = asyncio.to_thread

    async def counting_to_thread(func, /, *args, **kwargs):
        calls.append(getattr(func, "__name__", repr(func)))
        return await real_to_thread(func, *args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", counting_to_thread)

    async with _client(overview_app) as client:
        await _login(client, totp_code)
        payload = (await client.get("/api/v1/overview")).json()

    assert calls == ["search"], (
        f"erwartet: genau ein Store-Aufruf im Thread — gesehen: {calls}"
    )
    assert payload, "die Übersicht ist leer — der Test hat nichts geprüft"
