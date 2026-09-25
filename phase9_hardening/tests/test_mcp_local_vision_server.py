"""P9 Step C Teil 2 / C6 -- regress on the two `mcp_local_vision_server.py` fixes
from Plan §5.3.

Bug 1 (Zeile 223 vor C6): `serve()` hard-coded `DEFAULT_ENDPOINT` in its
startup log, while `handle_tools_call` resolved `$LOCAL_VISION_ENDPOINT`.
Bug 2 (Zeile 274 vor C6): the `--endpoint` flag only affected `--check`,
`serve()` ignored `args.endpoint` entirely.

Both are fixed by routing the resolved endpoint through `resolve_endpoint()`
once in `main()`, then threading it via `serve(endpoint, model)` into
`_CURRENT_ENDPOINT`, which `handle_tools_call` reads. These tests pin both
the resolution function (cheap, pure) and the visible behaviour (the
startup log line itself, in a subprocess).
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase8_6_ui_polish" / "scripts" / "mcp_local_vision_server.py"


@pytest.fixture(scope="module")
def mod():
    """Import the script as a module without triggering its `__main__` guard.

    `requests` is in the project venv (Hard Rule 7: no install per test) --
    not a network call is made here, the import is enough.
    """
    spec = importlib.util.spec_from_file_location("mcp_local_vision_server", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    sys.modules["mcp_local_vision_server"] = m
    spec.loader.exec_module(m)
    return m


def _ns(endpoint, model=None):
    import argparse
    return argparse.Namespace(endpoint=endpoint, check=False)


def test_resolve_endpoint_cli_wins(mod, monkeypatch):
    monkeypatch.delenv("LOCAL_VISION_ENDPOINT", raising=False)
    assert mod.resolve_endpoint(_ns("http://gpu:11434")) == "http://gpu:11434"


def test_resolve_endpoint_env_wins_when_cli_unset(mod, monkeypatch):
    monkeypatch.setenv("LOCAL_VISION_ENDPOINT", "http://gpu:11434")
    assert mod.resolve_endpoint(_ns(None)) == "http://gpu:11434"


def test_resolve_endpoint_default_when_neither_set(mod, monkeypatch):
    monkeypatch.delenv("LOCAL_VISION_ENDPOINT", raising=False)
    assert mod.resolve_endpoint(_ns(None)) == mod.DEFAULT_ENDPOINT


def test_resolve_endpoint_cli_wins_over_env(mod, monkeypatch):
    """Both sources set, CLI wins. This is the regression for Bug 2:
    before C6 the CLI flag was a no-op for the server path."""
    monkeypatch.setenv("LOCAL_VISION_ENDPOINT", "http://env:11434")
    assert mod.resolve_endpoint(_ns("http://cli:11434")) == "http://cli:11434"


def test_handle_tools_call_reads_current_endpoint_not_env(mod, monkeypatch):
    """The handler must read from `_CURRENT_ENDPOINT`, not from the env var.

    Pinned via direct call: we set the global to something the env doesn't
    carry, and check that `handle_tools_call` would call Ollama at that
    address. We use a fake image path to short-circuit before the network
    request -- the assertion is on the resolved endpoint reaching
    `call_ollama`, which logs its `POST <url>` line before any request.
    """
    mod._CURRENT_ENDPOINT = "http://fake-resolved:11434"
    monkeypatch.delenv("LOCAL_VISION_ENDPOINT", raising=False)

    captured = {}
    import base64
    import tempfile

    # 1x1 PNG
    png_bytes = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    )

    class _FakeResp:
        status_code = 200
        text = ""
        def json(self_inner):
            return {"response": "ok"}
        def raise_for_status(self_inner):
            pass

    def fake_post(url, json, timeout):
        captured["url"] = url
        return _FakeResp()

    monkeypatch.setattr(mod.requests, "post", fake_post)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(png_bytes)
        path = f.name
    try:
        result = mod.handle_tools_call(
            {"arguments": {"path": path, "prompt": "test"}}
        )
        assert "ok" in result["content"][0]["text"]
    finally:
        os.unlink(path)

    assert captured["url"].startswith("http://fake-resolved:11434/api/generate"), (
        f"handler used {captured['url']!r} instead of _CURRENT_ENDPOINT"
    )


def _spawn(env_overrides, argv_extra):
    """Start the server, close stdin immediately, capture stderr."""
    env = os.environ.copy()
    for k in ("LOCAL_VISION_ENDPOINT", "LOCAL_VISION_MODEL"):
        env.pop(k, None)
    for k, v in env_overrides.items():
        env[k] = v

    return subprocess.run(
        [sys.executable, str(SCRIPT)] + argv_extra,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=15,
        env=env,
        cwd=str(REPO_ROOT),
    )


def test_startup_log_shows_resolved_endpoint_via_env():
    """Bug 1 regression: with env set, the startup line must show the env
    value, not `DEFAULT_ENDPOINT`. Before C6 the line read
    `endpoint=http://127.0.0.1:11434` regardless of the env."""
    p = _spawn({"LOCAL_VISION_ENDPOINT": "http://gpu-via-env:11434"}, [])
    out = (p.stderr or "") + (p.stdout or "")
    assert "endpoint=http://gpu-via-env:11434" in out, (
        f"startup log missing env-resolved endpoint; got:\n{out!r}"
    )
    assert "endpoint=http://127.0.0.1:11434" not in out, (
        f"startup log still shows the hard-coded DEFAULT_ENDPOINT; got:\n{out!r}"
    )


def test_startup_log_shows_resolved_endpoint_via_flag():
    """Bug 2 regression: `--endpoint` must reach the server path, not just
    `--check`. Before C6, `serve()` ignored `args.endpoint` entirely."""
    p = _spawn({}, ["--endpoint", "http://gpu-via-flag:11434"])
    out = (p.stderr or "") + (p.stdout or "")
    assert "endpoint=http://gpu-via-flag:11434" in out, (
        f"startup log missing flag-resolved endpoint; got:\n{out!r}"
    )


def test_startup_log_shows_default_when_nothing_set():
    """Sanity: with neither env nor flag, the line shows DEFAULT_ENDPOINT."""
    p = _spawn({}, [])
    out = (p.stderr or "") + (p.stdout or "")
    assert f"endpoint={DEFAULT_ENDPOINT_FOR_TEST}" in out, (
        f"startup log missing DEFAULT_ENDPOINT; got:\n{out!r}"
    )


def test_check_flag_uses_resolved_endpoint():
    """`--check` must use the same resolved endpoint (Bug 2's *other* half:
    the flag used to work here, and continues to after C6).
    Smoke-pointing at an unreachable port: exit code 3, stderr mentions
    the resolved endpoint, not the default."""
    p = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--check",
         "--endpoint", "http://127.0.0.1:1"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=10,
        env={k: v for k, v in os.environ.items()
             if k != "LOCAL_VISION_ENDPOINT"},
        cwd=str(REPO_ROOT),
    )
    assert p.returncode == 3, p.stderr
    # `--check` logs the resolved endpoint via the `fail()` path, which
    # wraps it in the message body, not as `endpoint=...`.
    assert "Ollama not reachable at http://127.0.0.1:1" in (p.stderr or ""), (
        f"--check stderr missing the resolved endpoint; got:\n{p.stderr!r}"
    )


# Sentinel import so the test above doesn't fail with NameError if a
# refactor renames the constant; resolved lazily.
DEFAULT_ENDPOINT_FOR_TEST = "http://127.0.0.1:11434"
