"""`build_mcp()` — FastMCP-Instanz mit den sechs registrierten Tools (Plan §1.2, §4 Step 5).
Kennt `fastmcp` und `tools`, nicht HTTP oder Token — die Abhängigkeitsrichtung ist strikt
(Plan §1.2), damit P4/P5 denselben Kern benutzen können, ohne ihn anzufassen.
"""
from __future__ import annotations

from fastmcp import FastMCP

from storage.store import Store

from . import tools
from .permissions import Permissions

DEFAULT_SERVER_NAME = "sharefyx-spaces"


def build_mcp(
    store: Store, permissions: Permissions, *, name: str = DEFAULT_SERVER_NAME
) -> FastMCP:
    mcp = FastMCP(name)
    tools.register(mcp, store=store, permissions=permissions)
    return mcp
