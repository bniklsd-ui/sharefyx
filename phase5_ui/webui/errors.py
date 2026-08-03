"""Fehlertypen der UI-Anmeldewege — analog `authserver/errors.py`, aber eigene, kleinere Menge:
die UI unterscheidet noch nicht nach RFC-Fehlercodes wie OAuth. Wächst in Step 5 um `ApiError`
(stabile JSON-Fehlercodes für `/api/v1/*`, Plan §3.1) — bewusst noch nicht hier, Step 3 kennt
nur die Wege, auf denen es diese Codes noch nicht braucht (Login, Logout).
"""
from __future__ import annotations


class UiError(Exception):
    """Basis für alle UI-Auth-Fehler; `status_code` steuert die HTTP-Antwort, `message` ist
    Klartext für `pages.render_error_page()` (nie Nutzereingabe, siehe dortiger Docstring)."""

    def __init__(self, message: str, *, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class CsrfError(UiError):
    """Wird von `security.require_csrf()` geworfen (Plan §2.7) — immer 403, nie eine
    unterscheidbare Detailmeldung nach außen (dieselbe Enumerationsdisziplin wie OAuth)."""

    def __init__(self, message: str = "Anfrage abgelehnt (CSRF-Prüfung fehlgeschlagen)") -> None:
        super().__init__(message, status_code=403)
