"""`SessionManager` — Cookie-Logik über die Step-2-`AuthStore`-Methoden (`create_session`,
`touch_session`, `revoke_session`), kein eigenes SQL (Plan §2.7).

Cookie exakt: `__Host-sfx_session=<id>; Path=/; Secure; HttpOnly; SameSite=Strict`. Kein
`Domain`, kein `Max-Age` (Browser-Session-Cookie; die Lebensdauer ist serverseitig über
`ui_sessions.absolute_expires_at`/`last_seen_at` geregelt, nicht über das Cookie selbst).
`__Host-` verlangt genau das: kein `Domain`, `Path=/`, `Secure` — ohne diese drei akzeptiert
kein Browser das Präfix.
"""
from __future__ import annotations

from authserver.models import SessionRow
from authserver.store import AuthStore
from starlette.requests import Request
from starlette.responses import Response

from .config import COOKIE_NAME, UiSettings


class SessionManager:
    def __init__(self, store: AuthStore, *, settings: UiSettings) -> None:
        self._store = store
        self._settings = settings

    def issue(self, response: Response, *, space: str) -> str:
        """Mintet eine neue Sitzung, setzt das Cookie auf `response`, gibt den CSRF-Token
        (Klartext, nur dieses eine Mal) zurück."""
        session_id, csrf_token = self._store.create_session(
            space=space,
            idle_ttl_s=self._settings.idle_ttl_s,
            absolute_ttl_s=self._settings.absolute_ttl_s,
        )
        self._set_cookie(response, session_id)
        return csrf_token

    def load(self, request: Request) -> SessionRow | None:
        """Einziger Lesepfad (Plan §2.7) — ruft `touch_session()`, das `last_seen_at` in
        derselben Transaktion aktualisiert. Kein Cookie → `None`, nie eine Ausnahme."""
        session_id = request.cookies.get(COOKIE_NAME)
        if session_id is None:
            return None
        return self._store.touch_session(session_id, idle_ttl_s=self._settings.idle_ttl_s)

    def rotate(self, request: Request, response: Response, *, space: str) -> str:
        """Widerruft eine vorhandene Sitzung (falls ein Cookie mitkam) und mintet eine neue —
        ID-Rotation bei jedem erfolgreichen Login (P5-E), verhindert Session-Fixation."""
        old_session_id = request.cookies.get(COOKIE_NAME)
        if old_session_id is not None:
            self._store.revoke_session(old_session_id, reason="rotated")
        return self.issue(response, space=space)

    def clear(self, response: Response, session_id: str | None, reason: str) -> None:
        """Widerruft serverseitig (falls eine ID übergeben wurde) und löscht das Cookie in
        jedem Fall — auch wenn `session_id` `None` ist (abgelaufenes/schon widerrufenes Cookie
        im Browser muss trotzdem verschwinden)."""
        if session_id is not None:
            self._store.revoke_session(session_id, reason=reason)
        response.delete_cookie(COOKIE_NAME, path="/", secure=True, httponly=True, samesite="strict")

    def _set_cookie(self, response: Response, session_id: str) -> None:
        response.set_cookie(
            COOKIE_NAME,
            session_id,
            path="/",
            domain=None,
            max_age=None,
            secure=True,
            httponly=True,
            samesite="strict",
        )
