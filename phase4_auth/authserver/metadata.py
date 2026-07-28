"""Die zwei Metadatendokumente (Plan §2.2): Protected Resource Metadata (RFC 9728) und
Authorization Server Metadata (RFC 8414 + RFC 9207-Flag). Reine Funktionen aus `AuthSettings`,
keine Literale doppelt gepflegt.
"""
from __future__ import annotations

from .config import AuthSettings


def protected_resource_metadata(settings: AuthSettings) -> dict[str, object]:
    """RFC 9728. `resource` MUSS exakt der Connector-URL entsprechen (Plan §0.6)."""
    return {
        "resource": settings.resource,
        "authorization_servers": [settings.issuer],
        "bearer_methods_supported": ["header"],
        "scopes_supported": ["space"],
    }


def authorization_server_metadata(settings: AuthSettings) -> dict[str, object]:
    """RFC 8414 + RFC 9207-Flag. `client_id_metadata_document_supported` bleibt bewusst
    **abwesend** (nicht `false`) — dessen Anwesenheit würde Claude laut aktueller Anthropic-Doku
    (V14, diese Session) auf CIMD statt DCR umschalten (P4-E)."""
    issuer = settings.issuer
    return {
        "issuer": issuer,
        "authorization_endpoint": f"{issuer}/oauth/authorize",
        "token_endpoint": f"{issuer}/oauth/token",
        "registration_endpoint": f"{issuer}/oauth/register",
        "scopes_supported": ["space", "offline_access"],
        "response_types_supported": ["code"],
        "response_modes_supported": ["query"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "token_endpoint_auth_methods_supported": ["none"],
        "code_challenge_methods_supported": ["S256"],
        "authorization_response_iss_parameter_supported": True,
    }
