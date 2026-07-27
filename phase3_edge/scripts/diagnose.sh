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
# [VERIFY] — Ausgabeformat von "tailscale funnel status" auf dieser VM nie live geprüft
# (Tailscale hier nicht installiert, siehe Step 0). Grep-Muster nach Tailscales dokumentiertem
# Format ("proxy http://127.0.0.1:8765"); bei Abweichung in Step 7 korrigieren.
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

# 6) Wie viel 401-Rauschen in der letzten Stunde? (Nur Information, kein Abbruchkriterium.)
count="$(journalctl -u sharefyx-mcp --since -1h 2>/dev/null | grep -c '"status":401' || true)"
echo "INFO 401-Antworten in der letzten Stunde: ${count:-0}" >&2

echo "DIAGNOSE: alle Prüfungen bestanden." >&2
exit 0
