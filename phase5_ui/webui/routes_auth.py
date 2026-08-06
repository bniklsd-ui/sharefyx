"""UI-Auth-Routen: `/ui/login`, `/ui/logout` (Plan §2.7, §5 Step 3), `/ui/invite/{token}`,
`/ui/enroll/confirm` (Plan §2.8, §5 Step 4). Dünn wie `authserver/routes.py`: parsen,
`UserDirectory`/`AuthStore`/`SessionManager` aufrufen, antworten. Security-Header trägt jeder
Handler selbst (gleicher Grund wie dort — kein app-weites Middleware, das auch `/mcp` träfe).

`/ui/enroll/confirm` (statt `/api/v1/account/totp/confirm`, das dieselbe Operation JSON-only
anbietet, Plan §3.3) existiert, weil `pages.py`s Formulare bewusst ohne JavaScript auskommen
(dortiger Moduldocstring) — ein `<form>` ohne JS sendet immer `application/x-www-form-urlencoded`,
nie JSON, und `/api` nimmt laut §3.1 kein Formular-Encoding an. Beide Wege rufen dieselbe
`UserDirectory.confirm_totp_enrollment()` auf, keine doppelte Geschäftslogik.

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

from . import pages, passwords_policy
from .config import COOKIE_NAME, UiSettings
from .errors import CsrfError
from .security import require_csrf, ui_security_headers
from .sessions import SessionManager

# Dieselbe Konstante wie `webui/account.py` — ein Authenticator zeigt diesen Namen als
# Konto-Herkunft an. Absichtlich hier erneut definiert statt importiert (ein einzelner
# projektweiter String ist kein neuer Modul-Kopplungspunkt wert, dieselbe Abwägung wie
# `authserver/config.py :: KEYRING_SERVICE`).
TOTP_ISSUER = "sharefyx"


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

        # `record.status == "disabled"` (`authctl.py disable-user`) muss den Login exakt wie
        # ein falsches Passwort ablehnen — derselbe Enumerationsschutz wie oben: kein eigener
        # Fehlercode, keine Verzweigung vor `throttle.register_failure()`, sonst wäre ein
        # deaktivierter, aber existierender Space von außen unterscheidbar (Advisor-Fund,
        # vor diesem Commit: `disable-user` widerruft bisher nur Sitzungen/Familien, der
        # betroffene Space konnte sich mit unverändertem Passwort/TOTP sofort neu einloggen).
        account_active = record is not None and record.status == "active"
        if not (password_ok and code_ok and account_active):
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

    async def _invite_get(request: Request) -> Response:
        headers = ui_security_headers(settings)
        token = request.path_params["token"]
        if store.peek_invite(token) is None:
            return HTMLResponse(
                pages.render_error_page("Einladung ungültig oder abgelaufen."),
                status_code=404, headers=headers,
            )
        return HTMLResponse(pages.render_invite_page(token=token), headers=headers)

    async def _invite_post(request: Request) -> Response:
        headers = ui_security_headers(settings)
        token = request.path_params["token"]
        form = await request.form()
        new_password = str(form.get("password", ""))

        # Passwortpolitik VOR dem Verbrauch prüfen (`consume_invite()` ist einmalig) — sonst
        # würde ein Nutzer, der beim ersten Versuch ein zu schwaches Passwort eintippt, seine
        # einzige Einladung verlieren, ohne je ein Konto zu bekommen.
        peeked = store.peek_invite(token)
        if peeked is None:
            return HTMLResponse(
                pages.render_error_page("Einladung ungültig oder abgelaufen."),
                status_code=404, headers=headers,
            )
        reasons = passwords_policy.check(new_password, space=peeked.space)
        if reasons:
            return HTMLResponse(
                pages.render_invite_page(token=token, error=" ".join(reasons)),
                status_code=422, headers=headers,
            )

        invite = store.consume_invite(token)
        if invite is None:
            # Race: zwischen den beiden Store-Aufrufen von einem anderen Request verbraucht.
            return HTMLResponse(
                pages.render_error_page("Einladung ungültig oder abgelaufen."),
                status_code=404, headers=headers,
            )

        # `users.set_password()`/`begin_totp_enrollment()` setzen beide nur eine BESTEHENDE
        # `users`-Zeile per `UPDATE` (`store.py :: set_password_hash()`/`set_totp()`) — für einen
        # brandneuen Space aus einer Einladung existiert noch keine. `store.upsert_user()` legt
        # sie an (deckt zugleich `purpose="reset"` ab: eine bestehende Zeile wird dabei bewusst
        # vollständig überschrieben, nicht nur das Passwort — ein Reset soll auch einen alten
        # TOTP-Seed nicht überleben lassen).
        store.upsert_user(
            invite.space, password_hash=passwords.hash_password(new_password),
            totp_secret_enc=None, totp_alg="SHA1", totp_confirmed_at=None, status="active",
        )

        # **Befund S10, live gefunden am 2026-08-06.** Bis hierher endete der Reset mit dem
        # `upsert_user()` oben: Passwort-Hash und TOTP-Seed wurden ersetzt, **Token-Familien und
        # UI-Sitzungen aber nicht angetastet.** Belegt an einem echten Konto — nach einem Reset
        # standen dort neun Token-Familien vom 30.07. weiterhin auf „aktiv", neben der frisch
        # angelegten.
        #
        # Das ist genau verkehrt herum: der *Passwortwechsel* (`account.py :: _password()`, P5-Q)
        # widerruft seit Step 4 alles — und der **Reset**, die stärkere Operation, die man bei
        # Verdacht auf Kompromittierung oder verlorenem Zugang fährt, widerrief nichts. Wer ein
        # altes Refresh-Token hielt, behielt vollen Zugriff auf den Space, obwohl Passwort UND
        # TOTP ersetzt waren. Der Kommentar oben nennt die Absicht ausdrücklich („ein Reset soll
        # auch einen alten TOTP-Seed nicht überleben lassen") — die Absicht war richtig, sie war
        # nur nicht zu Ende geführt.
        #
        # Kein `except_session_id` wie beim Passwortwechsel: dort läuft die Sitzung des Handelnden
        # weiter, hier gibt es noch gar keine — die neue wird erst unten mit `sessions.issue()`
        # ausgestellt. Ein Reset darf schlicht nichts Altes überleben lassen.
        store.revoke_families_for_space(invite.space, "invite_redeemed")
        store.revoke_sessions_for_space(
            invite.space, except_session_id=None, reason="invite_redeemed"
        )

        secret = users.begin_totp_enrollment(invite.space)
        otpauth_uri = totp.provisioning_uri(secret, space=invite.space, issuer=TOTP_ISSUER)

        response = HTMLResponse("", headers=headers)
        csrf_token = sessions.issue(response, space=invite.space)
        response.body = pages.render_enrollment_page(
            secret=secret, otpauth_uri=otpauth_uri, csrf_token=csrf_token,
        ).encode("utf-8")
        response.headers["content-length"] = str(len(response.body))
        return response

    async def _enroll_confirm(request: Request) -> Response:
        def _enrollment_retry(*, space: str, csrf_token: str, error: str, status_code: int) -> Response:
            # Gemeinsam für „falscher Code" UND „CSRF-Fehlschlag" (Advisor-Fund-artiger
            # Live-Fund des Nikingers, 2026-08-03): eine fehlgeschlagene `require_csrf()`-Prüfung
            # landete bisher auf `pages.render_error_page()` — einer Sackgasse ohne Formular,
            # ohne Zurück. `begin_totp_enrollment()` erneut aufzurufen würde den bereits
            # gescannten Secret entwerten, deshalb wird hier derselbe Secret nur erneut gelesen,
            # nicht neu gemintet.
            record = users.get(space)
            otpauth_uri = totp.provisioning_uri(
                record.totp_secret or "" if record else "", space=space, issuer=TOTP_ISSUER,
            )
            return HTMLResponse(
                pages.render_enrollment_page(
                    secret=(record.totp_secret or "") if record else "", otpauth_uri=otpauth_uri,
                    csrf_token=csrf_token, error=error,
                ),
                status_code=status_code, headers=headers,
            )

        headers = ui_security_headers(settings)
        session = sessions.load(request)
        if session is None:
            return HTMLResponse(
                pages.render_error_page("Sitzung abgelaufen. Bitte Einladung erneut öffnen."),
                status_code=401, headers=headers,
            )

        form = await request.form()
        csrf_value = form.get("csrf")
        try:
            require_csrf(request, session, settings=settings, form_token=csrf_value)
        except CsrfError as exc:
            # Die Sitzung bleibt gültig (kein Widerruf bei einem CSRF-Fehlschlag) — derselbe
            # `csrf_token`, den `_invite_post`/der vorige Versuch bereits ausgegeben hat, ist
            # weiterhin der einzig gültige Wert gegen `session.csrf_hash` (der Vergleich selbst
            # wurde ja nie erreicht, die Origin-Prüfung schlug vorher fehl) — einfach erneut
            # einbetten, kein neuer Token nötig.
            return _enrollment_retry(
                space=session.space, csrf_token=str(csrf_value or ""), error=exc.message,
                status_code=exc.status_code,
            )

        code = str(form.get("code", ""))
        ok = users.confirm_totp_enrollment(session.space, code, now=store.now().timestamp())
        if not ok:
            return _enrollment_retry(
                space=session.space, csrf_token=str(csrf_value),
                error="Code ungültig, bitte erneut versuchen.", status_code=422,
            )

        codes = users.issue_recovery_codes(session.space)
        return HTMLResponse(
            pages.render_recovery_codes_page(codes=codes, csrf_token=str(csrf_value)),
            headers=headers,
        )

    return [
        Route("/ui/login", _login_get, methods=["GET"]),
        Route("/ui/login", _login_post, methods=["POST"]),
        Route("/ui/logout", _logout, methods=["POST"]),
        Route("/ui/invite/{token}", _invite_get, methods=["GET"]),
        Route("/ui/invite/{token}", _invite_post, methods=["POST"]),
        Route("/ui/enroll/confirm", _enroll_confirm, methods=["POST"]),
    ]
