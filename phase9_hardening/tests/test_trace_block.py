"""Wächter für den P9-Block trace — wer arbeitet dran, wer hat zuletzt geändert.

Mini-Plan `docs/concepts/phase9_hardening_block_trace_plan.md` §4. Die Verhaltens-Tests des
Blocks liegen dort, wo die Fixtures wohnen, nicht hier (V176: `phase9_hardening/tests/` hat
kein `conftest.py`):

  - T1–T5 (Kern)      → `phase1_storage/tests/test_store.py`
  - T6 (Git-Autor)    → `phase1_storage/tests/test_history.py`
  - T8/T9 (MCP)       → `phase2_mcp/tests/test_tools.py`
  - T10 (REST)        → `phase5_ui/tests/test_api.py`
  - T11 (P9-Z-Zweig)  → `phase5_ui/tests/test_static_routes.py`
  - **hier**          → die *strukturellen* Wächter, für die es sonst keine Datei gäbe

**Warum der erste Wächter der wichtigste des Blocks ist.** `actor` ist ein optionales Keyword
mit Default `""` (P9-AD), damit 294 Testaufrufe von `create()` nicht rot werden. Der Preis
davon ist bekannt und benannt: **eine vergessene Aufrufstelle fällt nicht mehr auf** — kein
`TypeError`, kein roter Test, nur ein Item, das `updated_by: ""` behält, während sein Nachbar
den Schreiber trägt. Genau diese still fehlende Aufrufstelle ist der Grund für T7: statt den
Typ zu härten, wird die *ganze Klasse* über den AST geprüft. Eine künftige Datei fällt durch
denselben Wächter, nicht nur `tools.py`/`api.py`.

Gemessen (2026-10-02) statt geraten: ein blinder `.<create|update|append>(`-Scan fände in
`phase2_mcp/mcpserver/` und `phase5_ui/webui/` 17 Aufrufe mit diesen Attributnamen, davon **8
Listen- oder dict-Methoden** (`routes.append`, `fields.update`, `result.append`, …). Ein
Wächter, der bei Falsch-Positiven rot wird, wird abgeschaltet — deshalb prüft er am
*Empfänger* (`store` im Namen), nicht am Methodennamen allein.

Kein Netz, kein echter DATA_ROOT, kein Dienst, kein LLM.
"""

from __future__ import annotations

import ast
from pathlib import Path

from storage import history, store as store_mod

REPO_ROOT = Path(__file__).resolve().parents[2]

# Die beiden Adapterpakete, die `Store` benutzen. Kein `storage/` — dort ist `actor` die
# Definition, nicht der Aufrufer.
ADAPTER_PACKAGES = (
    REPO_ROOT / "phase2_mcp" / "mcpserver",
    REPO_ROOT / "phase5_ui" / "webui",
)

# Die neun Schreibmethoden des `Store` (P9-AD, `store.py` nach dem Block). `get`/`search`/
# `list_*` sind Lese- und reine Verzeichnismethoden — kein Akteur, kein `updated_by`.
WRITE_METHODS = frozenset({
    "create", "update", "append", "patch", "archive", "move",
    "trash", "put_asset", "delete_asset",
})

# **Heute leer** (V183, gemessen am 2026-10-02): ausser `tools.py` und `api.py` schreiben nur
# Operator- und Fixture-Skripte (`space_cli.py`, `wegwerf_*`, `mcp_smoke.py`, `ui_smoke.py`,
# `ui_budget.py`), und die bleiben bei `actor=""` (P9-AB). Eine Ausnahme hier ist eine
# **Behauptung im Test**, die man begruenden muss — genau dafuer ist sie benannt und nicht
# einfach ein Kommentar. Wer sie erweitert, muss die Begruendung mitliefern.
ACTOR_ALLOWLIST: dict[tuple[str, int], str] = {}

# Testdateien werden nie gescannt (eine Test-Fixture darf `store.create()` ohne `actor`
# aufrufen — das ist genau der Fall, den P9-AD mit dem Default abdeckt).
def _module_files() -> list[Path]:
    dateien: list[Path] = []
    for paket in ADAPTER_PACKAGES:
        dateien.extend(sorted(p for p in paket.glob("*.py") if not p.name.startswith("test_")))
    return dateien


def _store_calls(datei: Path) -> list[tuple[int, str]]:
    """Alle `store.<Schreibmethode>(...)`-Aufrufe in einer Datei, als `(Zeile, `recv.attr`)`."""
    quelle = datei.read_text(encoding="utf-8")
    baum = ast.parse(quelle, filename=str(datei))
    treffer: list[tuple[int, str, str]] = []
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call) or not isinstance(knoten.func, ast.Attribute):
            continue
        if knoten.func.attr not in WRITE_METHODS:
            continue
        empfaenger = ast.unparse(knoten.func.value)
        # Der Empfaenger-Filter, siehe Moduldocstring: 8 der 17 Attribut-Treffer sind
        # Listen-/dict-Methoden mit demselben Namen.
        if "store" not in empfaenger.lower():
            continue
        treffer.append((knoten.lineno, f"{empfaenger}.{knoten.func.attr}", bool(
            [k for k in knoten.keywords if k.arg == "actor"]
        )))
    return treffer


def test_every_store_write_call_in_the_adapters_carries_an_actor():
    """T7, der Wächter des ganzen Blocks: **jeder** `Store`-Schreibaufruf in `mcpserver/` und
    `webui/` trägt ein `actor=`-Keyword. Nicht nur `tools.py` und `api.py` — ein neues Modul in
    einem der beiden Pakete faellt unter dieselbe Pruefung, sonst waere die Pruefung eine
    Momentaufnahme von zwei Dateinamen.

    Gegenprobe G1 (Plan §4) entfernt genau ein `actor=` an einer `tools.py`-Stelle und macht
    diesen Test rot. Ohne diese Gegenprobe waere nicht belegt, dass er etwas prueft."""
    verstoesse: list[str] = []
    gesehen = 0
    for datei in _module_files():
        for zeile, aufruf, hat_actor in _store_calls(datei):
            if (datei.name, zeile) in ACTOR_ALLOWLIST:
                continue
            gesehen += 1
            if not hat_actor:
                verstoesse.append(f"{datei.relative_to(REPO_ROOT)}:{zeile} {aufruf} ohne actor=")
    assert not verstoesse, "Store-Schreibaufruf ohne Akteur:\n  " + "\n  ".join(verstoesse)
    # Mindestens die heute bekannten Stellen — sonst waere der Test bei einer leeren
    # Dateiliste "gruen", ohne geprueft zu haben (die Dateiliste selbst waere dann leer).
    assert gesehen >= 10, f"nur {gesehen} Store-Schreibaufrufe gefunden — Scanner kaputt?"


def test_no_adapter_ever_writes_updated_by_itself():
    """P9-AA, die negative Haelfte: `updated_by` ist **serververwaltet** und darf von keinem
    Adapter gesetzt werden — weder als Frontmatter-Feld im Body noch als Schreibfeld. Ein
    PATCH, das es mitschickt, scheitert an der Whitelist; ein MCP-Tool kennt keinen Parameter
    dafuer. Geprueft wird ueber den AST, damit ein Kommentar, der das Wort nennt, nicht als
    Fund gilt (dritte Wiederholung derselben Falle im Repo: P8.6 Block H, P9 Step G)."""
    verstoesse: list[str] = []
    for datei in _module_files():
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.keyword) and knoten.arg == "updated_by":
                verstoesse.append(f"{datei.relative_to(REPO_ROOT)}:{knoten.lineno} keyword")
            if isinstance(knoten, ast.Assign):
                for ziel in knoten.targets:
                    if ast.unparse(ziel).endswith(".updated_by"):
                        verstoesse.append(f"{datei.relative_to(REPO_ROOT)}:{knoten.lineno} Zuweisung")
    assert not verstoesse, "Adapter schreibt updated_by selbst:\n  " + "\n  ".join(verstoesse)


def test_the_actor_keyword_exists_on_every_store_write_method():
    """P9-AD an der Signatur, nicht nur am Aufrufer: `actor` ist an **allen neun**
    Schreibmethoden ein optionales Keyword. Ohne das haette eine Aufrufstelle aus den
    `tools.py`-/`api.py`-Tests herausfallen koennen, ohne dass der erste Wächter es merkt —
    der erste Waelter sucht nach dem Keyword, nicht danach, dass es ueberhaupt eins geben
    kann."""
    import inspect

    for name in sorted(WRITE_METHODS):
        methode = getattr(store_mod.Store, name, None)
        assert methode is not None, f"Store.{name} existiert nicht — Liste hier veraltet?"
        parameter = inspect.signature(methode).parameters.get("actor")
        assert parameter is not None, f"Store.{name} hat kein actor-Keyword"
        assert parameter.default == "", f"Store.{name}(actor=…) hat Default {parameter.default!r}"


def test_updated_by_is_a_known_and_a_system_managed_field():
    """Der Kern von P9-AA am Ort, an dem er entschieden wird: in `_KNOWN_FIELDS` (sonst landet
    es in `Item.extra` — F4) **und** in `_SYSTEM_MANAGED_FIELDS` (sonst waere es ueber
    `**fields`/`**changes` setzbar). Die Gegenprobe G2 streicht `updated_by` aus
    `_SYSTEM_MANAGED_FIELDS` und macht diesen Test rot."""
    assert "updated_by" in store_mod._KNOWN_FIELDS
    assert "updated_by" in store_mod._SYSTEM_MANAGED_FIELDS
    # Und `assignee` bleibt ein **gewöhnliches** Feld — der Unterschied zwischen den beiden
    # ist der ganze Unterschied zwischen "Inhalt" und "Aussage ueber den Schreibvorgang".
    assert "assignee" in store_mod._KNOWN_FIELDS
    assert "assignee" not in store_mod._SYSTEM_MANAGED_FIELDS


def test_only_history_builds_the_git_author_arguments():
    """P9-AC, strukturell: `--author` wird an **genau einer** Stelle im Repo gebaut,
    `storage/history.py`. An jeder anderen Stelle waere es eine zweite Form derselben Regel
    (und im Fehlerfall eine zweite, stillere). Die Gegenprobe G5 laesst das Flag weg und
    macht Test 6 in `test_history.py` rot — dieser Test sagt zusaetzlich, warum das die
    einzige erlaubte Stelle ist."""
    funde: list[str] = []
    for datei in REPO_ROOT.rglob("*.py"):
        teile = datei.relative_to(REPO_ROOT).parts
        if ".venv" in teile or "releases" in teile or "__pycache__" in teile:
            continue
        # Testdateien ausgenommen: **dieser** Test enthaelt das Literal `"--author"` in seiner
        # eigenen Assertion. Ein Waechter, der sich selbst zaehlt, muesste man auskommentieren,
        # sobald jemand die Zeile laesst — die Ausnahme ist hier die Regel, nicht der Inhalt.
        if "tests" in teile:
            continue
        quelle = datei.read_text(encoding="utf-8", errors="replace")
        if '"--author"' in quelle or "'--author'" in quelle:
            funde.append(str(datei.relative_to(REPO_ROOT)))
    assert funde == ["phase1_storage/storage/history.py"], funde


def test_a_forbidden_author_is_reported_not_silently_dropped(caplog):
    """P9-ACs Fehlerfall: der verworfene Name erzeugt eine **Warnung** im Log, und der
    Commit laeuft trotzdem (diese zweite Haelfte prueft `test_history.py` ueber echtes Git).
    Ohne die Warnung waere ein Space-Name mit `<` ein Datenfehler, den niemand sieht — der
    Commit waere da, der Autor nicht, und niemand wuesste, dass etwas nicht stimmt."""
    import logging

    assert history._author_args("niklas") == ["--author", "niklas <niklas@sharefyx.invalid>"]
    assert history._author_args("") == [], "ohne Akteur wird gar kein --author gebaut (P9-AB)"

    with caplog.at_level(logging.WARNING, logger="storage.history"):
        for kaputt in ("a<b", "a>b", "a\nb", "a\rb", "<b"):
            assert history._author_args(kaputt) == [], kaputt
    # Eine Warnung **je** verworfenem Namen, nicht eine fuer alle: sonst faellt ein zweiter
    # schlechter Name unter, ohne dass ihn jemand sieht.
    assert caplog.text.count("verworfen") == 5, caplog.text
