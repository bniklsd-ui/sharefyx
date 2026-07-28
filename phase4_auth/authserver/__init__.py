"""Authorization Server (Phase 4) — eigener Prozessraum, kennt weder `mcpserver` noch `storage`
(P4-C). Starlette-Routen, SQLite, `argon2-cffi` — sonst keine neuen Laufzeitabhängigkeiten.
"""
