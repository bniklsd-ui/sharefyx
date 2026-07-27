#!/usr/bin/env bash
# phase3_edge/scripts/abnahme_run.sh
#
# Fährt die maschinell prüfbaren Zeilen der P3-Abnahmematrix ab und schreibt einen
# einreichbaren CLI-Ausschnitt auf stdout. Fortschritt und Warnungen gehen auf stderr
# (Hard Rule 7).
#
# WICHTIG — warum dieses Skript einen eigenen Redaktions-Filter hat:
# Test 9 prüft, ob ein Token im Journal steht. Ein Prüfwerkzeug, das den Token dabei in
# seine eigene Ausgabe schreibt, hat das Problem nur verschoben. Deshalb läuft JEDE Zeile
# dieses Skripts durch redact(): das eingegebene Token und jedes /mcp/<segment> werden
# ersetzt, bevor irgendetwas ausgegeben wird. Der Token wird über `read -rs` eingelesen,
# nie als Argument übergeben (Argumente landen in der Shell-History und in `ps`).
#
# Aufruf:
#   ./abnahme_run.sh start      # Startzeitpunkt für die --since-Prüfungen setzen
#   ./abnahme_run.sh run        # Prüfungen fahren            (ohne root: root-Tests -> skip)
#   sudo -E ./abnahme_run.sh run --with-kill                  # inkl. Kill-Test
set -euo pipefail

# ---------------------------------------------------------------- Konfiguration
HOST="${SHAREFYX_HOST:-}"                                   # <node>.<tailnet>.ts.net
PORT="${SPACE_PORT:-8765}"
UNIT="${SHAREFYX_UNIT:-sharefyx-mcp}"
TIMER="${SHAREFYX_TIMER:-sharefyx-backup}"
DATA_ROOT="${SHAREFYX_DATA_ROOT:-}"
BACKUP_DIR="${SHAREFYX_BACKUP_DIR:-/var/backups/sharefyx}"
STATE="${SHAREFYX_ABNAHME_STATE:-/var/tmp/sharefyx-abnahme-start}"
TITLE_MARKER="${SHAREFYX_TITLE_MARKER:-ZZZ-TITELMARKER-P3-7B3E1D}"
BODY_MARKER="${SHAREFYX_BODY_MARKER:-BODYMARKER-P3-4A9C6E}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RESTORE_CHECK="$REPO_ROOT/phase3_edge/scripts/restore_check.sh"

TOKEN=""                      # wird interaktiv eingelesen, nie aus einem Argument
PASS=0; FAIL=0; SKIP=0; MANUAL=0

# ---------------------------------------------------------------- Redaktion
redact() {
  local out
  out="$(sed -E 's#(/mcp/)[^[:space:]"'"'"']+#\1<redacted>#g')"
  if [ -n "$TOKEN" ]; then
    out="${out//"$TOKEN"/<TOKEN-REDACTED>}"
  fi
  printf '%s\n' "$out"
}
emit() { printf '%s\n' "$*" | redact; }
note() { printf '%s\n' "$*" >&2; }

result() { # result <status> <nr> <text> [detail]
  local st="$1" nr="$2" txt="$3" detail="${4:-}"
  case "$st" in
    ok)      PASS=$((PASS+1));   emit "[ok]      $nr  $txt${detail:+  — $detail}" ;;
    fail)    FAIL=$((FAIL+1));   emit "[FEHLER]  $nr  $txt${detail:+  — $detail}" ;;
    skip)    SKIP=$((SKIP+1));   emit "[skip]    $nr  $txt${detail:+  — $detail}" ;;
    manual)  MANUAL=$((MANUAL+1)); emit "[manuell] $nr  $txt${detail:+  — $detail}" ;;
  esac
}

have() { command -v "$1" >/dev/null 2>&1; }
is_root() { [ "$(id -u)" -eq 0 ]; }

# ---------------------------------------------------------------- start
cmd_start() {
  local ts; ts="$(date -Is)"
  printf '%s\n' "$ts" > "$STATE"
  note "Startzeitpunkt gesetzt: $ts  ($STATE)"
  note "Ab jetzt die Connector-Tests 2–5 fahren, danach: $0 run"
}

# ---------------------------------------------------------------- run
cmd_run() {
  local with_kill=0
  [ "${1:-}" = "--with-kill" ] && with_kill=1

  local since
  if [ -n "${SINCE:-}" ]; then since="$SINCE"
  elif [ -r "$STATE" ]; then since="$(cat "$STATE")"
  else
    note "WARNUNG: kein Startzeitpunkt gefunden ($STATE). Nutze 'today'."
    note "         Für einen sauberen Nachweis vorher '$0 start' laufen lassen."
    since="today"
  fi

  if [ -z "$HOST" ]; then
    note "SHAREFYX_HOST ist nicht gesetzt — die externen Prüfungen (1, 11) werden übersprungen."
  fi

  note "Token für Test 9 eingeben (Eingabe bleibt unsichtbar, leer = Test 9 überspringen):"
  read -rs TOKEN || true
  note ""

  emit "# P3-Abnahme — maschineller Lauf"
  emit "# Datum:  $(date -Is)"
  emit "# Host:   ${HOST:-<nicht gesetzt>}"
  emit "# Unit:   $UNIT"
  emit "# --since $since"
  emit ""

  # --- 1  /health von außen -------------------------------------------------
  if [ -n "$HOST" ]; then
    if body="$(curl -fsS --max-time 15 "https://$HOST/health" 2>&1)"; then
      if printf '%s' "$body" | grep -q '"uptime_s"'; then
        result ok 1 "/health von außen" "$body"
      else
        result fail 1 "/health von außen: uptime_s fehlt (P3-I noch nicht gebaut?)" "$body"
      fi
    else
      result fail 1 "/health von außen nicht erreichbar" "$body"
    fi
  else
    result skip 1 "/health von außen" "SHAREFYX_HOST nicht gesetzt"
  fi

  # --- 2–5  über die Connectors --------------------------------------------
  result manual 2 "Connector niklas: ein Read + ein Write" "in Claude fahren"
  result manual 3 "Connector fabian: ein Read + ein Write im eigenen Space" "in Claude fahren"
  result manual 4 "Cross-Space: fremder Body gewrappt, Schreibversuch -> write_denied" "in Claude fahren"
  result manual 5 "list_spaces bei leerem fabian -> item_count 0" "in Claude fahren"

  # --- 6  Reboot ------------------------------------------------------------
  if have systemd-analyze; then
    result manual 6 "Reboot-Test" "uptime seit: $(uptime -s 2>/dev/null || echo unbekannt)"
  else
    result manual 6 "Reboot-Test" "sudo reboot, danach Test 1 wiederholen"
  fi

  # --- 7  Kill-Test ---------------------------------------------------------
  if ! have systemctl; then
    result skip 7 "Kill-Test" "kein systemd"
  elif ! systemctl cat "$UNIT" >/dev/null 2>&1; then
    result skip 7 "Kill-Test" "Unit $UNIT existiert nicht (Step 4 noch offen)"
  elif [ "$with_kill" -ne 1 ]; then
    result skip 7 "Kill-Test" "nicht angefordert — erneut mit --with-kill"
  elif ! is_root; then
    result skip 7 "Kill-Test" "braucht root: sudo -E $0 run --with-kill"
  else
    systemctl kill -s KILL "$UNIT" || true
    sleep 10
    if hb="$(curl -fsS --max-time 10 "http://127.0.0.1:$PORT/health" 2>&1)"; then
      result ok 7 "Kill-Test: Dienst nach 10 s wieder gesund" "$hb"
    else
      result fail 7 "Kill-Test: Dienst nach 10 s nicht gesund" "$hb"
    fi
  fi

  # --- 8  Request-Log -------------------------------------------------------
  if ! have journalctl; then
    result skip 8 "Request-Log" "kein journalctl"
  else
    local log; log="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null || true)"
    if [ -z "$log" ]; then
      result skip 8 "Request-Log" "keine Journal-Einträge (Unit läuft nicht, oder Leserechte fehlen: Gruppe adm/systemd-journal)"
    else
      local tools; tools="$(printf '%s\n' "$log" | grep -c '"ev":"tool"' || true)"
      if [ "$tools" -gt 0 ]; then
        result ok 8 "Request-Log: $tools Tool-Ereignisse"
        emit ""
        emit "--- Auszug (letzte 5 Tool-Ereignisse) ---"
        printf '%s\n' "$log" | grep '"ev":"tool"' | tail -5 | redact
        emit "-----------------------------------------"
        emit ""
      else
        result fail 8 "Request-Log: kein einziges \"ev\":\"tool\" (Step 2 noch offen?)"
      fi
    fi
  fi

  # --- 9  Token-Grep --------------------------------------------------------
  if [ -z "$TOKEN" ]; then
    result skip 9 "Token-Grep" "kein Token eingegeben"
  elif ! have journalctl; then
    result skip 9 "Token-Grep" "kein journalctl"
  else
    local hits
    hits="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null | grep -cF "$TOKEN" || true)"
    if [ "$hits" -eq 0 ]; then
      result ok 9 "Token-Grep: leer"
    else
      result fail 9 "Token-Grep: $hits Treffer"
      note ""
      note "!!! BEFUND: Der Token steht im Journal."
      note "!!! Die Trefferzeilen werden bewusst NICHT ausgegeben."
      note "!!! Sofort: Token rotieren (--revoke + neu), exportieren, systemctl restart."
      note "!!! Diesen Lauf NICHT als Beleg einchecken."
      note ""
    fi
  fi

  # --- 10  Titel-Grep -------------------------------------------------------
  if ! have journalctl; then
    result skip 10 "Titel-Grep" "kein journalctl"
  else
    local th bh
    th="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null | grep -cF "$TITLE_MARKER" || true)"
    bh="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null | grep -cF "$BODY_MARKER"  || true)"
    if [ "$th" -eq 0 ] && [ "$bh" -eq 0 ]; then
      result ok 10 "Titel- und Body-Grep: leer"
    else
      result fail 10 "Inhalt im Log" "Titel: $th Treffer, Body: $bh Treffer"
    fi
  fi

  # --- 11  Fremdzugriff -----------------------------------------------------
  if [ -z "$HOST" ]; then
    result skip 11 "Fremdzugriff -> 401" "SHAREFYX_HOST nicht gesetzt"
  else
    local code
    code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://$HOST/mcp/falsch-token" || true)"
    if [ "$code" = "401" ]; then
      local n401
      n401="$(journalctl -u "$UNIT" --since "$since" --no-pager 2>/dev/null | grep -c '"status":401' || true)"
      result ok 11 "Fremdzugriff -> 401" "$n401 401-Zeilen im Log"
    else
      result fail 11 "Fremdzugriff" "HTTP $code statt 401"
    fi
  fi

  # --- 12  Backup-Timer -----------------------------------------------------
  if ! have systemctl; then
    result skip 12 "Backup-Timer" "kein systemd"
  elif ! systemctl cat "$TIMER.timer" >/dev/null 2>&1; then
    result skip 12 "Backup-Timer" "Timer $TIMER.timer existiert nicht (Step 5 noch offen)"
  else
    local last
    last="$(systemctl show -p LastTriggerUSec --value "$TIMER.timer" 2>/dev/null || true)"
    if [ -n "$last" ] && [ "$last" != "0" ] && [ "$last" != "n/a" ]; then
      result ok 12 "Backup-Timer" "letzter Lauf: $last"
      emit ""
      emit "--- systemctl list-timers $TIMER ---"
      systemctl list-timers "$TIMER*" --no-pager 2>/dev/null | redact
      emit "------------------------------------"
      emit ""
    else
      result fail 12 "Backup-Timer" "noch nie ausgelöst — 'sudo systemctl start $TIMER.service' erzwingt einen Lauf"
    fi
  fi

  # --- 13  Restore-Nachweis -------------------------------------------------
  if [ ! -x "$RESTORE_CHECK" ]; then
    result skip 13 "Restore-Nachweis" "restore_check.sh fehlt oder ist nicht ausführbar (Step 5 noch offen)"
  elif [ -z "$DATA_ROOT" ]; then
    result skip 13 "Restore-Nachweis" "SHAREFYX_DATA_ROOT nicht gesetzt"
  else
    if out="$(SHAREFYX_DATA_ROOT="$DATA_ROOT" SHAREFYX_BACKUP_DIR="$BACKUP_DIR" "$RESTORE_CHECK" 2>&1)"; then
      result ok 13 "Restore-Nachweis" "$(printf '%s' "$out" | tail -1)"
    else
      result fail 13 "Restore-Nachweis" "$(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
    fi
  fi

  emit ""
  emit "# Ergebnis: $PASS ok · $FAIL Fehler · $SKIP übersprungen · $MANUAL manuell"
  [ "$FAIL" -eq 0 ]
}

case "${1:-run}" in
  start) cmd_start ;;
  run)   shift || true; cmd_run "${1:-}" ;;
  *)     note "Aufruf: $0 {start|run [--with-kill]}"; exit 2 ;;
esac
