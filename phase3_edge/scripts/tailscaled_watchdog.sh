#!/usr/bin/env bash
#
# tailscaled_watchdog.sh — überwacht tailscaled und restartet, wenn die Control-Plane
# klemmt (Vorfall 2026-09-15, Plan §4.2).
#
# Aufgerufen von tailscaled-watchdog.timer (Type=oneshot, alle 60 s).
#
# Drei Stufen, in dieser Reihenfolge:
#   1. tailscale status --json     billig, lokal, kein Netz   → Self.Online
#   2. tailscale netcheck          nur wenn 1 unklar          → Timeout 30 s
#   3. systemctl restart tailscaled nur wenn 1 und 2 scheitern, Rate-Limit 1/15 min
#
# Härtung im Unit-File (User=savefyx, NoNewPrivileges, ProtectSystem=strict):
# der systemctl-Restart braucht eine Polkit-Regel oder ein sudoers-Fragment
# (V153, P9-Plan §4.2). Ohne diese Berechtigung schlägt Stufe 3 fehl, das
# Skript loggt das und beendet sich — kein Endlos-Restart.
#
# Testbarkeit: alle Pfade und Schwellen sind über Environment-Variablen
# überschreibbar (TAILSCALED_WATCHDOG_*), und die externen Aufrufe (tailscale,
# systemctl, date, timeout, cat) sind PATH-gesteuert. Die Tests in
# phase9_hardening/tests/test_tailscaled_watchdog.py nutzen das.

set -euo pipefail

STATE_FILE="${TAILSCALED_WATCHDOG_STATE_FILE:-/run/tailscaled-watchdog/last_restart}"
RATE_LIMIT_SECONDS="${TAILSCALED_WATCHDOG_RATE_LIMIT:-900}"
NETCHECK_TIMEOUT="${TAILSCALED_WATCHDOG_NETCHECK_TIMEOUT:-30}"

log() { printf '%s tailscaled-watchdog: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"; }

# --- Stufe 1: tailscale status --json → Self.Online
# Rückgabe auf stdout: "true" | "false" | "unclear"
stage1_status() {
    local json rc
    if ! json="$(tailscale status --json 2>/dev/null)"; then
        echo "unclear"; return 0
    fi
    # Inline-Python, weil `tailscale status --json` ein vollständiges JSON-Objekt
    # liefert und `jq` nicht zwingend auf der VM installiert ist (Plan-Hinweis zu
    # Python: sharefyx-mcp.service nutzt denselben Interpreter, ist also da).
    printf '%s' "$json" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print("unclear"); sys.exit(0)
online = d.get("Self", {}).get("Online")
if online is True:
    print("true")
elif online is False:
    print("false")
else:
    print("unclear")
'
}

# --- Stufe 2: netcheck (mit Timeout) → 0 = ok, sonst fail
stage2_netcheck_ok() {
    timeout "$NETCHECK_TIMEOUT" tailscale netcheck >/dev/null 2>&1
}

# --- Stufe 3: Rate-Limit-Prüfung und Restart
# Rückgabe auf stdout: "due" oder "rate-limited: <Sekunden>"
should_restart() {
    local now last
    now="$(date +%s)"
    if [[ ! -f "$STATE_FILE" ]]; then
        echo "due"; return 0
    fi
    last="$(cat "$STATE_FILE" 2>/dev/null || echo 0)"
    if (( now - last >= RATE_LIMIT_SECONDS )); then
        echo "due"; return 0
    fi
    printf 'rate-limited (%ss since last, threshold %ss)' \
        "$((now - last))" "$RATE_LIMIT_SECONDS"
    return 1
}

do_restart() {
    if ! systemctl restart tailscaled.service; then
        log "restart fehlgeschlagen (Polkit-Regel oder sudoers-Fragment fehlt? — V153)"
        return 1
    fi
    date +%s > "$STATE_FILE"
    log "tailscaled restarted (rate-limit window starts now)"
}

main() {
    local s1
    s1="$(stage1_status)"
    case "$s1" in
        true)
            log "healthy: Self.Online=true"
            exit 0
            ;;
        false)
            log "unhealthy: Self.Online=false"
            ;;
        unclear)
            log "status unclear; falling back to netcheck"
            if stage2_netcheck_ok; then
                log "netcheck ok after unclear status; no restart"
                exit 0
            fi
            log "netcheck failed; will restart"
            ;;
    esac

    local decision
    if ! decision="$(should_restart)"; then
        log "$decision"
        exit 0
    fi
    do_restart
}

main "$@"
