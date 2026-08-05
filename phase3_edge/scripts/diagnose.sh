#!/usr/bin/env bash
#
# diagnose.sh — automatisiert das Runbook „Connector zeigt Disconnected" (Plan §4 Step 6,
# phase3_edge/CLAUDE.md). Prüft in der dort festgelegten Reihenfolge und gibt bei der ersten
# fehlschlagenden Prüfung GENAU EINE Diagnose plus einen Handlungssatz aus. Rein lesend — kein
# `systemctl restart`, kein Schreibzugriff, kein Löschen.
#
# Aufruf: phase3_edge/scripts/diagnose.sh   (kein sudo nötig für die Lesezugriffe hier)

set -uo pipefail  # bewusst kein -e: jede Prüfung wertet ihren eigenen Exit-Code selbst aus

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_ENV="$PHASE_DIR/local.env"

diagnose() {
  echo "DIAGNOSE: $1" >&2
  echo "NÄCHSTER SCHRITT: $2" >&2
  exit 1
}

# 1) Läuft der Dienst?
if ! systemctl is-active --quiet sharefyx-mcp 2>/dev/null; then
  diagnose "sharefyx-mcp ist nicht aktiv (oder nicht installiert)." \
           "journalctl -u sharefyx-mcp -n 50"
fi
echo "OK  sharefyx-mcp aktiv" >&2

# 2) Antwortet er lokal?
if ! curl -sf http://127.0.0.1:8765/health >/dev/null; then
  diagnose "Dienst läuft, antwortet aber nicht auf 127.0.0.1:8765/health." \
           "Port belegt oder Start hängt — journalctl -u sharefyx-mcp -n 50 prüfen"
fi
echo "OK  /health lokal erreichbar" >&2

# 3) Ist der Tailscale-Node online?
if ! command -v tailscale >/dev/null 2>&1; then
  diagnose "tailscale-CLI nicht gefunden." \
           "Tailscale installieren (siehe phase3_edge/CLAUDE.md, Runbook Inbetriebnahme)"
fi
if ! tailscale status >/dev/null 2>&1; then
  diagnose "tailscale status meldet einen Fehler — Node vermutlich offline." \
           "Uplink prüfen, ggf. tailscaled neu starten"
fi
echo "OK  tailscale status erreichbar" >&2

# 4) Ist der Funnel für unseren Port an?
# [2026-08-05, P5 Step 8] Hier stand noch ein offener `[VERIFY]`-Vermerk („Ausgabeformat nie
# live geprüft, bei Abweichung in Step 7 korrigieren"). **V13 ist seit dem 2026-07-28 geschlossen**
# (P4 Step 0, `phase3_edge/CLAUDE.md`): das Skript lief komplett gegen ein echtes
# `tailscale funnel status`, das Grep-Muster matcht die reale Ausgabe unverändert. Der Vermerk
# war Drift, nicht offene Arbeit.
if ! tailscale funnel status 2>/dev/null | grep -q "127.0.0.1:8765"; then
  diagnose "tailscale funnel status zeigt Port 8765 nicht als aktiv." \
           "tailscale funnel --bg 8765"
fi
echo "OK  Funnel für Port 8765 aktiv" >&2

# 5) Antwortet er öffentlich? (Hostname aus local.env, falls vorhanden — sonst übersprungen.)
host=""
if [[ -f "$LOCAL_ENV" ]]; then
  # shellcheck disable=SC1090
  host="$(set -a && source "$LOCAL_ENV" && set +a && echo "${ALLOWED_HOSTS%%,*}")"
fi
if [[ -z "$host" ]]; then
  echo "WARNUNG: kein Hostname aus $LOCAL_ENV ablesbar — Prüfung 5 übersprungen." >&2
else
  if ! curl -sf "https://$host/health" >/dev/null; then
    diagnose "Lokal ok, öffentlich (https://$host/health) nicht erreichbar." \
             "Siehe Fallstrick 'funnel status sagt on, TLS-Handshake hängt' im Runbook — meist fehlt nodeAttrs:funnel im Tailnet-Policy-File"
  fi
  echo "OK  /health öffentlich über $host erreichbar" >&2
fi

# 6) Ist die Web-UI erreichbar? (P5 Step 8 — bis dahin prüfte dieses Skript nur /health und
#    damit nur die Wurzel-App; ein Deploy, das `webui` nicht mountet, fiel hier nicht auf.)
ui_code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:8765/ui/login 2>/dev/null || echo 000)"
if [[ "$ui_code" != "200" ]]; then
  diagnose "/ui/login antwortet mit $ui_code statt 200 — Web-UI nicht gemountet oder kaputt." \
           "journalctl -u sharefyx-mcp -n 50; ggf. phase5_ui/scripts/rollback.sh"
fi
echo "OK  /ui/login lokal erreichbar" >&2

# -- Ab hier nur noch INFORMATION, kein Abbruchkriterium -------------------------------------
# Diese Werte beantworten „ist das normal?", nicht „ist etwas kaputt?". Sie stehen deshalb NACH
# allen harten Prüfungen: ein fehlendes Backup ist ein Betriebsproblem, aber kein Grund, die
# Diagnose eines nicht erreichbaren Dienstes abzubrechen.

# 7) Wie viel 401-Rauschen in der letzten Stunde?
count="$(journalctl -u sharefyx-mcp --since -1h 2>/dev/null | grep -c '"status":401' || true)"
echo "INFO 401-Antworten in der letzten Stunde: ${count:-0}" >&2

# 8) Wie viele UI-Sitzungen sind offen? (P5 Step 8. Nur lesend, eigene Verbindung — der Dienst
#    hält die Datei geöffnet, SQLite verträgt einen zweiten Leser.)
auth_db="/var/lib/sharefyx/auth.sqlite3"
if [[ -r "$auth_db" ]] && command -v sqlite3 >/dev/null 2>&1; then
  sessions="$(sqlite3 "$auth_db" "SELECT COUNT(*) FROM ui_sessions WHERE revoked_at IS NULL;" 2>/dev/null || echo "?")"
  echo "INFO offene UI-Sitzungen: $sessions" >&2
else
  echo "INFO UI-Sitzungen: $auth_db nicht lesbar (als root aufrufen für diese Zahl)" >&2
fi

# 9) Wann lief das letzte Auth-Backup? (P5 Step 8, P5-R. Ein Backup-Timer, der seit Wochen still
#    ist, fällt sonst erst auf, wenn man das Backup braucht.)
auth_backup_dir="/var/lib/sharefyx-backup/auth"
if [[ -d "$auth_backup_dir" ]]; then
  newest="$(find "$auth_backup_dir" -maxdepth 1 -name 'auth-*.cred' 2>/dev/null | sort | tail -n1)"
  if [[ -n "$newest" ]]; then
    echo "INFO jüngstes Auth-Backup: $(basename "$newest") ($(date -u -r "$newest" +%Y-%m-%dT%H:%M:%SZ))" >&2
  else
    echo "WARNUNG: $auth_backup_dir existiert, enthält aber keine Generation —" \
         "sudo systemctl start sharefyx-authbackup.service" >&2
  fi
else
  echo "WARNUNG: kein Auth-Backup-Verzeichnis ($auth_backup_dir) —" \
       "sudo systemctl enable --now sharefyx-authbackup.timer" >&2
fi

# 10) Welches Release läuft gerade? (P5 Step 8. Nach dem Umstieg auf Release-Verzeichnisse ist
#     „welcher Stand ist live" nicht mehr aus dem Arbeitsverzeichnis ablesbar.)
current_link="/opt/sharefyx/current"
if [[ -L "$current_link" ]]; then
  echo "INFO aktives Release: $(readlink -f "$current_link")" >&2
else
  echo "INFO aktives Release: kein $current_link — der Dienst läuft aus einem Arbeitsverzeichnis" >&2
fi

echo "DIAGNOSE: alle Prüfungen bestanden." >&2
exit 0
