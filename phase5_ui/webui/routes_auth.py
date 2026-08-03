"""UI-Auth-Routen: `/ui/login`, `/ui/logout` (Plan §2.7, §5 Step 3). Dünn wie
`authserver/routes.py`: parsen, `UserDirectory`/`AuthStore`/`SessionManager` aufrufen,
antworten. Security-Header trägt jeder Handler selbst (gleicher Grund wie dort — kein
app-weites Middleware, das auch `/mcp` träfe).

`/ui/invite/{token}` (Einladung/Enrollment, Plan §2.8) ist NICHT Teil dieses Steps — Plan §5
Step 3 zeigt nur auf §2.7/§3.4, die Einladungslogik braucht `webui/passwords_policy.py`
(Step 4, Passwortpolitik-Prüfung ist Teil des Einladungs-Flows) und existiert hier noch nicht.

Der Login-Zweig dupliziert bewusst die enumerationssichere Prüfung aus
`authserver/flows.py :: submit_consent()` (Argon2id unconditional, TOTP/Recovery nur wenn der
Space existiert, dieselbe `LoginThrottle`) statt sie zu teilen — P5-G hält UI-Sitzung und
OAuth-Consent architektonisch getrennt, eine gemeinsame Funktion wäre eine Kopplung, die der
Plan an dieser Stelle nicht vorsieht.
"""
from __future__ import annotations

from authserver import passwords, totp
from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory, looks_like_recovery_code
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Route

from . import pages
from .config import COOKIE_NAME, UiSettings
from .errors import CsrfError
from .security import require_csrf, ui_security_headers
from .sessions import SessionManager


def ui_auth_routes(
    settings: UiSettings,
    store: AuthStore,
    users: UserDirectory,
    sessions: SessionManager,
) -> list[Route]:
    throttle = LoginThrottle(store, now_fn=store.now)

    async def _login_get(request: Request) -> Response:
        return HTMLResponse(pages.render_login_page(), headers=ui_security_headers(settings))

    async def _login_post(request: Request) -> Response:
        headers = ui_security_headers(settings)
        form = await request.form()
        space = str(form.get("space", ""))
        password = str(form.get("password", ""))
        code = str(form.get("totp", ""))

        remaining = throttle.check(space)
        if remaining is not None:
            return HTMLResponse(
                pages.render_login_page(
                    error=f"Konto gesperrt. Nächster Versuch in {remaining} Sekunden möglich."
                ),
                status_code=429,
                headers=headers,
            )

        # Enumerationsschutz, identisch zu `flows.py :: submit_consent()`: Argon2id läuft in
        # JEDEM Fall gegen einen festen Dummy-Hash, TOTP/Recovery nur, wenn der Space existiert.
        record = users.get(space)
        stored_hash = record.password_hash if record is not None else passwords.DUMMY_HASH
        password_ok = passwords.verify_password(stored_hash, password)

        code_ok = False
        accepted_counter: int | None = None
        if record is not None:
            if looks_like_recovery_code(code):
                # Nur bei richtigem Passwort verbrauchen (`consume_recovery_code()` mutiert) —
                # dieselbe Lehre wie im OAuth-Consent-Zweig (Advisor-Fund, P5 Step 2).
                code_ok = password_ok and users.consume_recovery_code(space, code)
            else:
                accepted_counter = totp.verify(
                    record.totp_secret or "",
                    code,
                    now=store.now().timestamp(),
                    last_counter=store.get_totp_counter(space),
                    algo=record.totp_alg,
                )
                code_ok = accepted_counter is not None

        if not (password_ok and code_ok):
            throttle.register_failure(space)
            return HTMLResponse(
                pages.render_login_page(error="Anmeldung fehlgeschlagen."),
                status_code=401,
                headers=headers,
            )

        throttle.reset(space)
        # Zähler erst nach VOLLSTÄNDIGEM Erfolg hochsetzen (dieselbe Lehre wie
        # `flows.py :: submit_consent()`, Advisor-Fund dieser Session: die erste Fassung setzte
        # ihn schon innerhalb des TOTP-Zweigs, VOR dem Passwort-Gate — ein richtiger TOTP-Code
        # mit falschem Passwort hätte das aktuelle Zeitfenster für den echten Nutzer verbrannt).
        if accepted_counter is not None:
            store.set_totp_counter(space, accepted_counter)
        # KEIN bloßer Redirect: `sessions.rotate()` gibt den CSRF-Token nur dieses eine Mal als
        # Klartext zurück (`ui_sessions` speichert nur den Hash) — ein Redirect ohne Body würde
        # ihn verwerfen und jede nachfolgende CSRF-geprüfte Anfrage (z. B. Logout) könnte nie
        # einen gültigen Wert vorlegen. Übergangsseite bis Step 6 die echte App-Shell baut.
        response = HTMLResponse("", headers=headers)
        csrf_token = sessions.rotate(request, response, space=space)
        response.body = pages.render_logged_in_page(csrf_token=csrf_token).encode("utf-8")
        response.headers["content-length"] = str(len(response.body))
        return response

    async def _logout(request: Request) -> Response:
        headers = ui_security_headers(settings)
        session = sessions.load(request)
        response = RedirectResponse("/ui/login", status_code=303, headers=headers)
        if session is None:
            # Kein/kein gültiges Cookie: Logout ist trotzdem "erfolgreich" (Ziel bereits
            # erreicht) — kein Fehler für einen Zustand, der schon der gewünschte ist.
            sessions.clear(response, None, reason="logout")
            return response

        form = await request.form()
        try:
            require_csrf(request, session, settings=settings, form_token=form.get("csrf"))
        except CsrfError as exc:
            return HTMLResponse(
                pages.render_error_page(exc.message), status_code=exc.status_code, headers=headers
            )

        session_id = request.cookies.get(COOKIE_NAME)
        sessions.clear(response, session_id, reason="logout")
        return response

    return [
        Route("/ui/login", _login_get, methods=["GET"]),
        Route("/ui/login", _login_post, methods=["POST"]),
        Route("/ui/logout", _logout, methods=["POST"]),
    ]
