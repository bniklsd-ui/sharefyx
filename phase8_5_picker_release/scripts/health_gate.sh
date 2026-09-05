#!/usr/bin/env bash
#
# health_gate.sh — Phase-8.5-Health-Gate (D3, P8.5-17).
#
# Verifiziert nach dem Deploy, dass der laufende sharefyx-mcp-Dienst alle Gates besteht:
#   1. /health antwortet 200 (mit Retry-Loop, max --max-wait Sekunden)
#   2. /ui/login antwortet 200
#   3. /api/v1/me antwortet 401 ohne Cookie
#   4. /mcp/ antwortet 401 ohne Bearer
#   5. .rail__version im HTML matcht --expected-version (Default v3.0.1)
#   6. /opt/sharefyx/current zeigt auf ein Release-Verzeichnis mit git-Historie
#   7. Optional: docs/UPDATE_LOG.md oberster Eintrag ist heute (--require-todays-update-log)
#   8. Optional: Release-SHA stimmt mit --expected-sha ueberein
#
# NICHT in diesem Skript: V105 (echter Anthropic-Connector verbindet) — ist manuelle
# Browser/Connector-Pruefung, Nikinger-Aktion (Plan §5 D3).
#
# Aufruf:
#   phase8_5_picker_release/scripts/health_gate.sh                              # D3 nach D2
#   phase8_5_picker_release/scripts/health_gate.sh --expected-version=v2.2.3   # Pre-D2-Baseline
#   phase8_5_picker_release/scripts/health_gate.sh --require-todays-update-log  # strikter Post-D2
#   phase8_5_picker_release/scripts/health_gate.sh --expected-sha=6f19a8f       # exakter Release-Match
#
# Ausgabe: eine JSON-Zeile auf stdout (Hard Rule 7), Details auf stderr.
# Exit:   0 = alle Gates gruen, 1 = mindestens ein Gate rot.

set -uo pipefail

EXPECTED_VERSION="${EXPECTED_VERSION:-v3.0.1}"
PORT="${PORT:-8765}"
BASE_URL="http://127.0.0.1:${PORT}"
CURRENT_LINK="${SHAREFYX_CURRENT_LINK:-/opt/sharefyx/current}"
MAX_WAIT="${MAX_WAIT:-30}"
REQUIRE_TODAYS_UPDATE_LOG=0
EXPECTED_SHA=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --expected-version=*) EXPECTED_VERSION="${1#*=}" ;;
    --port=*)             PORT="${1#*=}"; BASE_URL="http://127.0.0.1:${PORT}" ;;
    --current-link=*)     CURRENT_LINK="${1#*=}" ;;
    --max-wait=*)         MAX_WAIT="${1#*=}" ;;
    --require-todays-update-log) REQUIRE_TODAYS_UPDATE_LOG=1 ;;
    --expected-sha=*)     EXPECTED_SHA="${1#*=}" ;;
    -h|--help)
      sed -n '2,28p' "$0"
      exit 0
      ;;
    *)
      echo "ABBRUCH: unbekanntes Argument: $1" >&2
      exit 2
      ;;
  esac
  shift
done

probe() {
  curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$1" 2>/dev/null || echo "000"
}

FAILED=0
FIRST_REASON=""
record_fail() {
  echo "FEHLER: $1" >&2
  if [[ -z "$FIRST_REASON" ]]; then FIRST_REASON="$1"; fi
  FAILED=1
}
ok() { echo "OK  $1" >&2; }

# -- Gate 1: /health mit Retry-Loop (wie deploy.sh Z. 192-200) --------------------------
echo "Warte auf /health (max ${MAX_WAIT}s)..." >&2
gate1_ok=0
deadline=$(( SECONDS + MAX_WAIT ))
while (( SECONDS < deadline )); do
  if [[ "$(probe "$BASE_URL/health")" == "200" ]]; then
    gate1_ok=1
    break
  fi
  sleep 1
done
if (( gate1_ok == 1 )); then
  ok "/health -> 200"
else
  record_fail "/health kam nicht auf 200 binnen ${MAX_WAIT}s"
fi

# -- Gates 2-4: nur wenn Gate 1 gruen (wie deploy.sh Z. 202-217) -----------------------
if (( gate1_ok == 1 )); then
  for spec in "/ui/login:200" "/api/v1/me:401" "/mcp/:401"; do
    path="${spec%:*}"
    want="${spec##*:}"
    got="$(probe "$BASE_URL$path")"
    if [[ "$got" == "$want" ]]; then
      ok "$path -> $got"
    else
      record_fail "$path erwartet $want, erhalten $got"
    fi
  done
fi

# -- Gate 5: .rail__version im HTML (oeffentliche static-Route, NICHT /ui/login) -------
# /ui/login rendert das Auth-Template (webui/pages.py), das keine Rail enthaelt.
# /ui/static/app.html ist die Datei, die der Browser laedt -- prueft damit den vollen Stack
# (Static-Route + ausgelieferte Datei).
active_release=""
actual_version=""
if (( gate1_ok == 1 )); then
  static_url="$BASE_URL/ui/static/app.html"
  page="$(curl -sf --max-time 5 "$static_url" 2>/dev/null || true)"
  # app.html:20 -- <div class="rail__brand">sharefyx<span class="rail__version">v3.0.1</span></div>
  actual_version="$(printf '%s' "$page" | grep -oE 'rail__version"[^>]*>[^<]+' | sed -E 's/.*>([^<]+)$/\1/' | head -1 || true)"
  if [[ -z "$actual_version" ]]; then
    record_fail ".rail__version nicht im HTML von $static_url gefunden (Datei nicht erreichbar oder leer)"
  elif [[ "$actual_version" != "$EXPECTED_VERSION" ]]; then
    record_fail ".rail__version ist '$actual_version', erwartet '$EXPECTED_VERSION'"
  else
    ok ".rail__version -> $actual_version"
  fi
fi

# -- Gate 6: /opt/sharefyx/current ist ein Release-Verzeichnis -------------------------
if [[ -L "$CURRENT_LINK" ]]; then
  active_release="$(readlink -f "$CURRENT_LINK")"
  ok "$CURRENT_LINK -> $active_release"
elif [[ -d "$CURRENT_LINK" ]]; then
  active_release="$CURRENT_LINK"
  ok "$CURRENT_LINK ist ein Verzeichnis (kein Symlink)"
else
  record_fail "$CURRENT_LINK ist weder Symlink noch Verzeichnis"
fi

release_sha=""
if [[ -n "$active_release" && -d "$active_release/.git" ]]; then
  release_sha="$(git -C "$active_release" rev-parse HEAD 2>/dev/null || echo unknown)"
  ok "Release-SHA: $release_sha"
elif [[ -n "$active_release" ]]; then
  record_fail "$active_release enthaelt kein .git — kein Release-Checkout"
fi

# -- Gate 7 (optional): docs/UPDATE_LOG.md oberster Eintrag ist heute -----------------
if (( REQUIRE_TODAYS_UPDATE_LOG == 1 )); then
  if [[ -n "$active_release" && -f "$active_release/docs/UPDATE_LOG.md" ]]; then
    top_date="$(grep -m1 -E '^## [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$active_release/docs/UPDATE_LOG.md" 2>/dev/null | sed -E 's/^## //' || true)"
    today_utc="$(date -u +%F)"
    today_local="$(date +%F)"
    if [[ -z "$top_date" ]]; then
      record_fail "docs/UPDATE_LOG.md in $active_release hat keinen ## YYYY-MM-DD-Eintrag"
    elif [[ "$top_date" != "$today_utc" && "$top_date" != "$today_local" ]]; then
      record_fail "docs/UPDATE_LOG.md oberster Eintrag ist $top_date, erwartet $today_utc oder $today_local"
    else
      ok "docs/UPDATE_LOG.md oberster Eintrag: $top_date"
    fi
  else
    record_fail "docs/UPDATE_LOG.md in $active_release nicht lesbar"
  fi
fi

# -- Gate 8 (optional): Release-SHA matcht Erwartung ----------------------------------
# Akzeptiert short UND full SHA (git log --oneline liefert die kurze Form).
if [[ -n "$EXPECTED_SHA" ]]; then
  if [[ "$release_sha" == "$EXPECTED_SHA"* ]]; then
    ok "Release-SHA $release_sha matched --expected-sha=$EXPECTED_SHA"
  else
    record_fail "Release-SHA ist $release_sha, erwartet $EXPECTED_SHA (oder Prefix davon)"
  fi
fi

# -- JSON auf stdout, Hard Rule 7 ------------------------------------------------------
if (( FAILED == 0 )); then
  printf '{"ts":"%s","action":"health_gate","result":"ok","expected_version":"%s","actual_version":"%s","active_release":"%s","release_sha":"%s","port":%s}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$EXPECTED_VERSION" "${actual_version:-}" "${active_release:-}" "${release_sha:-}" "$PORT"
  exit 0
else
  printf '{"ts":"%s","action":"health_gate","result":"failed","expected_version":"%s","actual_version":"%s","active_release":"%s","release_sha":"%s","port":%s,"reason":"%s"}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$EXPECTED_VERSION" "${actual_version:-}" "${active_release:-}" "${release_sha:-}" "$PORT" "$FIRST_REASON"
  exit 1
fi
