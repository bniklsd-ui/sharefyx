"""Doc-health scan: index_lines, header_cards, updown_links, oversize.

Reads the repo's .md files and docs/INDEX.md, prints a JSON report to stdout, logs to
stderr (Hard Rule 7). No LLM calls, no interpretation of content — pure filesystem/regex
checks, same spirit as the rest of the server tooling.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OVERSIZE_BYTES = 40 * 1024
NAMED_OVERSIZE_MARKER = "benannt statt versteckt"

SNAPSHOT_GLYPHS = {"📕", "📦"}

# The four documented exceptions from docs/INDEX.md's own header (Ausnahmen-Absatz):
# harness files, test fixtures, machine-parsed files, vendor/license text.
CARD_EXEMPT = {
    ".claude/RESUME.md",
    "phase6_shares/tests/golden/archived.md",
    "phase6_shares/tests/golden/drift_repaired.md",
    "phase6_shares/tests/golden/roundtrip_create.md",
    "docs/UPDATE_LOG.md",
    "phase5_ui/THIRD_PARTY_LICENSES.md",
    "phase5_ui/vendor/lucide/README.md",
}

INDEX_LINE_EXEMPT = CARD_EXEMPT

IGNORE_DIR_PARTS = {".git", ".pytest_cache", "node_modules", ".venv", "vendor/plex"}


def _iter_markdown(repo_root: Path):
    for path in sorted(repo_root.rglob("*.md")):
        rel = path.relative_to(repo_root)
        parts = set(rel.parts)
        if parts & IGNORE_DIR_PARTS:
            continue
        if any(part.startswith(".") and part not in (".claude",) for part in rel.parts[:-1]):
            continue
        yield rel, path


def _read_index_lines(index_path: Path) -> str:
    return index_path.read_text(encoding="utf-8")


def check_index_lines(repo_root: Path, index_text: str) -> list[str]:
    findings = []
    for rel, _path in _iter_markdown(repo_root):
        rel_str = str(rel)
        if rel_str in INDEX_LINE_EXEMPT:
            continue
        if rel_str == "docs/INDEX.md":
            continue
        # Path-keyed, not bare-filename: "CLAUDE.md" alone appears in a dozen INDEX bullets,
        # so a bare-name check would pass a brand-new phaseN/CLAUDE.md for free forever.
        if _index_line_for(index_text, rel_str) is None:
            findings.append(f"{rel_str}: keine Zeile in docs/INDEX.md")
    return findings


def _parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    closers = [m.start() for m in re.finditer(r"^---\s*$", text, flags=re.MULTILINE)]
    if len(closers) < 2:
        return None
    fm_text = text[closers[0] : closers[1]]
    fields: dict[str, str] = {}
    for key in ("status", "purpose", "read-when", "detail"):
        m = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm_text, flags=re.MULTILINE)
        if m:
            fields[key] = m.group(1).strip()
    return fields


def check_header_cards(repo_root: Path) -> list[str]:
    findings = []
    for rel, path in _iter_markdown(repo_root):
        rel_str = str(rel)
        if rel_str in CARD_EXEMPT:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        if fm is None:
            findings.append(f"{rel_str}: keine erkennbare Frontmatter-Card")
            continue
        missing = [k for k in ("status", "purpose", "read-when", "detail") if k not in fm]
        if missing:
            findings.append(f"{rel_str}: Card fehlt Felder {missing}")
    return findings


_KEY_LINE_RE = re.compile(r"^([a-zA-Z_-]+):\s*(.*)$")
_DOWN_ITEM_RE = re.compile(r"^\s+-\s*([^\s#]+)")


def _extract_link_paths(fm_text: str) -> list[str]:
    """Only 'up:'/'down:' — a bullet under an unrelated key (e.g. a rotated 'updated:'
    chain that happens to use '- ' formatting) must never be read as a link."""
    paths: list[str] = []
    in_down_block = False
    for line in fm_text.splitlines():
        key_match = _KEY_LINE_RE.match(line)
        if key_match:
            key, rest = key_match.group(1), key_match.group(2).strip()
            in_down_block = False
            if key == "up" and rest:
                paths.append(rest.split("#", 1)[0].strip())
            elif key == "down":
                in_down_block = True
            continue
        if in_down_block:
            m = _DOWN_ITEM_RE.match(line)
            if m:
                paths.append(m.group(1))
            elif line.strip():
                in_down_block = False
    return paths


def check_updown_links(repo_root: Path) -> list[str]:
    findings = []
    for rel, path in _iter_markdown(repo_root):
        rel_str = str(rel)
        if rel_str in CARD_EXEMPT:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        closers = [m.start() for m in re.finditer(r"^---\s*$", text, flags=re.MULTILINE)]
        if len(closers) < 2:
            continue
        fm_text = text[closers[0] : closers[1]]
        for link in _extract_link_paths(fm_text):
            resolved = (path.parent / link).resolve()
            if not resolved.exists():
                findings.append(f"{rel_str}: Link löst nicht auf: {link}")
    return findings


_GLYPH_RE = re.compile(r"\]\([^)]*\)\s*(?:—|--)\s*([\U0001F300-\U0001FAFF☀-➿])")


def _index_line_for(index_text: str, rel_str: str) -> str | None:
    # Key on the fuller relative path, not the bare filename — "CLAUDE.md" alone collides
    # across a dozen phase heads and would silently match the wrong bullet.
    candidates = [rel_str]
    if rel_str.startswith("docs/"):
        candidates.append(rel_str[len("docs/") :])
    for line in index_text.splitlines():
        if not line.strip().startswith("- ["):
            continue
        if any(f"]({c})" in line or f"](../{c})" in line or f"](./{c})" in line for c in candidates):
            return line
    return None


_APPROX_KB_RE = re.compile(r"~\s*(\d+)\s*KB")
_EXACT_BYTES_RE = re.compile(r"(\d[\d.]*)\s*B\b")


def _named_size_is_current(line: str, size: int) -> bool:
    """Accepts either an exact byte figure or a rounded '~NNKB' — as long as it's within
    ~30% of the real size. Catches stale numbers (e.g. '~22KB' for a 64KB file) without
    demanding byte-exact text every convention example doesn't actually use."""
    actual_kb = size / 1024
    m = _EXACT_BYTES_RE.search(line)
    if m:
        exact = int(m.group(1).replace(".", ""))
        if exact == size:
            return True
    m = _APPROX_KB_RE.search(line)
    if m:
        written_kb = int(m.group(1))
        # Fixed absolute band, not a percentage — a percentage widens the blind spot as the
        # file grows (30% of 106KB is a 32KB gap a genuinely stale number could hide inside).
        if abs(written_kb - actual_kb) <= 2:
            return True
    return False


def check_oversize(repo_root: Path, index_text: str) -> list[str]:
    findings = []
    for rel, path in _iter_markdown(repo_root):
        rel_str = str(rel)
        size = path.stat().st_size
        if size <= OVERSIZE_BYTES:
            continue
        line = _index_line_for(index_text, rel_str)
        glyph_match = _GLYPH_RE.search(line) if line else None
        glyph = glyph_match.group(1) if glyph_match else None
        if glyph in SNAPSHOT_GLYPHS:
            continue
        if line and NAMED_OVERSIZE_MARKER in line and _named_size_is_current(line, size):
            continue
        findings.append(
            f"{rel_str}: {size} B > {OVERSIZE_BYTES} B, glyph={glyph!r}, nicht als 📕/📦 markiert "
            f"und nicht mit aktueller Größe benannt"
        )
    return findings


def run(repo_root: Path) -> dict:
    index_path = repo_root / "docs" / "INDEX.md"
    index_text = _read_index_lines(index_path)
    return {
        "index_lines": check_index_lines(repo_root, index_text),
        "header_cards": check_header_cards(repo_root),
        "updown_links": check_updown_links(repo_root),
        "oversize": check_oversize(repo_root, index_text),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    report = run(repo_root)
    total = sum(len(v) for v in report.values())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"doc_health: {total} Befund(e) gesamt", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
