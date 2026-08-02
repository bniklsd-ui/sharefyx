"""Starlette-Routen des Authorization Servers, dünn: parsen, Modullogik aufrufen, antworten
(Plan §5 Step 4/5 — Step 4 baut Metadaten + Registrierung, Step 5 ergänzt `/oauth/authorize`
und `/oauth/token`). Kein SQL, keine Zustandslogik hier — beides lebt in `store.py`/`clients.py`/
`flows.py`.

`oauth_routes()` ist der Anker für Step 6 (`mcpserver/app.py`, Plan §3.3): die zurückgegebene
Routenliste wird der Wurzel-App **vorangestellt**, kein eigenes `Mount`/Sub-App. Deshalb tragen
die Handler ihre Security-Header selbst statt über eine Starlette-`Middleware` — eine
app-weite Middleware in der Wurzel-App träfe auch `/health` und `/mcp`, und ein zweites,
pfadgebundenes Mounten sieht Plan §3.3 nicht vor ("vorangestellt", nicht `Mount`).
"""
from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from . import flows, templates
from .clients import check_register_rate_limit, register_client
from .config import AuthSettings
from .errors import DCRError, OAuthError
from .metadata import authorization_server_metadata, protected_resource_metadata
from .ratelimit import LoginThrottle
from .store import AuthStore
from .userdir import UserDirectory


def _security_headers(settings: AuthSettings) -> dict[str, str]:
    """Plan §2.6 — volles Set für HTML-Antworten und beide Metadatendokumente.

    **Live-Fund 2026-07-30:** `form-action` muss die erlaubten Redirect-Origins explizit nennen,
    nicht nur `'self'`. Chromium (bestätigt: Microsoft Edge 150, Fabians Verbindungsversuch)
    prüft `form-action` nicht nur gegen das unmittelbare `action`-Ziel des Formulars, sondern
    auch gegen das Redirect-Ziel, wenn die Antwort auf den `POST` selbst ein Redirect ist (genau
    der Fall hier: `POST /oauth/authorize` antwortet bei Erfolg mit `302` nach
    `https://claude.ai/...`). Ohne `https://claude.ai`/`https://claude.com` in `form-action`
    blockiert der Browser diesen Redirect **lautlos** — kein Fehler auf der Seite, nur eine
    Konsolen-Meldung, die kein Nutzer je sieht. Der Server selbst liefert dabei einen korrekten
    `302` mit gültigem Code (siehe `token_families` — die Anmeldung war jedes Mal erfolgreich);
    der Bruch passiert ausschließlich im Browser, nach der Antwort. Ein zweiter Klick auf das
    (bereits erfolgreich abgeschickte, aber nie weitergeleitete) Formular trifft dann auf
    `consume_auth_request()`s Einmal-Regel und zeigt "Anfrage ungueltig oder abgelaufen" — beide
    Symptome aus demselben einen Fund erklärt.

    `settings.csp_form_action` statt der rohen Redirect-Origin-Liste direkt: der Wert wird in
    `config.py` gebaut (siehe dortiger Docstring), damit dieses Modul die Liste nirgends selbst
    anfasst (`test_redirect_uri_allowed_is_the_only_matching_path`, Plan §2.6 [SEAM])."""
    headers = {
        "Content-Security-Policy": (
            f"default-src 'none'; style-src 'unsafe-inline'; form-action {settings.csp_form_action}; "
            "frame-ancestors 'none'; base-uri 'none'"
        ),
        "Referrer-Policy": "no-referrer",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Cache-Control": "no-store",
    }
    if settings.hsts:
        headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return headers


def _token_headers(settings: AuthSettings) -> dict[str, str]:
    """Additiv (Step 5): `Pragma: no-cache` steht in Plan §2.4 nur beim Token-Endpunkt, nicht in
    der allgemeinen Header-Tabelle §2.6 — deshalb kein Teil von `_security_headers()`."""
    return {**_security_headers(settings), "Pragma": "no-cache"}


def _dcr_error_response(exc: DCRError) -> JSONResponse:
    return JSONResponse(
        {"error": exc.code}, status_code=400, headers={"Cache-Control": "no-store"}
    )


def oauth_routes(
    auth_settings: AuthSettings,
    auth_store: AuthStore,
    users: UserDirectory,
) -> list[Route]:
    # Dieselbe Uhr wie `auth_store` (Advisor-Fund: "ein Clock, nicht zwei") — `AuthStore.now()`
    # exponiert genau dafür die injizierte `now_fn` des Stores, statt eine zweite anzulegen.
    throttle = LoginThrottle(auth_store, now_fn=auth_store.now)

    async def _prm(request: Request) -> JSONResponse:
        return JSONResponse(
            protected_resource_metadata(auth_settings), headers=_security_headers(auth_settings)
        )

    async def _as_metadata(request: Request) -> JSONResponse:
        return JSONResponse(
            authorization_server_metadata(auth_settings), headers=_security_headers(auth_settings)
        )

    async def _register(request: Request) -> JSONResponse:
        content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
        if content_type != "application/json":
            return _dcr_error_response(DCRError("invalid_client_metadata"))

        # Türstopper vor der eigentlichen Arbeit (Plan §2.7): zählt jeden Registrierungsversuch
        # mit korrektem Content-Type gegen das globale Stundenkontingent, unabhängig vom Ausgang.
        if not check_register_rate_limit(auth_store):
            return JSONResponse(
                {"error": "rate_limited"}, status_code=429, headers={"Cache-Control": "no-store"}
            )

        try:
            body = await request.json()
        except ValueError:
            return _dcr_error_response(DCRError("invalid_client_metadata"))
        if not isinstance(body, dict):
            return _dcr_error_response(DCRError("invalid_client_metadata"))

        try:
            client = register_client(
                store=auth_store,
                settings=auth_settings,
                client_name=body.get("client_name"),
                application_type=body.get("application_type"),
                redirect_uris=body.get("redirect_uris"),
            )
        except DCRError as exc:
            return _dcr_error_response(exc)

        return JSONResponse(
            {
                "client_id": client.client_id,
                "client_name": client.client_name,
                "application_type": client.application_type,
                "redirect_uris": list(client.redirect_uris),
                "token_endpoint_auth_method": "none",
                "client_id_issued_at": int(client.created_at.timestamp()),
            },
            status_code=201,
            headers={"Cache-Control": "no-store"},
        )

    def _authorize_response(result: flows.AuthorizeResult) -> Response:
        headers = _security_headers(auth_settings)
        if isinstance(result, flows.ErrorPage):
            return HTMLResponse(
                templates.render_error_page(result.message), status_code=400, headers=headers
            )
        if isinstance(result, flows.RenderForm):
            return HTMLResponse(templates.render_login_form(result.request_id), headers=headers)

        params: dict[str, str] = {"state": result.state, "iss": result.iss}
        if isinstance(result, flows.RedirectSuccess):
            params["code"] = result.code
        else:
            params["error"] = result.error
            params["error_description"] = result.error_description

        # S5 (Sicherheits-Review 2026-07-29): `f"{uri}?{query}"` hängte bedingungslos ein `?` an
        # — ein registrierter Redirect mit eigenem Query-String (`https://x/cb?a=b`) bekam damit
        # ein zweites `?`, das Teil des Werts von `a` wurde. `urlsplit`/`parse_qsl`/`urlunsplit`
        # mischen stattdessen in die vorhandene Query hinein.
        split = urlsplit(result.redirect_uri)
        existing = parse_qsl(split.query, keep_blank_values=True)
        merged = existing + [(k, v) for k, v in params.items() if v is not None]
        location = urlunsplit(split._replace(query=urlencode(merged)))
        return RedirectResponse(location, status_code=302, headers=headers)

    async def _authorize_get(request: Request) -> Response:
        q = request.query_params
        result = flows.start_authorize(
            store=auth_store,
            settings=auth_settings,
            client_id=q.get("client_id", ""),
            redirect_uri=q.get("redirect_uri", ""),
            response_type=q.get("response_type", ""),
            state=q.get("state"),
            code_challenge=q.get("code_challenge", ""),
            code_challenge_method=q.get("code_challenge_method", ""),
            scope=q.get("scope"),
            resource=q.get("resource"),
        )
        return _authorize_response(result)

    async def _authorize_post(request: Request) -> Response:
        form = await request.form()
        result = flows.submit_consent(
            store=auth_store,
            settings=auth_settings,
            users=users,
            throttle=throttle,
            now_fn=auth_store.now,
            request_id=form.get("request_id", ""),
            space=form.get("space", ""),
            password=form.get("password", ""),
            totp_code=form.get("totp", ""),
            action=form.get("action", ""),
        )
        return _authorize_response(result)

    async def _token(request: Request) -> Response:
        form = await request.form()
        try:
            result = flows.issue_token(
                store=auth_store,
                settings=auth_settings,
                grant_type=form.get("grant_type"),
                code=form.get("code"),
                redirect_uri=form.get("redirect_uri"),
                client_id=form.get("client_id"),
                code_verifier=form.get("code_verifier"),
                refresh_token=form.get("refresh_token"),
            )
        except OAuthError as exc:
            return JSONResponse(
                {"error": exc.code}, status_code=400, headers=_token_headers(auth_settings)
            )
        return JSONResponse(
            {
                "access_token": result.access_token,
                "token_type": "Bearer",
                "expires_in": result.expires_in,
                "refresh_token": result.refresh_token,
                "scope": result.scope,
            },
            headers=_token_headers(auth_settings),
        )

    return [
        Route("/.well-known/oauth-protected-resource", _prm, methods=["GET"]),
        Route("/.well-known/oauth-protected-resource/mcp", _prm, methods=["GET"]),
        Route("/.well-known/oauth-authorization-server", _as_metadata, methods=["GET"]),
        Route("/oauth/register", _register, methods=["POST"]),
        Route("/oauth/authorize", _authorize_get, methods=["GET"]),
        Route("/oauth/authorize", _authorize_post, methods=["POST"]),
        Route("/oauth/token", _token, methods=["POST"]),
    ]
