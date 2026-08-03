"""`reauth.verify_reauth()` (Plan §2.7, P5-P, §5 Step 4) — direkt getestet, ohne HTTP."""
from __future__ import annotations

import httpx
import pytest
from authserver.ratelimit import MAX_FAILURES, LoginThrottle

from webui.reauth import verify_reauth

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"


@pytest.mark.asyncio
async def test_reauth_failures_count_against_the_same_throttle(app, store, users, clock, totp_code):
    """Fünf falsche `verify_reauth()`-Versuche sperren denselben Space auch für den regulären
    UI-Login — `verify_reauth()` benutzt dieselbe `LoginThrottle`/`login_attempts`-Tabelle wie
    `routes_auth.py`, keine eigene."""
    throttle = LoginThrottle(store, now_fn=clock)
    for _ in range(MAX_FAILURES):
        ok = verify_reauth(
            users, throttle, store, space=SPACE, password="falsch", second_factor="000000",
            now=clock().timestamp(),
        )
        assert ok is False

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post(
            "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
        )
    assert response.status_code == 429
