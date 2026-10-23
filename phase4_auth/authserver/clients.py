"""Dynamic Client Registration (RFC 7591) und die Redirect-Origin-Allowlist (Plan §2.6).
`redirect_uri_allowed` ist die **einzige** Stelle im Paket, an der eine Redirect-URI gegen ein
erlaubtes Ziel geprüft wird — belegt durch `test_redirect_uri_allowed_is_the_only_matching_path`
(Grep über `authserver/`, nicht Verhalten).

**[2026-10-22, P10.5 Block 6, Lock P10.5-O]** Die zweite Vergleichsregel ist jetzt gebaut:
`http://127.0.0.1:<port><pfad>` (native Clients nach RFC 8252 §7.3). Der [SEAM]-Charakter bleibt:
`flows.py` ruft dieselbe Funktion, es gibt keine zweite Vergleichsstelle.
"""
from __future__ import annotations

from urllib.parse import urlsplit

from .config import AuthSettings
from .errors import DCRError
from .models import Client
from .store import AuthStore

MAX_REGISTRATIONS_PER_WINDOW = 20  # Plan §2.7: 20 pro Stunde insgesamt, grober Türstopper


def _is_loopback_uri(uri: str) -> bool:
    """Nur die **Form**: ist das eine Loopback-Adresse (`http://127.0.0.1:…`)?

    `localhost` und `[::1]` sind es **nicht** (P10.5-O): der gemessene opencode-DCR trägt
    `http://127.0.0.1:19876/mcp/oauth/callback` (V209, opencode 1.19.4), und eine
    CSP-Host-Quelle kann kein IPv6-Literal ausdrücken (V210).
    """
    try:
        parsed = urlsplit(uri)
    except ValueError:  # kaputte URI (z. B. ungeschlossene IPv6-Klammer)
        return False
    return parsed.scheme == "http" and parsed.hostname == "127.0.0.1"


def _loopback_uri_allowed(uri: str) -> bool:
    """Die zweite Vergleichsregel: `http://127.0.0.1:<port><pfad>` (P10.5-O, 2026-10-21).

    **Port explizit** (RFC 8252 §7.3 erlaubt auch den Wegfall des Ports — bewusst nicht
    gebaut, siehe P10.5-O: der portagnostische Vergleich hätte den byte-genauen Abgleich in
    `flows.py` verändert). Kein Userinfo, keine Query, kein Fragment.

    `urlsplit().port` wirft `ValueError` bei einem Port, der keine Zahl oder außerhalb
    1..65535 ist — das ist eine **Ablehnung**, kein Fehler: `register_client()` übersetzt sie
    in `invalid_redirect_uri`, nicht in einen 500er.
    """
    try:
        parsed = urlsplit(uri)
        port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "http"
        and parsed.hostname == "127.0.0.1"
        and port is not None
        and 1 <= port <= 65535
        and not parsed.username
        and not parsed.password
        and not parsed.query
        and not parsed.fragment
    )


def redirect_uri_allowed(uri: str, settings: AuthSettings) -> bool:
    """Die EINZIGE Stelle, an der über Rücksprungadressen entschieden wird.

    P4-Policy: exakter Origin-Vergleich gegen `settings.allowed_redirect_origins`,
    ausschließlich `https`.

    **[2026-10-22, P10.5 Block 6, Lock P10.5-O — die zweite Regel ist gebaut.]** Native Clients
    (opencode, CLI-Werkzeuge) registrieren sich per DCR mit einem Loopback-Callback
    (`http://127.0.0.1:<port>/…`, RFC 8252 §7.3). Gebaut wurde: exakter Vergleich, **nur**
    `127.0.0.1`, Port **explizit**, kein Userinfo, keine Query, kein Fragment; `localhost` und
    `[::1]` bleiben abgelehnt. Portagnostisch (RFC 8252 §7.3) wurde bewusst **nicht** gebaut —
    es hätte den byte-genauen Abgleich in `flows.py` verändert, und der [SEAM] verspricht
    „diese Funktion und ihre Tests, sonst nichts". `flows.py` bleibt unberührt und ruft
    weiterhin genau diese Funktion.
    """
    try:
        parsed = urlsplit(uri)
    except ValueError:  # kaputte URI → Ablehnung, kein 500er
        return False
    if parsed.scheme == "http":
        return _loopback_uri_allowed(uri)
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

    **[2026-10-22, P10.5 Block 6, Lock P10.5-O]** Die Pauschalablehnung von `"native"` ist
    weg; `"web"` mit einer Loopback-Adresse wird abgelehnt (`invalid_redirect_uri`).
    """
    if application_type not in (None, "native", "web"):
        # [2026-10-22, P10.5 Block 6, Lock P10.5-O] Drei erlaubte Formen: fehlend/null (das
        # schickt opencode, V209), "native" (RFC 8252 §7.3, Loopback-Callback) und "web"
        # (Browser-Client, https-Origins). Die Pauschalablehnung von "native" (P4,
        # Nikinger-Entscheidung 2026-07-28) fällt weg — jeder andere Wert bleibt ein
        # Metadatenfehler.
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
    if application_type == "web" and any(_is_loopback_uri(uri) for uri in redirect_uris):
        # [2026-10-22, P10.5 Block 6, Lock P10.5-O] Ein "web"-Client läuft im Browser auf
        # einem fremden Rechner — ein Loopback-Rücksprung käme dort nie an.
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
