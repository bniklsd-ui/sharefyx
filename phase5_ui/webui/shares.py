"""`widens()`/`require_share_reauth()` (Step 7 Commit 5, Plan §1.2.5/P6-N) — das Re-Auth-Gate
vor jeder rechte-ERWEITERNDEN Freigabeänderung. Eine Verkleinerung (Freigabe zurückziehen,
`human → private`) verlangt nie erneuten Beweis; das Gate schützt gegen Versehen und gegen
injektionsgetriebene Massenfreigabe, nicht gegen einen entschlossenen Agenten — der kann Inhalte
in einen bereits geteilten Space kopieren, ein legitimer Schreibvorgang, den kein Gate hier
sieht.

`ShareState` trägt bewusst nur die fünf Felder, die `AclReader.decision_for()` braucht — nicht
das ganze Item. `widens()` ruft `decision_for()` zweimal auf (vorher/nachher) und vergleicht die
EFFEKTIVEN Lese-/Schreibmengen, nicht die rohen `share_read`/`share_write`-Felder direkt: eine
`.share.yml` kann genauso erweiternd wirken wie ein Item-Feld (Ordner-Verschieben in einen
breiter geteilten Ordner), `decision_for()` kennt beides bereits. `visibility` fließt in diesen
Vergleich strukturell nicht ein (`decision_for()` nutzt es nur für `AclDecision.visibility`,
nie für die `read`/`write`-Vereinigung — das ist Schritt 5s eigener Fund, hier wiederverwendet,
nicht neu erfunden) — `private → human` ist deshalb korrekt NIE ein Widen.
"""
from __future__ import annotations

from dataclasses import dataclass

from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

from storage.acl import AclReader

from .errors import ApiError
from .reauth import verify_reauth


@dataclass(frozen=True, kw_only=True)
class ShareState:
    visibility: str
    share_read: frozenset[str]
    share_write: frozenset[str]
    space: str
    folder: str


def widens(before: ShareState, after: ShareState, *, acl: AclReader) -> bool:
    """Wahr, wenn `after`s effektive Lese- ODER Schreibmenge eine ECHTE Obermenge von `before`s
    ist (Plan §1.2.5) — Rücknahme, `human → private` und reine Inhaltsänderungen sind `False`.
    """
    before_decision = acl.decision_for(
        space=before.space, folder=before.folder, visibility=before.visibility,
        share_read=before.share_read, share_write=before.share_write,
    )
    after_decision = acl.decision_for(
        space=after.space, folder=after.folder, visibility=after.visibility,
        share_read=after.share_read, share_write=after.share_write,
    )
    return (after_decision.read > before_decision.read) or (after_decision.write > before_decision.write)


def require_share_reauth(
    session,
    body: dict,
    *,
    before: ShareState,
    after: ShareState,
    acl: AclReader,
    userdir: UserDirectory,
    throttle: LoginThrottle,
    auth_store: AuthStore,
) -> None:
    """Wirft `ApiError("reauth_required")`, wenn `widens()` wahr ist UND `password`/`totp` im
    Body fehlen oder nicht verifizieren — beide Fälle liefern denselben Code (Plan-Entscheidung,
    `serialized-seeking-aurora.md` Commit 5: der Client kann und muss „fehlt" nicht von „falsch"
    unterscheiden, er zeigt in beiden Fällen dasselbe Mini-Formular und schickt denselben PATCH-
    Body erneut, jetzt mit `password`/`totp`). Kein eigener `ReauthRequired`-Exception-Typ (P6-
    Plan §1.2.5 skizziert einen, `request`/`session`/`before`/`after`/`acl` als Signatur — diese
    Skizze deckt nicht ab, WIE gegen ein echtes Credential geprüft wird; die Prüfung selbst
    braucht `body`/`userdir`/`throttle`/`auth_store` zusätzlich, dieselben Bausteine wie
    `account.py :: _require_reauth()`, hier als Parameter statt als Closure, weil `shares.py`
    kein eigenes `throttle`/`userdir` besitzt. `request` fiel ganz weg — ungenutzt, `body` kommt
    bereits geparst herein, kein zweiter Lesezugriff auf den Request-Stream) — eine
    Exception-Klasse mehr für denselben Übersetzungsschritt wäre eine Indirektion ohne Nutzen.
    """
    if not widens(before, after, acl=acl):
        return
    password = body.get("password")
    code = body.get("totp")
    if not isinstance(password, str) or not isinstance(code, str):
        raise ApiError(
            "reauth_required",
            "Diese Änderung erweitert Zugriffsrechte — Passwort und TOTP-Code nötig.",
        )
    ok = verify_reauth(
        userdir, throttle, auth_store, space=session.space, password=password,
        second_factor=code, now=auth_store.now().timestamp(),
    )
    if not ok:
        raise ApiError("reauth_required", "Re-Authentisierung fehlgeschlagen.")
