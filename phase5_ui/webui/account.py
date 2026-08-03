"""`/api/v1/account/*` (Plan §2.8/§3.3, §5 Step 4) — Selbstverwaltung: Passwort, TOTP,
Recovery-Codes, eigene Sessions, eigene Connector-Verbindungen. JSON durchgehend (§3.1: kein
Formular-Encoding, kein HTML in Antworten). Dünn wie `authserver/routes.py`/
`webui/routes_auth.py`: parsen, `UserDirectory`/`AuthStore`/`SessionManager`/`verify_reauth()`
aufrufen, antworten.

Jede Route lädt zuerst die Sitzung (`sessions.load()`) — kein Cookie/abgelaufen → `401
unauthenticated`. State-ändernde Routen prüfen danach CSRF (`X-CSRF-Token`-Header, `/api` kennt
kein Formularfeld, §3.1). Re-Auth-pflichtige Routen (P5-P) verlangen zusätzlich `password` +
`totp` im Body, geprüft über `reauth.verify_reauth()` — Fehlschlag → `403 forbidden` (kein
eigener Code für „Re-Auth fehlgeschlagen": das Konto ist ja schon per Sitzung authentifiziert,
nur diese eine Aktion verlangt frischen Beweis).
"""
from __future__ import annotations

from datetime import datetime

from authserver import totp
from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from . import passwords_policy
from .config import COOKIE_NAME, UiSettings
from .errors import ApiError, CsrfError
from .reauth import verify_reauth
from .security import require_csrf
from .sessions import SessionManager

# Dieselbe Konstante wie `phase4_auth/scripts/provision_user.py :: ISSUER` — ein Authenticator
# zeigt diesen Namen als Konto-Herkunft an, `settings.base_url` wäre dafür unleserlich lang.
TOTP_ISSUER = "sharefyx"


def _iso(dt: datetime) -> str:
    """Plan §3.1: ISO-8601 UTC mit `Z`, dasselbe Format wie `storage.store :: _format_dt()`.
    `AuthStore` liefert Zeitstempel immer UTC-aware (`store.py :: _parse_dt()`)."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _error_response(exc: ApiError) -> JSONResponse:
    return JSONResponse(exc.to_json(), status_code=exc.status_code, headers={"Cache-Control": "no-store"})


def account_routes(
    settings: UiSettings,
    store: AuthStore,
    users: UserDirectory,
    sessions: SessionManager,
) -> list[Route]:
    throttle = LoginThrottle(store, now_fn=store.now)

    async def _require_session(request: Request, *, require_confirmed: bool = True):
        session = sessions.load(request)
        if session is None:
            raise ApiError("unauthenticated", "Keine gültige Sitzung.")
        if require_confirmed:
            # §2.8: solange TOTP unbestätigt ist, ist das Konto nur für den Enrollment-Abschluss
            # freigeschaltet (`/api/v1/account/totp/confirm`, hier explizit ausgenommen) — jede
            # andere Route antwortet `403 totp_required`.
            record = users.get(session.space)
            if record is None or not record.totp_confirmed:
                raise ApiError("totp_required", "TOTP-Einrichtung noch nicht abgeschlossen.")
        return session

    async def _require_csrf_json(request: Request, session) -> None:
        try:
            require_csrf(request, session, settings=settings, form_token=None)
        except CsrfError as exc:
            raise ApiError("csrf_failed", exc.message) from exc

    async def _require_reauth(request: Request, session, body: dict) -> None:
        password = body.get("password")
        code = body.get("totp")
        if not isinstance(password, str) or not isinstance(code, str):
            raise ApiError("validation_failed", "password und totp sind Pflichtfelder.")
        ok = verify_reauth(
            users, throttle, store, space=session.space, password=password,
            second_factor=code, now=store.now().timestamp(),
        )
        if not ok:
            raise ApiError("forbidden", "Re-Authentisierung fehlgeschlagen.")

    async def _json_body(request: Request) -> dict:
        try:
            body = await request.json()
        except ValueError as exc:
            raise ApiError("validation_failed", "Ungültiges JSON.") from exc
        if not isinstance(body, dict):
            raise ApiError("validation_failed", "Body muss ein JSON-Objekt sein.")
        return body

    async def _password(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        await _require_reauth(request, session, body)

        new_password = body.get("new_password")
        if not isinstance(new_password, str):
            raise ApiError("validation_failed", "new_password ist Pflichtfeld.")
        reasons = passwords_policy.check(new_password, space=session.space)
        if reasons:
            raise ApiError("validation_failed", "Passwort erfüllt die Richtlinie nicht.", detail={"reasons": reasons})

        users.set_password(session.space, new_password)
        # P5-Q: ALLE Token-Familien widerrufen, alle FREMDEN UI-Sessions beenden (die aktuelle
        # bleibt bestehen — sie wird gleich rotiert, nicht beendet).
        current_session_id = request.cookies.get(COOKIE_NAME)
        store.revoke_families_for_space(session.space, "password_changed")
        store.revoke_sessions_for_space(
            session.space, except_session_id=current_session_id, reason="password_changed"
        )

        # `rotate()` gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions`
        # speichert nur `csrf_hash`, genau wie in `pages.py :: render_logged_in_page()`
        # dokumentiert) — ein verworfener Rückgabewert hätte jede folgende
        # CSRF-geprüfte `/api/v1/account/*`-Anfrage bis zum nächsten Login mit `403 csrf_failed`
        # blockiert (Advisor-Fund vor dem Commit).
        response = JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})
        new_csrf = sessions.rotate(request, response, space=session.space)  # P5-E: Rotation bei Re-Auth
        response.body = response.render({"ok": True, "csrf_token": new_csrf})
        response.headers["content-length"] = str(len(response.body))
        return response

    async def _totp_start(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        await _require_reauth(request, session, body)

        secret = users.begin_totp_enrollment(session.space)
        uri = totp.provisioning_uri(secret, space=session.space, issuer=TOTP_ISSUER)
        return JSONResponse(
            {"secret": secret, "otpauth_uri": uri}, headers={"Cache-Control": "no-store"}
        )

    async def _totp_confirm(request: Request) -> Response:
        session = await _require_session(request, require_confirmed=False)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        code = body.get("code")
        if not isinstance(code, str):
            raise ApiError("validation_failed", "code ist Pflichtfeld.")

        ok = users.confirm_totp_enrollment(session.space, code, now=store.now().timestamp())
        if not ok:
            raise ApiError("validation_failed", "TOTP-Code ungültig.")
        return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

    async def _recovery_codes(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        await _require_reauth(request, session, body)

        codes = users.issue_recovery_codes(session.space)
        return JSONResponse({"codes": codes}, headers={"Cache-Control": "no-store"})

    async def _sessions_get(request: Request) -> Response:
        session = await _require_session(request)
        rows = store.list_sessions(session.space)
        return JSONResponse(
            [
                {
                    "created_at": _iso(row.created_at),
                    "last_seen_at": _iso(row.last_seen_at),
                    "revoked_at": _iso(row.revoked_at) if row.revoked_at else None,
                    "is_current": row.session_hash == session.session_hash,
                }
                for row in rows
            ],
            headers={"Cache-Control": "no-store"},
        )

    async def _sessions_delete(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        await _require_reauth(request, session, body)

        current_session_id = request.cookies.get(COOKIE_NAME)
        killed = store.revoke_sessions_for_space(
            session.space, except_session_id=current_session_id, reason="user_ended_other_sessions"
        )
        return JSONResponse({"revoked": killed}, headers={"Cache-Control": "no-store"})

    async def _connectors_get(request: Request) -> Response:
        session = await _require_session(request)
        families = [f for f in store.list_families(space=session.space) if f.revoked_at is None]
        result = []
        for family in families:
            client = store.get_client(family.client_id)
            result.append(
                {
                    "family_id": family.family_id,
                    "client_id": family.client_id,
                    "client_name": client.client_name if client is not None else None,
                    "created_at": _iso(family.created_at),
                }
            )
        return JSONResponse(result, headers={"Cache-Control": "no-store"})

    async def _connectors_delete(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        await _require_reauth(request, session, body)

        family_id = request.path_params["family_id"]
        # Nur eigene, aktive Familien — sonst 404 (nicht 403: ein 403 wäre ein Orakel darüber,
        # dass die ID existiert, Plan §3.3).
        owned = any(
            f.family_id == family_id and f.revoked_at is None
            for f in store.list_families(space=session.space)
        )
        if not owned:
            raise ApiError("not_found", "Connector-Verbindung nicht gefunden.")
        store.revoke_family(family_id, "user_revoked")
        return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

    def _catch(handler):
        """Ummantelt einen Handler mit dem gemeinsamen `ApiError`→JSON-Übersetzer — VOR dem
        `Route(...)`-Konstruktor angewendet, nicht danach: `Route.__init__` erfasst den
        übergebenen Endpoint sofort in `self.app` (`request_response(endpoint)`), ein späteres
        Überschreiben von `route.endpoint` hätte auf das tatsächlich bediente `self.app` keinen
        Effekt gehabt (kein Starlette-`exception_handler` auf App-Ebene: der würde auch `/ui/`
        und `/mcp` treffen)."""
        async def _inner(request: Request) -> Response:
            try:
                return await handler(request)
            except ApiError as exc:
                return _error_response(exc)
        return _inner

    return [
        Route("/api/v1/account/password", _catch(_password), methods=["POST"]),
        Route("/api/v1/account/totp/start", _catch(_totp_start), methods=["POST"]),
        Route("/api/v1/account/totp/confirm", _catch(_totp_confirm), methods=["POST"]),
        Route("/api/v1/account/recovery-codes", _catch(_recovery_codes), methods=["POST"]),
        Route("/api/v1/account/sessions", _catch(_sessions_get), methods=["GET"]),
        Route("/api/v1/account/sessions", _catch(_sessions_delete), methods=["DELETE"]),
        Route("/api/v1/account/connectors", _catch(_connectors_get), methods=["GET"]),
        Route("/api/v1/account/connectors/{family_id}", _catch(_connectors_delete), methods=["DELETE"]),
    ]
