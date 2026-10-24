"""`GET /api/v1/events` — der Realtime-Änderungsfeed (P10.5, Block 10, Schritt 10.2 — LG-2,
Lock P10.5-L).

**Drei Ebenen, drei Testarten:**

1. `read_git_head()` / `changed_spaces()` — die Quelle. Getestet an echten Git-Strukturen
   (eine Ref-Datei, gepackte Refs, detached HEAD) und an einem **echten** tmp-Repo.
2. `ChangeFeed` — der Feed. Getestet an der echten `Store` (mit `git=True`), also an einem
   echten Write, der einen echten Commit erzeugt.
3. Die Route — der Stream. Getestet **als ASGI**, nicht über `httpx.ASGITransport`: der
   sammelt den ganzen Body, bevor er antwortet, und ein SSE-Stream ist endlos — die Antwort
   käme nie zurück.

**Was hier nicht getestet wird:** das Verhalten im Browser (der Client holt die Daten über
`/api/v1/items` und `/api/v1/overview`). Dafür ist die Probe
`phase10_5_finishing/probes/p105_b10_realtime_probe.py` da."""
from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

import pytest
from starlette.applications import Starlette
from storage.store import Store

from webui.account import account_routes
from webui.api import api_routes
from webui.config import COOKIE_NAME, UiSettings
from webui.events import ChangeFeed
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager

SPACE = "niklas"
FOREIGN_SPACE = "fabian"
IDLE_TTL_S = 12 * 3600
ABSOLUTE_TTL_S = 7 * 24 * 3600


# -- Hilfen ---------------------------------------------------------------------------------


async def _call(app, path: str = "/api/v1/events", cookie: str | None = None):
    """Ruft die App **als ASGI** auf und liefert `(task, state)`.

    **Warum nicht `httpx.ASGITransport`:** der sammelt den **ganzen** Body, bevor er die
    Antwort zurückgibt (`body_parts` in `httpx/_transports/asgi.py`). Ein SSE-Stream ist
    endlos — die Antwort käme nie zurück, der Test hinge. Der Stream wird deshalb
    **während** des Laufs gelesen; `receive()` kehrt nie zurück (der Test bricht ab).

    `state` trägt `status`, `headers`, `chunks` (die empfangenen Teile) und `complete`
    (die Antwort ist fertig — der Stream wurde beendet)."""
    headers = [(b"cookie", cookie.encode("utf-8"))] if cookie else []
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "headers": headers,
        "scheme": "https",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "query_string": b"",
        "server": ("testserver", 443),
        "client": ("testclient", 50000),
        "root_path": "",
    }
    state: dict = {"status": None, "headers": [], "chunks": [], "complete": False}

    async def receive():
        await asyncio.sleep(3600)
        return {"type": "http.disconnect"}

    async def send(message):
        if message["type"] == "http.response.start":
            state["status"] = message["status"]
            state["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            body = message.get("body", b"")
            if body:
                state["chunks"].append(body)
            if not message.get("more_body", False):
                state["complete"] = True

    task = asyncio.create_task(app(scope, receive, send))
    return task, state


def _text(state) -> str:
    return b"".join(state["chunks"]).decode("utf-8", errors="replace")


def _session_cookie(auth_store, space: str = SPACE) -> str:
    """Eine Sitzung ohne den ganzen Login-Durchlauf.

    `SessionManager.issue()` ruft `AuthStore.create_session()` auf und liefert die
    Session-ID zurück — das ist genau der Wert, der im Cookie steht. Der Test braucht keine
    Anmeldung, sondern eine gültige Sitzung."""
    session_id, _csrf = auth_store.create_session(
        space=space, idle_ttl_s=IDLE_TTL_S, absolute_ttl_s=ABSOLUTE_TTL_S,
    )
    return f"{COOKIE_NAME}={session_id}"


def _fake_head(counter: list[int]):
    """Ein `head_reader`, der bei jedem Aufruf einen **neuen** Hash liefert.

    Damit sieht der Feed Bewegung, ohne dass ein Git-Repo nötig ist — die Git-Seite wird
    an echten Repos getestet (`test_read_git_head_*`, `test_store_write_reaches_subscriber…`)."""

    def _reader(_data_root):
        counter[0] += 1
        # 40 Hex-Zeichen wie ein echter Commit-Hash — die Route kürzt auf zwölf.
        return f"{counter[0]:040x}"

    return _reader


@pytest.fixture
def events_app(ui_settings, store, confirmed_users, sessions, item_store, permissions):
    """Die Items-API **plus** der Ereignis-Stream, mit einem Feed auf 20 ms Takt."""

    def _build(feed: ChangeFeed) -> Starlette:
        routes = (
            ui_auth_routes(ui_settings, store, confirmed_users, sessions)
            + account_routes(ui_settings, store, confirmed_users, sessions)
            + api_routes(
                ui_settings, item_store, sessions, permissions, store, confirmed_users,
                events=feed,
            )
        )
        return Starlette(routes=routes)

    return _build


# -- 1. Die Quelle: read_git_head() ----------------------------------------------------------


def test_read_git_head_ref_file(tmp_path):
    """Der Normalfall: `HEAD` zeigt auf einen Branch, der als **Datei** vorliegt."""
    git_dir = tmp_path / ".git"
    (git_dir / "refs" / "heads").mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/master\n", encoding="utf-8")
    (git_dir / "refs" / "heads" / "master").write_text("a" * 40 + "\n", encoding="utf-8")
    from webui.events import read_git_head

    assert read_git_head(tmp_path) == "a" * 40


def test_read_git_head_packed_refs(tmp_path):
    """`git pack-refs`/`git gc` legt den Ref in `packed-refs` — der HEAD zeigt weiterhin
    auf den Branch-Namen, die Datei unter `refs/` fehlt."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/master\n", encoding="utf-8")
    (git_dir / "packed-refs").write_text(
        "# pack-refs with: peeled fully-peeled sorted\n"
        f"{'b' * 40} refs/heads/master\n",
        encoding="utf-8",
    )
    from webui.events import read_git_head

    assert read_git_head(tmp_path) == "b" * 40


def test_read_git_head_detached(tmp_path):
    """Ein **detached HEAD** trägt den Hash direkt in `HEAD` — kein Ref, kein Branch."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir(parents=True)
    (git_dir / "HEAD").write_text(f"{'c' * 40}\n", encoding="utf-8")
    from webui.events import read_git_head

    assert read_git_head(tmp_path) == "c" * 40


def test_read_git_head_without_repo_is_none(tmp_path):
    """Kein Repo → `None`. Der Feed darf daraus **nichts** melden (lieber still als falsch)."""
    from webui.events import read_git_head

    assert read_git_head(tmp_path) is None


# -- 2. Die Quelle: changed_spaces() --------------------------------------------------------


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_changed_spaces_maps_paths_and_trash(tmp_path):
    """Der **erste** Pfadbestandteil ist der Space; `._trash/<space>/…` ist der Papierkorb
    (eine Ebene höher als ein Space); Dateien in der Wurzel gehören zu keinem Space."""
    repo = tmp_path / "data"
    (repo / "alpha").mkdir(parents=True)
    (repo / "._trash" / "beta").mkdir(parents=True)
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")
    (repo / "alpha" / "notiz.md").write_text("a\n", encoding="utf-8")
    (repo / "._trash" / "beta" / "weg.md").write_text("b\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".index.sqlite3*\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "erster")
    first = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True,
    ).stdout.strip()

    (repo / "alpha" / "notiz.md").write_text("a2\n", encoding="utf-8")
    (repo / "gamma" / "neu.md").parent.mkdir(parents=True)
    (repo / "gamma" / "neu.md").write_text("c\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "zweiter")
    second = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True,
    ).stdout.strip()

    from webui.events import changed_spaces

    spaces = changed_spaces(repo, first, second)
    assert spaces == {"alpha", "gamma"}


def test_changed_spaces_maps_the_trash_to_its_space(tmp_path):
    """Ein Item, das in den Papierkorb wandert, meldet **seinen** Space — der Papierkorb
    liegt unter `._trash/<space>/`, also ist das zweite Segment der Space-Name."""
    repo = tmp_path / "data"
    (repo / "._trash" / "beta").mkdir(parents=True)
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")
    (repo / "._trash" / "beta" / "weg.md").write_text("b\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "erster")
    first = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True,
    ).stdout.strip()
    (repo / "._trash" / "beta" / "weg.md").unlink()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "zweiter")
    second = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True,
    ).stdout.strip()

    from webui.events import changed_spaces

    assert changed_spaces(repo, first, second) == {"beta"}


# -- 3. Der Feed ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_store_write_reaches_subscriber_within_two_intervals(tmp_path):
    """Der **echte** Weg: ein `Store`-Write macht einen Commit (Hard Rule 5), der Commit
    bewegt den HEAD, und der Feed meldet den Space — innerhalb von zwei Intervallen."""
    data_root = tmp_path / "data"
    data_root.mkdir()
    store = Store(data_root, git=True)
    store.create("alpha", type="note", title="Vorher")

    feed = ChangeFeed(data_root, interval_s=0.05)
    task = asyncio.create_task(feed.subscribe().__anext__())
    await asyncio.sleep(0.1)  # der Feed muss laufen, bevor geschrieben wird
    store.create("alpha", type="note", title="Nachher")

    event = await asyncio.wait_for(task, timeout=5)
    assert "alpha" in event.spaces
    assert event.head


@pytest.mark.asyncio
async def test_feed_starts_and_stops_with_subscribers(tmp_path):
    """Der Poll-Task startet mit dem ersten Abonnenten und endet mit dem letzten."""
    feed = ChangeFeed(tmp_path, interval_s=0.02)
    assert feed.subscriber_count == 0

    agen = feed.subscribe()
    pending = asyncio.create_task(agen.__anext__())
    await asyncio.sleep(0.05)
    assert feed.subscriber_count == 1

    pending.cancel()
    try:
        await pending
    except (asyncio.CancelledError, StopAsyncIteration):
        pass
    await asyncio.sleep(0.05)
    assert feed.subscriber_count == 0


@pytest.mark.asyncio
async def test_feed_aclose_ends_streams(tmp_path):
    """`aclose()` beendet alle Abonnements — der Wartende bekommt ein Ende, kein Warten."""
    feed = ChangeFeed(tmp_path, interval_s=0.02)
    agen = feed.subscribe()
    pending = asyncio.create_task(agen.__anext__())
    await asyncio.sleep(0.05)

    await feed.aclose()
    with pytest.raises(StopAsyncIteration):
        await asyncio.wait_for(pending, timeout=5)


# -- 4. Die Route --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_events_require_session(events_app, tmp_path):
    """Ohne Sitzung: 401 — der Stream ist eine Session-Fläche wie jede andere (`/api` kennt
    keine Bearer-Token, P5-D)."""
    feed = ChangeFeed(tmp_path, interval_s=0.02)
    app = events_app(feed)
    task, state = await _call(app)
    await asyncio.wait_for(task, timeout=5)
    assert state["status"] == 401
    assert json.loads(_text(state))["error"] == "unauthenticated"


@pytest.mark.asyncio
async def test_events_filter_invisible_spaces(events_app, item_store, store, tmp_path):
    """**Ein unsichtbarer Space-Name verlässt den Server nie.**

    Der Feed meldet beide Spaces; die Route filtert über `_visible_space_infos()` — der
    fremde Space ist ohne Freigabe nicht sichtbar und taucht deshalb nicht im Ereignis auf."""
    item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    feed = ChangeFeed(
        tmp_path, interval_s=0.02, head_reader=_fake_head([0]),
        differ=lambda _root, _old, _new: {SPACE, FOREIGN_SPACE},
    )
    app = events_app(feed)
    task, state = await _call(app, cookie=_session_cookie(store))
    await asyncio.sleep(0.2)
    task.cancel()

    text = _text(state)
    assert "event: changed" in text
    daten = json.loads(text.split("data: ", 1)[1].split("\n", 1)[0])
    assert daten["spaces"] == [SPACE]


@pytest.mark.asyncio
async def test_events_heartbeat_revalidates_and_closes_expired_session(
    events_app, store, tmp_path, monkeypatch
):
    """Der Herzschlag prüft die Sitzung neu — eine abgelaufene Sitzung **beendet** den
    Stream, statt ihn offenzuhalten."""
    monkeypatch.setattr("webui.api.HEARTBEAT_SECONDS", 0.05)
    feed = ChangeFeed(tmp_path, interval_s=0.02)
    app = events_app(feed)
    cookie = _session_cookie(store)
    task, state = await _call(app, cookie=cookie)
    await asyncio.sleep(0.15)
    assert ": ping" in _text(state), "der Herzschlag kommt nicht an"

    # Die Sitzung widerrufen — sie ist ab jetzt ungültig.
    session_id = cookie.split("=", 1)[1]
    store.revoke_session(session_id, reason="test")

    await asyncio.wait_for(task, timeout=5)
    assert state["complete"], "der Stream wurde nicht beendet"


@pytest.mark.asyncio
async def test_events_limit_three_streams_per_session(events_app, store, tmp_path):
    """Höchstens drei Streams je Sitzung; der vierte bekommt 429."""
    feed = ChangeFeed(tmp_path, interval_s=0.05)
    app = events_app(feed)
    cookie = _session_cookie(store)
    tasks = []
    for _ in range(3):
        task, _state = await _call(app, cookie=cookie)
        tasks.append(task)
    await asyncio.sleep(0.1)

    task, state = await _call(app, cookie=cookie)
    await asyncio.wait_for(task, timeout=5)
    assert state["status"] == 429
    assert json.loads(_text(state))["error"] == "rate_limited"

    for task in tasks:
        task.cancel()


@pytest.mark.asyncio
async def test_events_send_nothing_when_only_invisible_spaces_changed(
    events_app, item_store, store, tmp_path
):
    """**Kein Ereignis, wenn sich nur Unsichtbares geändert hat** (Abnahme P10.5-46,
    Gegenlauf: „unsichtbarer Space → kein Ereignis").

    Der Space-Name dürfte den Server ohnehin nicht verlassen (Hard Rule 4); ein leeres
    Ereignis würde den Client trotzdem zum Nachladen auffordern — also wird gar keines
    gesendet. **Gegenprobe:** derselbe Feed, aber der Feed meldet einen **sichtbaren**
    Space — dann kommt ein Ereignis an."""
    item_store.create(FOREIGN_SPACE, type="note", title="Fremd, ungeteilt")
    feed = ChangeFeed(
        tmp_path, interval_s=0.02, head_reader=_fake_head([0]),
        differ=lambda _root, _old, _new: {FOREIGN_SPACE},
    )
    app = events_app(feed)
    task, state = await _call(app, cookie=_session_cookie(store))
    await asyncio.sleep(0.25)
    task.cancel()
    assert "event: changed" not in _text(state), (
        "es wurde ein Ereignis gesendet, obwohl sich nur ein unsichtbarer Space geaendert hat"
    )


@pytest.mark.asyncio
async def test_events_report_the_head_and_the_changed_spaces(
    events_app, item_store, store, tmp_path
):
    """Das Ereignis nennt die **geänderten** Spaces und den **HEAD** (zwölf Zeichen) — mehr
    nicht. Kein Body, kein Titel: der Server ist dumm, und ein fremder Inhalt im Ereignis
    wäre ein Datenleck an der Rechteprüfung vorbei."""
    item_store.create(SPACE, type="note", title="Eigen")
    feed = ChangeFeed(
        tmp_path, interval_s=0.02, head_reader=_fake_head([0]),
        differ=lambda _root, _old, _new: {SPACE},
    )
    app = events_app(feed)
    task, state = await _call(app, cookie=_session_cookie(store))
    await asyncio.sleep(0.2)
    task.cancel()

    text = _text(state)
    daten = json.loads(text.split("data: ", 1)[1].split("\n", 1)[0])
    assert daten["spaces"] == [SPACE]
    assert len(daten["head"]) == 12
    assert "body" not in daten and "title" not in daten
