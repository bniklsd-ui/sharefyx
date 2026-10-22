"""Tests fuer den `fastmcp`-Pin — P9 Step H, Plan §10 — und fuer die Versions-Quelle
`constraints.txt` (P10.5 Block 1, Schritt 1.4; BT-6, Lock P10.5-Q).

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

Dazu zwei Wächter fuer `constraints.txt` (P10.5 Block 1, Schritt 1.4 — BT-6, D-13). Der Pin auf
`fastmcp` allein loest BT-6 nicht: das *transitive* `mcp` blieb ungepinnt, und die Live- und
Dev-Umgebungen liefen auseinander (`mcp` live 1.30.0 gegen dev 1.28.1, `starlette` live 1.7.0
gegen dev 1.3.1, gemessen 2026-10-22). P10.5-Q macht `constraints.txt` zur einzigen Quelle
aller transitiven Versionen — Dev und Deploy ueber **einen** Weg (`scripts/dev_install.sh`).

  6. test_dev_install_uses_the_constraints_file     # `-c constraints.txt`, und ohne die Datei Abbruch
  7. test_every_installed_distribution_matches_the_constraints   # installiert == gepinnt

Test 4 ist der einzige, der den laufenden Betrieb sieht — und genau deshalb ist er es wert: er
laeuft im **Release-venv** mit, weil `deploy.sh:169` dort `pytest -q` aufruft und den Deploy bei
Fehlschlag abbricht. Damit ist ein stiller Patch-Drift ein roter Deploy und keine Randnotiz in
einem Plan. Er ist zugleich der teuerste Test der Datei: er schlaegt an, wenn das Dev-venv
absichtlich von der Pin-Zeile abweicht. Das ist gewollt — die Abweichung gehoert dann in den
Pin oder in den Befund, nicht in die lokale Umgebung. Test 7 hat dieselbe Form und dieselbe
Wirkung fuer die transitive Ebene.

Kein Netz, kein Dienst, kein root. Test 4 liest nur die installierte Version des laufenden
Interpreters (`importlib.metadata`), startet nichts und spricht nichts an. Test 6 ruft das
Installationsskript in einer Kopie auf, **ohne** die Datei `constraints.txt` — es bricht dort
ab, bevor pip laeuft, also ohne Netz und ohne Aenderung an der Umgebung.
"""

from __future__ import annotations

import importlib.metadata
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
from importlib.metadata import PackageNotFoundError, version as installed_version
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "phase2_mcp" / "pyproject.toml"
DEV_INSTALL = REPO_ROOT / "scripts" / "dev_install.sh"
CONSTRAINTS = REPO_ROOT / "constraints.txt"
# Verzeichnisse, in denen ein `pyproject.toml` nichts über den Betrieb sagt: das Dev-venv und
# ggf./vendor-Zeug. Ohne diese Liste fände der Test 3 die mitinstallierten Fremdpakete.
_SKIP_DIR_PARTS = {".venv", ".git", "node_modules", "vendor"}

# Die Menge, die `pip freeze` selbst auslässt (pip, setuptools, distribute, wheel): der
# Installationsweg, nicht der Abhängigkeits-Abschluss. `pip freeze` erzeugte `constraints.txt`
# — also muss derselbe Wächter dieselbe Menge auslassen, sonst wäre `pip` ein "ungepinntes
# Paket" und der Wächter dauerhaft rot.
_FREEZE_EXCLUDED = {"pip", "setuptools", "distribute", "wheel"}


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


# --- constraints.txt (P10.5 Block 1, Schritt 1.4 — BT-6, Lock P10.5-Q) --------------

def _constraints() -> dict[str, str]:
    """`constraints.txt` als {kanonischer Name: Version}.

    Kanonisch, weil `pip freeze` die Namen so schreibt, wie sie in der Distribution stehen
    (`docstring_parser`, `jaraco.classes`), `importlib.metadata` aber die kanonische Form
    liefert (`docstring-parser`, `jaraco-classes`). Vergleichen kann man nur eine Form.
    """
    constraints: dict[str, str] = {}
    for raw in CONSTRAINTS.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, sep, version = line.partition("==")
        assert sep and version, f"unerwartete Form in constraints.txt: {raw!r}"
        constraints[canonicalize_name(name)] = version
    return constraints


def _project_package_names() -> set[str]:
    """Die Namen der eigenen Pakete — aus den pyprojects, nicht aus einer handgepflegten Liste.

    Eine Liste hier wäre die nächste Stelle, an der etwas veraltet. Die pyprojects sind die
    Wahrheit, und sie stehen im Repo.
    """
    names: set[str] = set()
    for path in sorted(REPO_ROOT.glob("phase*_*/pyproject.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        names.add(canonicalize_name(data["project"]["name"]))
    return names


def _is_editable(dist) -> bool:
    """Installiert aus dem Arbeitsverzeichnis? `direct_url.json` sagt es."""
    try:
        raw = dist.read_text("direct_url.json")
    except OSError:  # pragma: no cover - nur in kaputten Umgebungen
        return False
    if not raw:
        return False
    return bool(json.loads(raw).get("dir_info", {}).get("editable"))


def test_dev_install_uses_the_constraints_file() -> None:
    """`scripts/dev_install.sh` installiert mit `-c constraints.txt` — und braucht die Datei.

    Zwei Haelften, weil zwei Dinge getrennt verschwinden koennen:

    * **Die Form:** ohne `-c` waere die Datei nur eine Liste, die niemand liest. Geprueft
      wird an der pip-Zeile selbst, nicht an einer Erwahnung im Kommentar — dieselbe
      Unterscheidung wie in `test_tail_proxy.py::_directives_only`.
    * **Die Härte:** fehlt die Datei, muss das Skript **abbrechen**. Ein stiller Fallback
      („installiere halt die neueste Version") waere genau der Drift, den BT-6 abschafft.
      Geprueft wird das **verhaltend**, in einer Kopie des Skripts ohne die Datei: es bricht
      ab, bevor pip laeuft — also ohne Netz und ohne Aenderung an dieser Umgebung.
    """
    script = DEV_INSTALL.read_text(encoding="utf-8")

    install_lines = [
        line for line in script.splitlines()
        if "pip install" in line and "-e" in line
    ]
    assert install_lines, "keine editable pip-install-Zeile im Skript gefunden"
    for line in install_lines:
        assert "-c " in line, \
            f"die editable Installation ohne `-c` — {line.strip()!r}"
        assert "constraints.txt" in line, \
            f"die `-c`-Option zeigt nicht auf constraints.txt — {line.strip()!r}"

    # Verhaltensprobe: dasselbe Skript, aber ohne die Datei im Repo-Wurzel.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        (root / "scripts").mkdir(parents=True)
        shutil.copy(DEV_INSTALL, root / "scripts" / "dev_install.sh")
        # Ein Stub `python`: ohne den Abbruchblock liefe der echte pip-Aufruf. Der Stub
        # beantwortet ihn mit Exit 0 — damit ist das **Fehlen des Abbruchs** der einzige
        # Grund für einen erfolgreichen Lauf, und die Probe braucht weder Netz noch fasst
        # sie das echte venv an. (Der erste Entwurf prüfte das ohne Stub und war grün, weil
        # `python` im PATH der Testumgebung fehlt — der Abbruch wäre nie erreicht worden.)
        stub = Path(tmp) / "python"
        stub.write_text("#!/bin/sh\nexit 0\n")
        stub.chmod(0o755)
        result = subprocess.run(
            ["bash", str(root / "scripts" / "dev_install.sh")],
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PATH": f"{tmp}:{os.environ.get('PATH', '')}"},
        )
    assert result.returncode != 0, \
        "ohne constraints.txt muss das Skript abbrechen — ein stiller Fallback ist der Drift"
    assert "constraints.txt" in result.stderr, \
        f"die Abbruchmeldung nennt die fehlende Datei nicht: {result.stderr!r}"


def test_every_installed_distribution_matches_the_constraints() -> None:
    """Was installiert ist, steht in `constraints.txt` — und umgekehrt.

    BT-6/D-13: das transitive `mcp` war ungepinnt, und die Umgebungen liefen auseinander
    (live `mcp 1.30.0` / `starlette 1.7.0` gegen dev `mcp 1.28.1` / `starlette 1.3.1`,
    gemessen 2026-10-22). `constraints.txt` ist die eine Quelle, und dieser Waechter ist das
    Riegel: er laeuft im **Release-venv** mit (`deploy.sh:169` ruft dort `pytest -q` und
    bricht den Deploy bei Fehlschlag ab), also ist ein Drift ein roter Deploy.

    Ausgenommen sind die vier editierbaren Projektpakete (sie kommen aus dem Arbeitsverzeichnis,
    nicht von PyPI) und die Menge, die `pip freeze` selbst auslaesst (`pip`, `setuptools`,
    `distribute`, `wheel`) — der Installationsweg, nicht der Abhaengigkeits-Abschluss.

    Beide Richtungen werden geprueft: eine installierte Distribution, die nicht in der Datei
    steht, ist genauso ein Drift wie eine abweichende Version, und eine Zeile der Datei, die
    nicht installiert ist, waere eine Luege nach der anderen Seite.
    """
    constraints = _constraints()
    assert constraints, "constraints.txt ist leer — das kann nicht der Live-Stand sein"
    project_packages = _project_package_names()

    installed: dict[str, str] = {}
    unpinned: dict[str, str] = {}
    for dist in importlib.metadata.distributions():
        name = canonicalize_name(dist.metadata["Name"])
        if name in _FREEZE_EXCLUDED:
            continue
        if name in project_packages and _is_editable(dist):
            continue
        if name in constraints:
            installed[name] = dist.version
        else:
            unpinned[name] = dist.version

    assert not unpinned, (
        "installiert, aber nicht in constraints.txt gepinnt: "
        f"{sorted(unpinned)} — Werkzeuge gehoeren nach ~/.claude-code-tools/ (so die "
        "Konvention), oder constraints.txt ist veraltet"
    )

    drifting = {
        name: (version, constraints[name])
        for name, version in installed.items()
        if version != constraints[name]
    }
    assert not drifting, (
        f"Version weicht von constraints.txt ab (installiert, Constraints): {drifting} — "
        "unter einem Dauerdienst darf sich das nicht unbemerkt bewegen (P3-D)"
    )

    missing = sorted(set(constraints) - set(installed))
    assert not missing, (
        f"in constraints.txt gepinnt, aber nicht installiert: {missing} — die Datei beschreibt "
        "eine Umgebung, die es so nicht gibt"
    )
