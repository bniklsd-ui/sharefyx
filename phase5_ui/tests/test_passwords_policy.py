"""`passwords_policy.check()` (Plan §2.9, §5 Step 4)."""
from __future__ import annotations

from webui import passwords_policy


def test_password_policy_rejects_short_and_blocklisted():
    assert passwords_policy.check("short1", space="niklas") != []
    assert passwords_policy.check("password", space="niklas") != []  # in blocklist.txt


def test_password_policy_rejects_space_name_substring():
    reasons = passwords_policy.check("niklas-is-my-secret-passphrase", space="niklas")
    assert any("Space-Namen" in r for r in reasons)


def test_password_policy_accepts_long_passphrase_without_symbols():
    assert passwords_policy.check("correct horse battery staple friend", space="niklas") == []
