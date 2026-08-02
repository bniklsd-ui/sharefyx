"""Token-Hashing (Plan §2.3).

**[2026-08-02 Korrektur, P5 Step 0 A]:** dieses Modul trug bis zum P5-Rückbau den gesamten
Pfad-Token-Lebenszyklus (`issue`/`revoke`/`load_space_map`/`save_space_map`, Keyring- und
Credentials-Verzeichnis-Auflösung). Seit dem P4-Schnitt (2026-07-30) war das ohnehin kein Teil
des Live-Request-Pfads mehr, nur noch Bestandswerkzeug für `issue_token.py`/
`export_space_map.py`/`KeyringTokenResolver`. `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` §4.5
markierte den Rückbau für P5 Step 0; `docs/concepts/phase5_ui_plan.md` Step 0 A führt ihn aus.
Beide Skripte sind gelöscht, `KeyringTokenResolver` ist aus `auth.py` entfernt. Übrig bleibt
`hash_token()` — `mcpserver/asgi.py` dokumentiert im eigenen Docstring, dass sie byte-identisch
mit `authserver.crypto.hash_secret` ist, und diese Aussage soll nachprüfbar bleiben, auch ohne
lebenden Aufrufer."""
from __future__ import annotations

import hashlib


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
