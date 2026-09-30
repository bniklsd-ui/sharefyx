"""Tests fuer den `fastmcp`-Pin — P9 Step H, Plan §10.

Der Plan §10 ging von „installiert ist 3.4.4" aus. Gemessen am 2026-09-30 ist das falsch, und
der Unterschied ist der eigentliche Fund des Steps:

| Ort | fastmcp | mcp |
|---|---|---|
| Live-Release `/opt/sharefyx/current/.venv` (read-only) | **3.4.7** | 1.30.0 |
| Dev-`.venv` | 3.4.4 | 1.28.1 |
| `phase2_mcp/pyproject.toml` (seit dem ersten Commit) | `>=3.4,<3.5` | — |

`deploy.sh:153` baut pro Release ein **frisches** venv und `scripts/dev_install.sh:9-13`
installiert die Phasenpakete editable; ein Range-Pin loest damit bei jedem Deploy auf das
damalige neueste 3.4.x auf. Der Patch-Versionswechsel hat also bereits stattgefunden — vom
3.4.4 auf 3.4.7, mit dem Release vom 2026-09-18, unbemerkt. Genau das verbietet P3-D
(`phase3_edge_plan.md:106`): „Patchversionen aendern hier Verhalten, und unter einem Dauerdienst
darf sich das nicht unbemerkt bewegen." P3-D und P4-R behaupteten beide einen exakten Pin, den
der Code bis heute nie hatte — dieser Test ist die Einloesung dieses Anspruchs, nicht eine
neue Erfindung.

  1. test_the_pin_is_an_exact_version              # kein Range, dreiteilige Version
  2. test_the_pin_stays_inside_the_three_line      # P9-R: 3.4.x, 4.x bleibt V79
  3. test_only_one_pyproject_declares_fastmcp      # ein zweiter Pin koennte dem Deploy widersprechen
  4. test_the_installed_fastmcp_matches_the_pin    # der eigentliche Riegel
  5. test_the_pin_comment_points_at_p9_r_and_v79   # Sperrverweis und Nachfolger bleiben sichtbar

Test 4 ist der einzige, der den laufenden Betrieb sieht — und genau deshalb ist er es wert: er
laeuft im **Release-venv** mit, weil `deploy.sh:169` dort `pytest -q` aufruft und den Deploy bei
Fehlschlag abbricht. Damit ist ein stiller Patch-Drift ein roter Deploy und keine Randnotiz in
einem Plan. Er ist zugleich der teuerste Test der Datei: er schlaegt an, wenn das Dev-venv
absichtlich von der Pin-Zeile abweicht. Das ist gewollt — die Abweichung gehoert dann in den
Pin oder in den Befund, nicht in die lokale Umgebung.

Kein Netz, kein Dienst, kein root. Test 4 liest nur die installierte Version des laufenden
Interpreters (`importlib.metadata`), startet nichts und spricht nichts an.
"""

from __future__ import annotations

import tomllib
from importlib.metadata import PackageNotFoundError, version as installed_version
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "phase2_mcp" / "pyproject.toml"
# Verzeichnisse, in denen ein `pyproject.toml` nichts über den Betrieb sagt: das Dev-venv und
# ggf./vendor-Zeug. Ohne diese Liste fände der Test 3 die mitinstallierten Fremdpakete.
_SKIP_DIR_PARTS = {".venv", ".git", "node_modules", "vendor"}


def _fastmcp_requirement() -> Requirement:
    """Die eine `fastmcp`-Zeile aus `phase2_mcp/pyproject.toml`, geparst."""
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    declared = [
        Requirement(dep) for dep in data["project"]["dependencies"] if "fastmcp" in dep.lower()
    ]
    assert len(declared) == 1, f"genau eine fastmcp-Zeile erwartet, gefunden: {declared}"
    return declared[0]


def _pinned_version() -> str:
    """Die gepinnte Version als String — setzt einen *einzigen* Specifier voraus.

    `SpecifierSet` hat kein `.version`; genau das war der erste eigene Fehler in diesem Modul
    (zwei Tests rot, bevor der Helper existierte)."""
    specifiers = list(_fastmcp_requirement().specifier)
    assert len(specifiers) == 1, f"genau ein Specifier erwartet, gefunden: {specifiers}"
    return specifiers[0].version


def _comment_above_dependencies() -> str:
    """Der Kommentarblock direkt ueber der `dependencies`-Zeile, ohne `#`-Praefix.

    Test 5 prueft auf Lock- und Verify-Kuerzel, nicht auf meine Formulierung: eine eigene
    Wortwahl darf den Wächter nicht rot machen, ein geloeschter Verweis auf P9-R/V79 schon.
    """
    lines = PYPROJECT.read_text(encoding="utf-8").splitlines()
    anchor = next(i for i, line in enumerate(lines) if line.startswith("dependencies"))
    block: list[str] = []
    for line in reversed(lines[:anchor]):
        stripped = line.strip()
        if stripped.startswith("#"):
            block.append(stripped.lstrip("#").strip())
        elif stripped:
            break
    return "\n".join(reversed(block))


def test_the_pin_is_an_exact_version() -> None:
    """P3-D/P4-R: `==` mit dreiteiliger Version, kein `>=3.4,<3.5`."""
    req = _fastmcp_requirement()
    assert req.name == "fastmcp"
    specifiers = list(req.specifier)
    assert len(specifiers) == 1, f"genau ein Specifier erwartet, gefunden: {specifiers}"
    operator, pinned = specifiers[0].operator, specifiers[0].version
    assert operator == "==", f"Pin muss exakt sein (==), ist aber {operator}{pinned}"
    assert len(pinned.split(".")) == 3, f"Version muss dreiteilig sein, ist {pinned!r}"
    # `==3.4` waere in PEP 440 kein exakter Pin — es liest 3.4.7 mit. Der dritte Teil ist der Witz.
    Version(pinned)


def test_the_pin_stays_inside_the_three_line() -> None:
    """P9-R: `fastmcp` bleibt auf 3.4.x. FastMCP 4 / MCP-Revision 2026-07-28 ist V79,
    eine eigene Mini-Phase seit P5-C — kein Nebenbei-Update dieser Zeile."""
    pinned = _pinned_version()
    assert Version(pinned).major == 3, f"Pin muss in der 3.x-Linie bleiben, ist {pinned}"
    assert Version(pinned).minor == 4, f"Pin muss in der 3.4-Linie bleiben, ist {pinned}"


def test_only_one_pyproject_declares_fastmcp() -> None:
    """Genau eine `fastmcp`-Zeile im ganzen Repo.

    Ein zweiter Pin — etwa in `phase4_auth` — koennte dem Deploy widersprechen, und welcher
    gewinnt, entscheidet pip nach Dateialphabet, nicht nach Absicht."""
    declaring: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("pyproject.toml")):
        if _SKIP_DIR_PARTS & set(path.relative_to(REPO_ROOT).parts):
            continue
        if "fastmcp" in path.read_text(encoding="utf-8").lower():
            declaring.append(path.relative_to(REPO_ROOT))
    assert declaring == [Path("phase2_mcp/pyproject.toml")], (
        f"fastmcp darf nur in phase2_mcp/pyproject.toml gepinnt werden, gefunden: {declaring}"
    )


def test_the_installed_fastmcp_matches_the_pin() -> None:
    """Der Deploy-Riegel: was installiert ist, ist was deklariert ist.

    Laeuft im Release-venv mit (`deploy.sh:169` ruft dort `pytest -q` und bricht den Deploy bei
    Fehlschlag ab) — deshalb ist ein Patch-Drift ab jetzt ein roter Deploy."""
    pinned = _pinned_version()
    try:
        present = installed_version("fastmcp")
    except PackageNotFoundError:  # pragma: no cover - nur in kaputten Umgebungen
        raise AssertionError(
            "fastmcp ist in diesem Interpreter nicht installiert — die Testumgebung "
            "entspricht nicht dem, was deploy.sh installiert"
        ) from None
    assert present == pinned, (
        f"installiert ist fastmcp {present}, gepinnt ist {pinned} — "
        "Versionen auseinanderlaufen lassen heisst Drift unter einem Dauerdienst (P3-D)"
    )


def test_the_pin_comment_points_at_p9_r_and_v79() -> None:
    """Der Kommentar nennt den Lock (P9-R) und den Nachfolger (V79).

    Sonst steht ein exakter Pin da, und in drei Jahren fragt jemand, warum nicht 4.x — ohne
    dass die Antwort im Code steht. Geprueft werden die Kuerzel, nicht der Satzbau."""
    comment = _comment_above_dependencies()
    assert "P9-R" in comment, "der Pin-Kommentar muss P9-R nennen (Obergrenze 3.4.x)"
    assert "V79" in comment, "der Pin-Kommentar muss V79 nennen (FastMCP 4, eigene Mini-Phase)"
    assert "P3-D" in comment, "der Pin-Kommentar muss P3-D nennen (der Grund fuer exakt statt Range)"
