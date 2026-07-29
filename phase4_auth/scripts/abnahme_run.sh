#!/usr/bin/env bash
#
# phase4_auth/scripts/abnahme_run.sh — fährt die maschinell prüfbaren Zeilen der
# P4-Abnahmematrix (16 Zeilen, phase4_auth/CLAUDE.md) ab und schreibt einen einreichbaren,
# redigierten CLI-Ausschnitt auf stdout. Fortschritt und Warnungen gehen auf stderr (Hard
# Rule 7). Baut 1:1 auf demselben Aufbau/denselben Sicherheitsmustern wie
# phase3_edge/scripts/abnahme_run.sh: Redaktion vor jeder Ausgabe, Geheimnisse ausschließlich
# über `read -rs` eingelesen, nie als Argument (Argumente landen in der Shell-History und in
# `ps`) — dieses Repo hat mehrere dokumentierte Klartext-Token-Vorfälle, keinen weiteren dieser
# Art produzieren.
#
# Deckt NUR die Zeilen ab, die ohne echte Passwort-/TOTP-Eingabe eines Menschen im echten
# Connector prüfbar sind: 1, 2, 3, 10, 11 (über oauth_smoke.py --base-url), 12, 13, 16. Die
# übrigen acht Zeilen (4, 5, 6, 7, 8, 9, 14, 15) sind bewusst NICHT hier drin — eine
# curl-Nachbildung des Login-Formulars wäre eine zweite, ungetestete Implementierung des
# OAuth-Flusses neben oauth_smoke.py/authserver selbst, genau die Art Duplikation, die dieses
# Repo vermeiden will. Diese acht Zeilen laufen als `result manual` mit der konkreten
# Handlungsanweisung.
#
# Aufruf:
#   ./abnahme_run.sh start      # Startzeitpunkt für die --since-Prüfungen setzen
#   ./abnahme_run.sh run        # Prüfungen fahren
#
# Umgebungsvariablen:
#   SHAREFYX_HOST      Pflicht für run — <node>.<tailnet>.ts.net (ohne https://)
#   SHAREFYX_SPACE     Default: niklas — Space für Zeile 10/11 (oauth_smoke.py)
#   SHAREFYX_UNIT       Default: sharefyx-mcp
#   SHAREFYX_ABNAHME_STATE   Default: /var/tmp/sharefyx-p4-abnahme-start
set -euo pipefail

HOST="${SHAREFYX_HOST:-}"
SPACE="${SHAREFYX_SPACE:-niklas}"
UNIT="${SHAREFYX_UNIT:-sharefyx-mcp}"
STATE="${SHAREFYX_ABNAHME_STATE:-/var/tmp/sharefyx-p4-abnahme-start}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OAUTH_SMOKE="$REPO_ROOT/phase4_auth/scripts/oauth_smoke.py"

PASS=0; FAIL=0; SKIP=0; MANUAL=0

# ---------------------------------------------------------------- Redaktion
# Deckt dieselben Muster ab wie mcpserver/logging_setup.py::_SECRET_PATTERNS — dieses Skript
# gibt Server-Antworten (Discovery-JSON, Fehlerkörper) roh weiter, keine davon enthält laut
# API-Vertrag ein Geheimnis, aber Verteidigung in der Tiefe kostet hier nichts.
redact() {
  sed -E \
    -e 's/("?access_token"?\s*[:=]\s*"?)[^"&[:space:],}]+/\1<redacted>/gi' \
    -e 's/("?refresh_token"?\s*[:=]\s*"?)[^"&[:space:],}]+/\1<redacted>/gi' \
    -e 's/("?code"?\s*[:=]\s*"?)[^"&[:space:],}]+/\1<redacted>/gi' \
    -e 's/(Authorization:[[:space:]]*Bearer[[:space:]]+)[^[:space:]]+/\1<redacted>/gi'
}
emit() { printf '%s\n' "$*" | redact; }
note() { printf '%s\n' "$*" >&2; }

result() { # result <status> <nr> <text> [detail]
  local st="$1" nr="$2" txt="$3" detail="${4:-}"
  case "$st" in
    ok)     PASS=$((PASS+1));     emit "[ok]      $nr  $txt${detail:+  — $detail}" ;;
    fail)   FAIL=$((FAIL+1));     emit "[FEHLER]  $nr  $txt${detail:+  — $detail}" ;;
    skip)   SKIP=$((SKIP+1));     emit "[skip]    $nr  $txt${detail:+  — $detail}" ;;
    manual) MANUAL=$((MANUAL+1)); emit "[manuell] $nr  $txt${detail:+  — $detail}" ;;
  esac
}

have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- start
cmd_start() {
  local ts; ts="$(date -Is)"
  printf '%s\n' "$ts" > "$STATE"
  note "Startzeitpunkt gesetzt: $ts  ($STATE)"
  note "Ab jetzt Zeilen 4–9 (Connector, Passwort/TOTP, Sperre) manuell fahren, danach: $0 run"
}

# ---------------------------------------------------------------- run
cmd_run() {
  if [ -z "$HOST" ]; then
    note "ABBRUCH: SHAREFYX_HOST ist nicht gesetzt (z. B. export SHAREFYX_HOST=<node>.<tailnet>.ts.net)."
    exit 2
  fi

  local since
  if [ -n "${SINCE:-}" ]; then since="$SINCE"
  elif [ -r "$STATE" ]; then since="$(cat "$STATE")"
  else
    note "WARNUNG: kein Startzeitpunkt gefunden ($STATE). Nutze 'today' für Zeile 13."
    note "         Für einen sauberen Nachweis vorher '$0 start' laufen lassen."
    since="today"
  fi

  emit "# P4-Abnahme — maschineller Lauf"
  emit "# Datum:  $(date -Is)"
  emit "# Host:   $HOST"
  emit "# Space:  $SPACE (Zeile 10/11)"
  emit "# --since $since"
  emit ""

  # --- 1  /health von außen -------------------------------------------------
  if body="$(curl -fsS --max-time 15 "https://$HOST/health" 2>&1)"; then
    if printf '%s' "$body" | grep -q '"status":"ok"'; then
      result ok 1 "/health von außen" "$body"
    else
      result fail 1 "/health von außen: status nicht ok" "$body"
    fi
  else
    result fail 1 "/health von außen nicht erreichbar" "$body"
  fi

  # --- 2  POST /mcp/ ohne Token -> 401 + WWW-Authenticate -------------------
  # Trailing Slash ist Pflicht: "POST /mcp" (ohne Slash) trifft Starlettes eigenes
  # Mount-Redirect (307 nach "/mcp/") VOR jeder Auth-Prüfung — kein Bug im Server, aber ein
  # falscher Negativbefund, wenn man ohne Slash testet (live geprüft, 2026-07-29).
  headers="$(curl -sS -D- -o /dev/null --max-time 15 -X POST "https://$HOST/mcp/" 2>&1 || true)"
  code="$(printf '%s' "$headers" | head -1 | grep -oE '[0-9]{3}' || true)"
  if [ "$code" = "401" ] && printf '%s' "$headers" | grep -qi '^www-authenticate:'; then
    result ok 2 "POST /mcp/ ohne Token -> 401 + WWW-Authenticate"
  else
    result fail 2 "POST /mcp/ ohne Token" "HTTP ${code:-?}, Header: $(printf '%s' "$headers" | tr -d '\r' | tr '\n' ' ')"
  fi

  # --- 3  Discovery von außen ------------------------------------------------
  prm="$(curl -fsS --max-time 15 "https://$HOST/.well-known/oauth-protected-resource" 2>&1 || true)"
  asm="$(curl -fsS --max-time 15 "https://$HOST/.well-known/oauth-authorization-server" 2>&1 || true)"
  if disc_summary="$(python -c '
import json, sys
prm = json.loads(sys.argv[1])
asm = json.loads(sys.argv[2])
resource = prm.get("resource", "")
issuer = asm.get("issuer", "")
ok = bool(resource) and bool(issuer) and resource == f"{issuer}/mcp"
print(f"{int(ok)} resource={resource!r} issuer={issuer!r}")
' "$prm" "$asm" 2>/dev/null)"; then
    disc_ok="${disc_summary%% *}"
    disc_detail="${disc_summary#* }"
  else
    disc_ok="0"; disc_detail="Antwort kein gültiges JSON"
  fi
  if [ "$disc_ok" = "1" ]; then
    result ok 3 "Discovery von außen" "$disc_detail"
  else
    result fail 3 "Discovery von außen" "$disc_detail — prm=$prm asm=$asm"
  fi

  # --- 10/11  Refresh-Replay + Code-Replay über oauth_smoke.py --------------
  if [ ! -f "$OAUTH_SMOKE" ]; then
    result skip 10 "Refresh-Replay" "oauth_smoke.py fehlt"
    result skip 11 "Code-Replay" "oauth_smoke.py fehlt"
  else
    note "Zeilen 10/11: oauth_smoke.py --base-url gegen https://$HOST, Space '$SPACE'."
    note "Fragt Passwort + TOTP-Seed interaktiv ab (getpass, nie als Argument)."
    if smoke_json="$(python "$OAUTH_SMOKE" --base-url "https://$HOST" --space "$SPACE" --json 2>/tmp/oauth_smoke_p4_abnahme.stderr)"; then
      smoke_ok=1
    else
      smoke_ok=0
    fi
    refresh_ok="$(printf '%s' "$smoke_json" | python -c '
import json,sys
try:
    data=json.load(sys.stdin)
except Exception:
    print("0"); raise SystemExit
for c in data:
    if c["name"]=="refresh_replay_kills_family":
        print("1" if c["ok"] else "0"); break
else:
    print("0")
' 2>/dev/null || echo 0)"
    code_ok="$(printf '%s' "$smoke_json" | python -c '
import json,sys
try:
    data=json.load(sys.stdin)
except Exception:
    print("0"); raise SystemExit
for c in data:
    if c["name"]=="code_replay_kills_family":
        print("1" if c["ok"] else "0"); break
else:
    print("0")
' 2>/dev/null || echo 0)"
    if [ "$refresh_ok" = "1" ]; then
      result ok 10 "Refresh-Replay (oauth_smoke.py)"
    else
      result fail 10 "Refresh-Replay (oauth_smoke.py)" "siehe /tmp/oauth_smoke_p4_abnahme.stderr"
    fi
    if [ "$code_ok" = "1" ]; then
      result ok 11 "Code-Replay (oauth_smoke.py)"
    else
      result fail 11 "Code-Replay (oauth_smoke.py)" "siehe /tmp/oauth_smoke_p4_abnahme.stderr"
    fi
    if [ "$smoke_ok" = "1" ] && [ "$refresh_ok" = "1" ] && [ "$code_ok" = "1" ]; then
      emit ""
      emit "--- Bonusbeleg für Zeile 4 (echte DCR->Consent->Tool-Aufruf-Runde, synthetischer Client): ---"
      emit "$smoke_json" | redact
      emit "-------------------------------------------------------------------------------------------"
      emit ""
    fi
  fi

  # --- 12  Fremdregistrierung ------------------------------------------------
  reg_resp="$(curl -sS -w '\n%{http_code}' --max-time 15 -X POST "https://$HOST/oauth/register" \
    -H 'Content-Type: application/json' \
    -d '{"client_name":"p4-abnahme-fremd","application_type":"web","redirect_uris":["https://evil.example/callback"]}' 2>&1 || true)"
  reg_code="$(printf '%s' "$reg_resp" | tail -1)"
  reg_body="$(printf '%s' "$reg_resp" | sed '$d')"
  if [ "$reg_code" = "400" ] && printf '%s' "$reg_body" | grep -q '"error":"invalid_redirect_uri"'; then
    result ok 12 "Fremdregistrierung abgelehnt" "$reg_body"
  else
    result fail 12 "Fremdregistrierung" "HTTP $reg_code, $reg_body"
  fi

  # --- 13  Secret-Grep im journald -------------------------------------------
  if ! have journalctl; then
    result skip 13 "Secret-Grep im journald" "kein journalctl"
  else
    note ""
    note "Zeile 13: Passwort für '$SPACE' eingeben, um das Journal seit $since danach zu"
    note "durchsuchen (Eingabe bleibt unsichtbar, leer = Prüfung überspringen):"
    read -rsp "" PW || true
    note ""
    log="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null || true)"
    if [ -z "$PW" ]; then
      result skip 13 "Secret-Grep im journald" "kein Passwort eingegeben"
    elif [ -z "$log" ]; then
      result skip 13 "Secret-Grep im journald" "keine Journal-Einträge (Leserechte fehlen? Gruppe adm/systemd-journal)"
    else
      hits="$(printf '%s' "$log" | grep -cF "$PW" || true)"
      if [ "$hits" -eq 0 ]; then
        result ok 13 "Secret-Grep im journald: leer"
      else
        result fail 13 "Secret-Grep im journald: $hits Treffer"
        note ""
        note "!!! BEFUND: das Passwort steht im Journal."
        note "!!! Die Trefferzeilen werden bewusst NICHT ausgegeben."
        note "!!! Diesen Lauf NICHT als Beleg einchecken — zuerst dem Nikinger melden."
        note ""
      fi
    fi
    unset PW
  fi

  # --- 16  Pfad-Token tot (nur nach dem Schnitt, Runbook Schritt 8) ---------
  mode="$(systemctl show -p Environment "$UNIT" 2>/dev/null | grep -oE 'SPACE_AUTH_MODE=[a-z]+' || true)"
  if [ "$mode" != "SPACE_AUTH_MODE=oauth" ]; then
    result skip 16 "Pfad-Token tot" "SPACE_AUTH_MODE ist noch nicht 'oauth' (${mode:-unbekannt}) — erst nach Runbook-Schritt 8 sinnvoll"
  else
    old_code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://$HOST/mcp/irgendein-altes-token" || true)"
    if [ "$old_code" = "401" ]; then
      result ok 16 "Pfad-Token tot -> 401"
    else
      result fail 16 "Pfad-Token tot" "HTTP $old_code statt 401"
    fi
  fi

  emit ""
  emit "# Maschinell geprüfte Zeilen: $PASS ok · $FAIL Fehler · $SKIP übersprungen"
  emit "# Manuell zu prüfen (nicht Teil dieses Laufs): 4, 5, 6, 7, 8, 9, 14, 15"
  [ "$FAIL" -eq 0 ]
}

case "${1:-run}" in
  start) cmd_start ;;
  run)   cmd_run ;;
  *)     note "Aufruf: $0 {start|run}"; exit 2 ;;
esac
