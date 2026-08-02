"""Der Autorisierungsfluss (Plan §2.4), bewusst frei von jedem HTTP-Framework — `routes.py`
bleibt dünn ("parsen, `flows` aufrufen, antworten"), diese Datei ist deshalb die einzige Stelle,
an der der Fluss ohne einen echten HTTP-Request testbar ist. Rückgaben sind kleine, eingefrorene
Ergebnis-Typen statt Starlette-`Response`-Objekten — sonst würden `test_flows.py` und
`test_routes.py` de facto dasselbe prüfen.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from . import crypto, passwords, totp
from .clients import redirect_uri_allowed
from .config import AuthSettings
from .errors import OAuthError
from .ratelimit import LoginThrottle
from .store import AuthStore
from .userdir import UserDirectory, looks_like_recovery_code

SUPPORTED_SCOPES = frozenset({"space", "offline_access"})

_ERROR_DESCRIPTIONS: dict[str, str] = {
    "unsupported_response_type": "response_type muss 'code' sein.",
    "invalid_request": "code_challenge fehlt oder code_challenge_method ist nicht S256.",
    "invalid_scope": "angeforderter scope ist keine Teilmenge von space, offline_access.",
    "invalid_target": "resource stimmt nicht mit der erwarteten Ressource überein.",
    "access_denied": "Nutzer hat die Anfrage abgelehnt.",
}


# -- Ergebnistypen, die `routes.py` in eine HTTP-Antwort übersetzt --------------------


@dataclass(frozen=True)
class ErrorPage:
    """`client_id`/`redirect_uri` sind noch nicht (oder ein Login ist fehlgeschlagen) —
    niemals ein Redirect (Plan §2.4: "Erst ab hier ist die Rücksprungadresse vertrauenswürdig")."""

    message: str


@dataclass(frozen=True)
class RenderForm:
    request_id: str


@dataclass(frozen=True)
class RedirectError:
    redirect_uri: str
    error: str
    error_description: str
    state: str | None
    iss: str


@dataclass(frozen=True)
class RedirectSuccess:
    redirect_uri: str
    code: str
    state: str | None
    iss: str


AuthorizeResult = ErrorPage | RenderForm | RedirectError | RedirectSuccess


@dataclass(frozen=True)
class TokenSuccess:
    access_token: str
    refresh_token: str
    expires_in: int
    scope: str


# -- GET /oauth/authorize --------------------------------------------------------------


def start_authorize(
    *,
    store: AuthStore,
    settings: AuthSettings,
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str | None,
    code_challenge: str,
    code_challenge_method: str,
    scope: str | None,
    resource: str | None,
) -> AuthorizeResult:
    client = store.get_client(client_id)
    if client is None:
        return ErrorPage("Unbekannter Client.")
    # Byteweise Mitgliedschaft in der Registrierung UND die Origin-Allowlist (Plan §2.6: die
    # beiden einzigen Aufrufer von redirect_uri_allowed() sind /oauth/register und hier) —
    # eine später verschärfte Allowlist muss auch längst registrierte Redirects neu bewerten.
    if redirect_uri not in client.redirect_uris or not redirect_uri_allowed(redirect_uri, settings):
        return ErrorPage("Rücksprungadresse ist für diesen Client nicht registriert.")

    def _redirect_error(error: str) -> RedirectError:
        return RedirectError(
            redirect_uri=redirect_uri,
            error=error,
            error_description=_ERROR_DESCRIPTIONS[error],
            state=state,
            iss=settings.issuer,
        )

    if response_type != "code":
        return _redirect_error("unsupported_response_type")
    if not code_challenge or code_challenge_method != "S256":
        return _redirect_error("invalid_request")
    requested_scopes = set(scope.split()) if scope else {"space"}
    if not requested_scopes <= SUPPORTED_SCOPES:
        return _redirect_error("invalid_scope")
    if resource and resource != settings.resource:
        return _redirect_error("invalid_target")

    request_id = store.create_auth_request(
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
        scope=scope or "space",
        resource=resource,
        ttl_s=settings.request_ttl_s,
    )
    return RenderForm(request_id=request_id)


# -- POST /oauth/authorize (Consent-Formular) -------------------------------------------


def submit_consent(
    *,
    store: AuthStore,
    settings: AuthSettings,
    users: UserDirectory,
    throttle: LoginThrottle,
    now_fn: Callable[[], datetime],
    request_id: str,
    space: str,
    password: str,
    totp_code: str,
    action: str,
) -> AuthorizeResult:
    # Einmalig: markiert sofort als konsumiert, unabhängig vom Ausgang des restlichen Flusses
    # (Plan §2.4 POST-Schritt 1, "ein Formular, ein Versuch") — `consume_auth_request()`
    # erledigt das bereits in `store.py` (Step 3).
    pending = store.consume_auth_request(request_id)
    if pending is None:
        return ErrorPage("Anfrage ungültig oder abgelaufen.")

    if action == "deny":
        return RedirectError(
            redirect_uri=pending.redirect_uri,
            error="access_denied",
            error_description=_ERROR_DESCRIPTIONS["access_denied"],
            state=pending.state,
            iss=settings.issuer,
        )

    remaining = throttle.check(space)
    if remaining is not None:
        return ErrorPage(f"Konto gesperrt. Nächster Versuch in {remaining} Sekunden möglich.")

    # Enumerationsschutz (Plan §2.4 Schritt 4): ein nicht existierender Space durchläuft
    # trotzdem einen vollen Argon2id-Verify gegen einen festen Dummy-Hash. TOTP wird für einen
    # nicht existierenden Space bewusst NICHT geprüft — Argon2id (t=8, ~55ms) dominiert die
    # TOTP-HMAC-Prüfung um Größenordnungen, das Weglassen ist deshalb kein Timing-Orakel
    # (Advisor-Review dieser Session). Beide Ergebnisse werden trotzdem erst am Ende verknüpft,
    # kein früher `return`.
    # S6 (Sicherheits-Review 2026-07-29): jetzt strukturell geschlossen — `UserDirectory.get()`
    # gibt `UserRecord | None` zurück (nie ein Datensatz mit fehlenden Feldern; `store.get_user()`
    # liest über feste Spalten, keine dict-Indizierung mehr). Die in Step 1 übergangsweise
    # eingesetzte `record.get(...)`-Fix-Skizze ist damit gegenstandslos und entfernt (P5 Step 2).
    record = users.get(space)
    stored_hash = record.password_hash if record is not None else passwords.DUMMY_HASH
    password_ok = passwords.verify_password(stored_hash, password)

    # Enumerationsschutz gilt unverändert (siehe Absatz oben): Argon2id läuft in JEDEM Fall,
    # der TOTP-/Recovery-Zweig nur, wenn der Space existiert.
    totp_ok = False
    accepted_counter: int | None = None
    if record is not None:
        # P5-Ergänzung: ein Recovery-Code funktioniert auch im OAuth-Consent-Formular, sonst
        # wäre ein Nutzer ohne Authenticator zwar in der UI, aber nicht am Connector
        # handlungsfähig (Plan §2.5). Die Formerkennung lebt einzig in `looks_like_recovery_code()`
        # — kein zweiter, hier abgeleiteter Literal-Check.
        if looks_like_recovery_code(totp_code):
            # `consume_recovery_code()` mutiert (stempelt `used_at`) — nur bei richtigem
            # Passwort aufrufen, sonst verbrennt ein Tippfehler im Passwortfeld einen von zehn
            # Codes ohne jede Rückmeldung. Spiegelt den `accepted_counter`-Guard unten (gleiche
            # Lehre, TOTP-Zweig), Advisor-Fund vor diesem Commit.
            totp_ok = password_ok and users.consume_recovery_code(space, totp_code)
        else:
            accepted_counter = totp.verify(
                record.totp_secret or "",
                totp_code,
                now=now_fn().timestamp(),
                last_counter=store.get_totp_counter(space),
                algo=record.totp_alg,
            )
            totp_ok = accepted_counter is not None

    if not (password_ok and totp_ok):
        throttle.register_failure(space)
        return ErrorPage("Anmeldung fehlgeschlagen.")

    # Zähler erst nach einem VOLLSTÄNDIGEN Erfolg hochsetzen (Passwort UND TOTP) — ein
    # frühzeitiges Hochsetzen bei richtigem TOTP aber falschem Passwort würde das aktuelle
    # Zeitfenster für den echten Nutzer verbrennen, beobachtbar von jedem, der den Code sieht.
    # Ein Recovery-Code hat keinen Zähler (`accepted_counter` bleibt `None`) — `set_totp_counter`
    # darf dann nicht laufen, sonst überschreibt ein Recovery-Login stillschweigend den
    # TOTP-Replay-Zähler mit `None`.
    throttle.reset(space)
    if accepted_counter is not None:
        store.set_totp_counter(space, accepted_counter)

    family_id = store.create_family(
        space=space,
        client_id=pending.client_id,
        scope=pending.scope,
        resource=pending.resource or settings.resource,
    )
    code = store.issue_code(
        family_id=family_id,
        client_id=pending.client_id,
        redirect_uri=pending.redirect_uri,
        code_challenge=pending.code_challenge,
        ttl_s=settings.code_ttl_s,
    )
    return RedirectSuccess(
        redirect_uri=pending.redirect_uri, code=code, state=pending.state, iss=settings.issuer,
    )


# -- POST /oauth/token --------------------------------------------------------------------


def issue_token(
    *,
    store: AuthStore,
    settings: AuthSettings,
    grant_type: str | None,
    code: str | None = None,
    redirect_uri: str | None = None,
    client_id: str | None = None,
    code_verifier: str | None = None,
    refresh_token: str | None = None,
) -> TokenSuccess:
    """Wirft `OAuthError` bei jeder Ablehnung. Alle Fehler, die eine `code`/`refresh_token`
    betreffen (unbekannt, abgelaufen, verbraucht/rotiert, Client- oder Redirect-Mismatch,
    falscher PKCE-Verifier), sammeln sich auf `invalid_grant` — nur ein fehlender/unbekannter
    `grant_type` oder ein fehlendes Pflichtfeld behalten ihren eigenen RFC-6749-Code (Plan §2.4:
    "Alle Fehlerantworten ... niemals eine Beschreibung, die zwischen ... unterscheidet")."""
    if grant_type == "authorization_code":
        if not code or not redirect_uri or not client_id or not code_verifier:
            raise OAuthError("invalid_request")
        auth_code, _was_replay = store.consume_code(code)
        if auth_code is None:
            raise OAuthError("invalid_grant")
        if auth_code.client_id != client_id or auth_code.redirect_uri != redirect_uri:
            raise OAuthError("invalid_grant")
        if not crypto.verify_pkce(code_verifier, auth_code.code_challenge):
            raise OAuthError("invalid_grant")
        access_token, new_refresh = store.issue_token_pair(
            auth_code.family_id, access_ttl_s=settings.access_ttl_s, refresh_ttl_s=settings.refresh_ttl_s,
        )
    elif grant_type == "refresh_token":
        if not refresh_token or not client_id:
            raise OAuthError("invalid_request")
        pair = store.rotate_refresh(
            refresh_token, client_id=client_id,
            access_ttl_s=settings.access_ttl_s, refresh_ttl_s=settings.refresh_ttl_s,
        )
        if pair is None:
            raise OAuthError("invalid_grant")
        access_token, new_refresh = pair
    else:
        raise OAuthError("unsupported_grant_type")

    record = store.lookup_access_token(access_token)
    return TokenSuccess(
        access_token=access_token,
        refresh_token=new_refresh,
        expires_in=settings.access_ttl_s,
        scope=record.scope,
    )
