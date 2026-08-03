"""Passwortpolitik (P5-O, Plan §2.9) — Länge + Blocklist, kein Zeichenklassenzwang. **Kein
Netzaufruf**, kein HIBP-Range-Query: der Server telefoniert nicht nach Hause, dieselbe Regel wie
das LLM-Verbot (Root-`CLAUDE.md` Bauprinzip).

`[VERIFY]` V30 (Herkunft/Stand der Blocklist) aufgelöst 2026-08-03: `blocklist.txt` ist
`danielmiessler/SecLists`s `Passwords/Common-Credentials/10k-most-common.txt` (MIT-lizenziertes
Repo; die Liste selbst geht auf Mark Burnetts öffentlich freigegebene „10,000 Top Passwords"-Liste
zurück), 10000 Einträge — deckt sich mit dem Plan-Vorschlag „10.000 häufigste Passwörter, ~80 KB"
fast exakt (73 KB real).
"""
from __future__ import annotations

from pathlib import Path

MIN_LEN = 12
MAX_LEN = 128

_BLOCKLIST_PATH = Path(__file__).parent / "blocklist.txt"


def _load_blocklist() -> frozenset[str]:
    lines = _BLOCKLIST_PATH.read_text(encoding="utf-8").splitlines()
    return frozenset(
        line.strip().lower() for line in lines if line.strip() and not line.startswith("#")
    )


_BLOCKLIST = _load_blocklist()  # einmal beim Import geladen, 10000 Einträge sind kein Laufzeitkostenfaktor


def check(password: str, *, space: str) -> list[str]:
    """Leere Liste = in Ordnung. Sonst Klartext-Gründe für die UI.

    **Dokumentierte Abweichung vom Plan-Schnipsel** (wie schon `security.require_csrf()` in
    Step 3): die gedruckte Signatur zeigt nur `check(password)`, aber der Fließtext direkt
    darunter verlangt die „Passwort enthält den Space-Namen"-Ableitung, die ohne `space` nicht
    prüfbar wäre — dieselbe Kategorie Abkürzung im Plan-Text, kein Alleingang.
    """
    reasons: list[str] = []
    if len(password) < MIN_LEN:
        reasons.append(f"Passwort muss mindestens {MIN_LEN} Zeichen lang sein.")
    if len(password) > MAX_LEN:
        reasons.append(f"Passwort darf höchstens {MAX_LEN} Zeichen lang sein.")
    if password.strip().lower() in _BLOCKLIST:
        reasons.append("Passwort ist zu gebräuchlich (Blocklist).")
    if space and space.lower() in password.lower():
        reasons.append("Passwort darf den Space-Namen nicht enthalten.")
    return reasons
