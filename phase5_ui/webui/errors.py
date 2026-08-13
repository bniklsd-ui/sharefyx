"""Fehlertypen der UI/API-Wege. `UiError`/`CsrfError` (Step 3) für die servergerenderten Seiten
(`/ui/*` — HTML-Antworten). `ApiError` (Step 4, Plan §3.1) für `/api/v1/*` — JSON-Antworten,
stabile Fehlercodes, nie HTML. `security.require_csrf()` wirft weiterhin nur `CsrfError`
(einheitliche CSRF-Prüfung für beide Wege, Step 3); `account.py` fängt sie und übersetzt in eine
`ApiError(code="csrf_failed")`, statt eine zweite CSRF-Prüfung zu bauen.
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
    """Wird von `security.require_csrf()` geworfen (Plan §2.7) — immer 403. **Korrektur
    2026-08-03:** dieser Docstring behauptete bis dahin „nie eine unterscheidbare Detailmeldung
    nach außen (dieselbe Enumerationsdisziplin wie OAuth)" — das war schon immer falsch,
    `require_csrf()` wirft drei unterscheidbare Klartextmeldungen ("Herkunft (Origin) stimmt
    nicht", "Herkunft nicht bestimmbar", "CSRF-Token fehlt oder stimmt nicht"), nicht erst seit
    ein Live-Fund des Nikingers `exc.message` auf einer Retry-Seite sichtbar machte
    (`routes_auth.py :: _enroll_confirm`). Das ist unbedenklich: anders als beim OAuth-/UI-Login
    verrät keine dieser drei Meldungen, ob ein Space existiert — sie unterscheiden nur
    Transport-/Formularzustände (fehlende Herkunft, falsche Herkunft, falscher Token), keine
    Kontoexistenz. Docstring korrigiert, Verhalten unverändert."""

    def __init__(self, message: str = "Anfrage abgelehnt (CSRF-Prüfung fehlgeschlagen)") -> None:
        super().__init__(message, status_code=403)


# Plan §3.1 — genau diese elf Codes, kein weiterer ohne Plan-Änderung. **[2026-08-13 Ergänzung,
# P6 Step 7 Commit 5a]:** `reauth_required` kam dazu (`webui/shares.py :: require_share_reauth()`
# — eine rechte-erweiternde `PATCH /api/v1/items/{id}` ohne oder mit falschem `password`/`totp`).
# Bewusst NICHT in der 📕-Plandatei nachgezogen (Doc-Layers: 📕 heißt niemals editieren) — die
# Ergänzung steht stattdessen hier und im Phase-Head-Session-Block, benannte Abweichung von der
# Ausführungsplan-Formulierung, die den Nachtrag dort verlangte.
API_ERROR_STATUS: dict[str, int] = {
    "unauthenticated": 401,
    "csrf_failed": 403,
    "totp_required": 403,
    "forbidden": 403,
    "reauth_required": 403,
    "not_found": 404,
    "conflict": 409,
    "validation_failed": 422,
    "rate_limited": 429,
    "payload_too_large": 413,
    "internal": 500,
}


class ApiError(Exception):
    """Trägt einen der elf stabilen Codes aus Plan §3.1 (Step 7 Commit 5a: `reauth_required`
    dazu, siehe Modulkopf) — dieselbe Validierungsdisziplin wie
    `authserver.errors.OAuthError`/`DCRError`: ein Aufrufer, der sich vertippt, bekommt sofort
    einen `ValueError`, nicht eine stumme falsche Antwort. `detail` trägt z. B. `{"current": …}`
    bei `409 conflict` (Plan §3.1) — leer per Default."""

    def __init__(self, code: str, message: str, *, detail: dict | None = None) -> None:
        if code not in API_ERROR_STATUS:
            raise ValueError(f"kein gültiger API-Fehlercode: {code!r}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.detail = detail if detail is not None else {}
        self.status_code = API_ERROR_STATUS[code]

    def to_json(self) -> dict:
        return {"error": self.code, "message": self.message, "detail": self.detail}
