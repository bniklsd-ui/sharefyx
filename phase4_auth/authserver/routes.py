"""Starlette-Routen des Authorization Servers, dünn: parsen, Modullogik aufrufen, antworten
(Plan §5 Step 4/5 — Step 4 baut Metadaten + Registrierung, Step 5 ergänzt `/oauth/authorize`
und `/oauth/token`). Kein SQL, keine Zustandslogik hier — beides lebt in `store.py`/`clients.py`.

`oauth_routes()` ist der Anker für Step 6 (`mcpserver/app.py`, Plan §3.3): die zurückgegebene
Routenliste wird der Wurzel-App **vorangestellt**, kein eigenes `Mount`/Sub-App. Deshalb tragen
die Handler ihre Security-Header selbst statt über eine Starlette-`Middleware` — eine
app-weite Middleware in der Wurzel-App träfe auch `/health` und `/mcp`, und ein zweites,
pfadgebundenes Mounten sieht Plan §3.3 nicht vor ("vorangestellt", nicht `Mount`).
"""
from __future__ import annotations

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .clients import check_register_rate_limit, register_client
from .config import AuthSettings
from .errors import DCRError
from .metadata import authorization_server_metadata, protected_resource_metadata
from .store import AuthStore


def _security_headers(settings: AuthSettings) -> dict[str, str]:
    """Plan §2.6 — volles Set für HTML-Antworten und beide Metadatendokumente."""
    headers = {
        "Content-Security-Policy": (
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; "
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


def _dcr_error_response(exc: DCRError) -> JSONResponse:
    return JSONResponse(
        {"error": exc.code}, status_code=400, headers={"Cache-Control": "no-store"}
    )


def oauth_routes(auth_settings: AuthSettings, auth_store: AuthStore) -> list[Route]:
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

    return [
        Route("/.well-known/oauth-protected-resource", _prm, methods=["GET"]),
        Route("/.well-known/oauth-protected-resource/mcp", _prm, methods=["GET"]),
        Route("/.well-known/oauth-authorization-server", _as_metadata, methods=["GET"]),
        Route("/oauth/register", _register, methods=["POST"]),
    ]
