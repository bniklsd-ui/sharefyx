"""Dynamic Client Registration (RFC 7591) und die Redirect-Origin-Allowlist (Plan §2.6).
`redirect_uri_allowed` ist die **einzige** Stelle im Paket, an der eine Redirect-URI gegen eine
erlaubte Origin geprüft wird — belegt durch `test_redirect_uri_allowed_is_the_only_matching_path`
(Grep über `authserver/`, nicht Verhalten).
"""
from __future__ import annotations

from urllib.parse import urlsplit

from .config import AuthSettings
from .errors import DCRError
from .models import Client
from .store import AuthStore

MAX_REGISTRATIONS_PER_WINDOW = 20  # Plan §2.7: 20 pro Stunde insgesamt, grober Türstopper


def redirect_uri_allowed(uri: str, settings: AuthSettings) -> bool:
    """Die EINZIGE Stelle, an der über Rücksprungadressen entschieden wird.

    P4-Policy: exakter Origin-Vergleich gegen `settings.allowed_redirect_origins`,
    ausschließlich `https`.

    [SEAM] Native Clients (Claude Code, CLI-Werkzeuge) brauchen Loopback-Redirects nach
    RFC 8252 §7.3: `http://127.0.0.1:<wechselnder Port>/callback` bzw.
    `http://localhost/callback`, Vergleich mit ignoriertem Port. Das ist eine zweite
    Vergleichsregel, kein Sonderfall dieser hier — und sie hängt an CIMD, nicht an DCR (Plan
    §2.6, §8). Zurückgestellt (2026-07-28, Nikinger-Entscheidung nach der V14-Recherche dieser
    Session — aktuelle Anthropic-Doku verlangt das inzwischen für Claude Code, Details:
    Phase-Head, Abschnitt „Scope"). Wer das baut, ändert diese Funktion und ihre Tests, sonst
    nichts.
    """
    parsed = urlsplit(uri)
    if parsed.scheme != "https":
        return False
    origin = f"{parsed.scheme}://{parsed.netloc}"
    return origin in settings.allowed_redirect_origins


def register_client(
    *,
    store: AuthStore,
    settings: AuthSettings,
    client_name: str | None,
    application_type: str | None,
    redirect_uris: object,
) -> Client:
    """Wirft `DCRError` bei jeder Ablehnung — der Aufrufer (`routes.py`) baut daraus die
    400er-JSON-Antwort. `redirect_uris` ist bewusst ungetypt im Signaturkopf: der Wert kommt
    roh aus einem geparsten JSON-Body (Systemgrenze, Plan §2.6), die Formprüfung passiert hier.
    """
    if application_type == "native":
        # [SEAM]-Gegenstück: siehe redirect_uri_allowed-Docstring. Solange es keine zweite
        # Vergleichsregel gibt, ist "native" per Definition nicht bedienbar.
        raise DCRError("invalid_client_metadata")
    if (
        not isinstance(redirect_uris, list)
        or not redirect_uris
        or not all(isinstance(uri, str) for uri in redirect_uris)
    ):
        raise DCRError("invalid_redirect_uri")
    for uri in redirect_uris:
        if not redirect_uri_allowed(uri, settings):
            raise DCRError("invalid_redirect_uri")
    return store.create_client(
        client_name=client_name, application_type=application_type, redirect_uris=redirect_uris,
    )


def check_register_rate_limit(store: AuthStore) -> bool:
    """True, wenn die Registrierung das stündliche Kontingent (Plan §2.7) noch nicht
    überschreitet. Zählt bei jedem Aufruf sofort mit — anders als `ratelimit.LoginThrottle` gibt
    es hier keinen Erfolgsfall, der einen Zähler zurücksetzen müsste (deshalb lebt das hier,
    nicht in `ratelimit.py`, dessen Docstring sich ausdrücklich auf Login pro Space bezieht):
    jede Registrierung zählt gegen das globale Kontingent, unabhängig vom Ausgang."""
    return store.increment_register_window() <= MAX_REGISTRATIONS_PER_WINDOW
