"""Realtime-Änderungsfeed über Server-Sent Events (P10.5, Block 10, Schritt 10.2 — LG-2,
Lock P10.5-L).

**Die Quelle ist der Git-HEAD des `DATA_ROOT`, nicht ein Write-Hook.** Hard Rule 5 macht aus
jedem erfolgreichen Write einen Commit — also heißt „HEAD hat sich bewegt" genau „die Daten
haben sich geändert". Das gilt für den MCP-Adapter, die Web-Oberfläche und die Hand-Edit im
Texteditor **gleichermaßen**, ohne dass in einen Schreibpfad eingegriffen werden muss. Ein
Eingriff in `Store.create()`/`update()`/`append()` wäre doppelt schlecht: er säße im
`storage/`-Kern (P10.5-F: nur angekündigte Dateien dürfen dort angefasst werden) und er sähe
eine Hand-Edit von außen nicht.

**Was der Server meldet: Space-Namen und ein Commit-Hash. Sonst nichts.** Kein Body, kein
Titel, kein Item-Text — der Server bleibt dumm (Kernprinzip), und ein fremder Body im Ereignis
wäre ein Datenleck durch die Hintertür der Rechteprüfung. Der Client holt sich die Daten
danach **über die normale API**, die ihre Rechte prüft.

**Ein Poll-Task je App.** Zwei offene Tabs desselben Menschen würden sonst zweimal pollen und
zweimal `git diff` laufen lassen. Der Feed pollt einmal und verteilt das Ergebnis an alle
Wartenden; der Task startet mit dem ersten Abonnenten und endet mit dem letzten.

**Kein LLM, keine Deutung.** Der Feed meldet, **dass** sich etwas geändert hat, und in welchem
Space. Was sich geändert hat, sagt die API — die den Unterschied ohnehin besser kennt.
"""
from __future__ import annotations

import asyncio
import logging
import subprocess
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

#: Der Heartschlag-Abstand des SSE-Protokolls (Plan §Block 10, Schritt 10.2): alle 25 s ein
#: `: ping`. Er hält die Verbindung durch Proxies und Zeitgebern offen und ist der Moment, in
#: dem die Sitzung neu geprüft wird.
HEARTBEAT_SECONDS = 25.0

#: Länge des gemeldeten Commit-Hashs. Zwölf Zeichen reichen zum Nachschlagen und lassen das
#: Ereignis klein — der volle Hash stünde ohnehin im Git-Protokoll.
HEAD_CHARS = 12


@dataclass(frozen=True)
class ChangeEvent:
    """Ein Änderungsereignis: der neue HEAD und die **Space-Namen**, die sich verändert haben.

    **Beide Felder gehören zusammen.** Der Client, der den Raum-Namen sieht, muss wissen, zu
    welchem Commit er gehört — sonst zeigt er einen Stand an, der schon wieder alt ist. Der
    Plan zeichnet `subscribe()` als `AsyncIterator[set[str]]` vor; hier trägt das Ereignis den
    Hash **mit**, weil der Route sonst den Kopf des *nächsten* Ereignisses lesen müsste —
    ein Rennen, das bei zwei schnellen Schreibvorgängen sichtbar wird (datierte Abweichung vom
    Plan-Sketch, 2026-10-24)."""

    head: str
    spaces: frozenset[str]


def read_git_head(data_root: Path) -> str | None:
    """Der Commit-Hash, auf den `.git/HEAD` zeigt — oder `None`, wenn es keinen gibt.

    Drei Fälle, alle drei möglich:

    * `HEAD` enthält ``ref: refs/heads/master`` → der Ref wird unter
      `.git/refs/heads/master` nachgeschlagen (eine **Datei**; im Live-`DATA_ROOT` gibt es
      keine `packed-refs` — gemessen am 2026-10-20).
    * `HEAD` enthält ``ref: …``, aber die Ref-Datei fehlt → `.git/packed-refs` wird
      gelesen. Das ist der Zustand nach `git pack-refs`/`git gc`.
    * `HEAD` enthält einen Hash → **detached HEAD**; der Hash ist die Antwort.

    **Kein `git`-Aufruf.** Der HEAD wird alle Sekunde gelesen; ein `git rev-parse` pro Sekunde
    wäre ein Prozess pro Sekunde. Die Datei ist die Quelle (Hard Rule 2: die Dateien sind die
    Wahrheit — hier: die Git-Dateien).

    **Annahme:** `.git` ist ein **Verzeichnis**. Das ist beim `DATA_ROOT` der Fall, weil
    `storage/history.py :: ensure_repo()` dort `git init` macht. Ein Worktree oder ein
    Submodul (`.git` als Datei) kommt in diesem Server nicht vor.
    """
    git_dir = Path(data_root) / ".git"
    try:
        text = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not text:
        return None
    if not text.startswith("ref:"):
        # detached HEAD — der Hash steht direkt in HEAD
        return text
    ref = text.split(":", 1)[1].strip()
    if not ref:
        return None
    try:
        value = (git_dir / ref).read_text(encoding="utf-8").strip()
    except OSError:
        value = ""
    if value:
        return value
    # Der Ref liegt nicht als Datei vor → gepackte Refs.
    try:
        packed = (git_dir / "packed-refs").read_text(encoding="utf-8")
    except OSError:
        return None
    for line in packed.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("^"):
            continue
        parts = line.split()
        if len(parts) == 2 and parts[1] == ref:
            return parts[0]
    return None


def changed_spaces(data_root: Path, old: str, new: str) -> set[str]:
    """Welche Spaces hat der Commit `new` gegenüber `old` verändert?

    `git diff --name-only old new` nennt die geänderten Pfade. Der **erste** Pfadbestandteil
    ist der Space-Name — das ist die Layout-Regel des `DATA_ROOT`: `<space>/<ordner>/<datei>.md`.
    Zwei Sonderfälle:

    * `._trash/<space>/…` — der Papierkorb (P9 Step G) liegt **eine Ebene höher** als ein
      Space; hier ist deshalb das **zweite** Segment der Space-Name.
    * Dateien **in der Wurzel** (`.gitignore`, `.index.sqlite3`, …) gehören zu keinem Space
      und werden ignoriert — sie sind Ableitung, kein Inhalt.

    **Fehlschläge sind still, aber sichtbar.** Kein Git, kein Diff → leere Menge (kein
    Ereignis). Das ist die sichere Richtung: lieber kein Ereignis als ein falsches.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(data_root), "diff", "--name-only", old, new],
            capture_output=True, text=True,
        )
    except OSError as exc:
        logger.critical("git diff fehlgeschlagen (Binary evtl. nicht installiert): %s", exc)
        return set()
    if result.returncode != 0:
        logger.warning(
            "git diff %s..%s fehlgeschlagen: %s", old[:8], new[:8], result.stderr.strip(),
        )
        return set()
    spaces: set[str] = set()
    for line in result.stdout.splitlines():
        path = line.strip()
        if not path:
            continue
        parts = path.split("/")
        if parts[0] == "._trash":
            if len(parts) >= 2:
                spaces.add(parts[1])
            continue
        if len(parts) >= 2:
            spaces.add(parts[0])
    return spaces


class ChangeFeed:
    """Der Änderungsfeed einer App: ein Poll-Task, eine Queue je Abonnent.

    **Der Task startet mit dem ersten Abonnenten und endet mit dem letzten.** Eine App ohne
    offene Streams pollt nicht — kein Git-Aufruf pro Sekunde, nur weil jemand die Seite
    offen hatte und dann weg ist.

    **`head_reader` und `differ` sind einschaltbar.** Nicht für Tests allein: der
    Produktivpfad benutzt die beiden Funktionen dieses Moduls, und ein Test kann mit
    denselben Schwellen arbeiten, die der Feed in echt benutzt (derselbe Code, nicht eine
    nachgebaute Attrappe).
    """

    def __init__(
        self,
        data_root: Path,
        *,
        interval_s: float = 1.0,
        head_reader: Callable[[Path], str | None] = read_git_head,
        differ: Callable[[Path, str, str], set[str]] = changed_spaces,
    ) -> None:
        self._data_root = Path(data_root)
        self._interval = interval_s
        self._head_reader = head_reader
        self._differ = differ
        self._subscribers: set[asyncio.Queue] = set()
        self._task: asyncio.Task | None = None
        self._closed = False
        # Der HEAD **jetzt** — ein Write, der zwischen dem Bauen des Feeds und dem ersten
        # Abonnenten passiert, darf nicht verschluckt werden.
        self._head: str | None = self._head_reader(self._data_root)

    @property
    def head(self) -> str | None:
        """Der zuletzt gesehene HEAD (oder `None`, wenn das Repo noch keinen hat)."""
        return self._head

    @property
    def closed(self) -> bool:
        """Ist der Feed geschlossen? Nach `aclose()` ist er **nicht** wieder verwendbar."""
        return self._closed

    @property
    def subscriber_count(self) -> int:
        """Wie viele Abonnenten gerade warten — für Wächter und Diagnose."""
        return len(self._subscribers)

    async def subscribe(self) -> AsyncIterator[ChangeEvent]:
        """Der Ereignisstrom eines Abonnenten.

        Der Generator endet, wenn der Feed geschlossen wird (`aclose()`) — der Wartende
        bekommt dann `None` und der Stream ist zu.
        """
        queue: asyncio.Queue = asyncio.Queue()
        self._subscribers.add(queue)
        self._start()
        try:
            while True:
                event = await queue.get()
                if event is None:
                    return
                yield event
        finally:
            self._subscribers.discard(queue)
            await self._stop_if_idle()

    async def aclose(self) -> None:
        """Beendet alle Abonnements (Shutdown). Der Feed ist danach **nicht** wieder verwendbar."""
        self._closed = True
        await self._stop_task()
        self._wake_all()
        self._subscribers.clear()

    # -- intern -------------------------------------------------------------------------------

    def _start(self) -> None:
        if self._task is None and not self._closed:
            self._task = asyncio.create_task(self._poll_loop())

    async def _stop_if_idle(self) -> None:
        """Kein Abonnent mehr → der Poll-Task endet."""
        if self._subscribers:
            return
        await self._stop_task()

    async def _stop_task(self) -> None:
        task, self._task = self._task, None
        if task is None or task.done():
            return
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    async def _poll_loop(self) -> None:
        try:
            while self._subscribers:
                await asyncio.sleep(self._interval)
                if self._closed:
                    break
                new_head = self._head_reader(self._data_root)
                if not new_head or new_head == self._head:
                    continue
                old_head, self._head = self._head, new_head
                spaces = (
                    self._differ(self._data_root, old_head, new_head) if old_head else set()
                )
                event = ChangeEvent(head=new_head, spaces=frozenset(spaces))
                for queue in list(self._subscribers):
                    queue.put_nowait(event)
        finally:
            if self._task is asyncio.current_task():
                self._task = None
            self._wake_all()

    def _wake_all(self) -> None:
        """Alle Wartenden aufwecken (Feed geschlossen oder Poll-Task beendet)."""
        for queue in list(self._subscribers):
            queue.put_nowait(None)
