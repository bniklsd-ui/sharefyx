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
REPO_TOP="$(cd "$PHASE_DIR/.." && pwd)"
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
#
# **[2026-08-19 Korrektur, Live-Fund nach einem VM-Reboot]:** ein einfaches `curl -sf
# "https://$host/health"` auf DIESER Maschine ist **kein** echter Test des öffentlichen
# Funnel-Pfads — `100.100.100.100` (Tailscales eigener MagicDNS-Resolver) fängt jede
# `*.ts.net`-Anfrage systemweit ab und löst `$host` auf die **Tailnet-IP** (`100.x.x.x`) auf,
# nicht auf die öffentliche Funnel-Relay-IP. Ein Node, der sich selbst über den Tailnet-Mesh
# erreicht, kann antworten, obwohl die Backhaul-Verbindung des Nodes zum öffentlichen
# Funnel-Relay tot ist — genau der Zustand, der nach diesem Reboot vorlag (lokal + `funnel
# status` sahen beide gesund aus, ein echtes Gerät ohne Tailscale bekam
# `NS_ERROR_CONNECTION_REFUSED`). Behoben: DNS explizit gegen einen öffentlichen Resolver
# auflösen und `curl --resolve` gegen genau diese IP fahren — derselbe Weg, den ein Browser
# ohne Tailscale nimmt. `dig`/`getent` fehlen auf manchen Minimalsystemen; `python3` ist hier
# ohnehin Pflicht (Prüfung 12 braucht es bereits).
host=""
if [[ -f "$LOCAL_ENV" ]]; then
  # shellcheck disable=SC1090
  host="$(set -a && source "$LOCAL_ENV" && set +a && echo "${ALLOWED_HOSTS%%,*}")"
fi
if [[ -z "$host" ]]; then
  echo "WARNUNG: kein Hostname aus $LOCAL_ENV ablesbar — Prüfung 5 übersprungen." >&2
else
  public_ip="$(python3 -c '
import socket, sys
try:
    # 1.1.1.1 als DNS-Server erzwingen, kein Fallback auf den System-Resolver (der ist
    # MagicDNS) -- reines UDP-DNS ohne Zusatzpaket, ~30 Zeilen waeren fuer eine Bibliothek zu
    # viel fuer diesen einen Zweck.
    import struct
    host = sys.argv[1]
    qname = b"".join(bytes([len(p)]) + p.encode() for p in host.split(".")) + b"\x00"
    query = b"\xAA\xAA\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + qname + b"\x00\x01\x00\x01"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(query, ("1.1.1.1", 53))
    resp, _ = sock.recvfrom(512)
    ancount = struct.unpack(">H", resp[6:8])[0]
    pos = 12 + len(qname) + 4
    for _ in range(ancount):
        if resp[pos] & 0xC0 == 0xC0:
            pos += 2
        rtype, _, _, rdlen = struct.unpack(">HHIH", resp[pos:pos+10])
        pos += 10
        if rtype == 1 and rdlen == 4:
            print(".".join(str(b) for b in resp[pos:pos+4]))
            break
        pos += rdlen
except Exception:
    pass
' "$host" 2>/dev/null)"
  if [[ -z "$public_ip" ]]; then
    echo "WARNUNG: öffentliche DNS-Auflösung von $host über 1.1.1.1 fehlgeschlagen —" \
         "Prüfung 5 übersprungen (Netz down? DNS-über-UDP blockiert?)." >&2
  elif ! curl -sf --resolve "$host:443:$public_ip" "https://$host/health" >/dev/null; then
    diagnose "Lokal ok, aber über den ECHTEN öffentlichen Pfad ($public_ip, nicht MagicDNS) nicht erreichbar." \
             "sudo systemctl restart tailscaled  # meist reicht das (stale Funnel-Backhaul nach Boot/Netzwechsel) -- danach erneut prüfen. Bleibt es rot: Fallstrick 'funnel status sagt on, TLS-Handshake hängt' im Runbook, meist fehlt nodeAttrs:funnel im Tailnet-Policy-File"
  fi
  echo "OK  /health öffentlich über $host erreichbar (echter Pfad, $public_ip)" >&2
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
#
# **[2026-08-14 Korrektur, Live-Fund beim Post-Deploy-Check]:** `authbackup.sh` läuft bewusst
# OHNE `User=`/`Group=` (root) -- siehe dessen eigener Kommentar: es muss `auth.sqlite3` aus dem
# StateDirectory lesen und `systemd-creds encrypt --with-key=host` (root-only Schlüssel)
# aufrufen. Das Zielverzeichnis selbst erbt daher `0700 root:root`. Ein unprivilegierter
# `diagnose.sh`-Lauf (der Normalfall -- ohne `sudo`) bekam bei `find` bisher lautlos "Permission
# denied" (`2>/dev/null` verschluckt es), `$newest` blieb leer, und das Skript meldete
# fälschlich "keine Generation" samt dem Vorschlag, den Dienst neu zu starten -- obwohl das
# Backup real lief (`journalctl -u sharefyx-authbackup` zeigte zum Fundzeitpunkt
# `"generations":7,"verified":true` von derselben Nacht). Derselbe Lesbarkeits-Check wie
# Prüfung 8 oben (`[[ -r ... ]]`) unterscheidet jetzt "nicht geprüft, weil kein root" von
# "geprüft, keine Generation gefunden" -- Letzteres bleibt eine echte WARNUNG.
auth_backup_dir="/var/lib/sharefyx-backup/auth"
if [[ -r "$auth_backup_dir" ]]; then
  newest="$(find "$auth_backup_dir" -maxdepth 1 -name 'auth-*.cred' 2>/dev/null | sort | tail -n1)"
  if [[ -n "$newest" ]]; then
    echo "INFO jüngstes Auth-Backup: $(basename "$newest") ($(date -u -r "$newest" +%Y-%m-%dT%H:%M:%SZ))" >&2
  else
    echo "WARNUNG: $auth_backup_dir existiert, enthält aber keine Generation —" \
         "sudo systemctl start sharefyx-authbackup.service" >&2
  fi
elif [[ -d "$auth_backup_dir" ]]; then
  echo "INFO Auth-Backup: $auth_backup_dir nicht lesbar (als root aufrufen für diese Prüfung," \
       "z.B. 'sudo $0') — Verzeichnis existiert, Generationen sind 0700 root:root" >&2
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

# 11) Wann lief der Purge-Timer zuletzt? (P6 Step 2, O2 — `authserver/store.py :: purge_expired()`
#     räumt seither auch `token_families`/`clients` ab, aber nur, wenn der Timer tatsächlich
#     läuft. Kein Artefakt wie beim Auth-Backup — `authctl.py purge-expired` schreibt nur eine
#     Logzeile, keine Datei — deshalb hier über systemd selbst, nicht über eine Datei im
#     Dateisystem, gleiche INFO/WARNUNG-Kategorie wie Prüfung 9: ein stiller Purge ist ein
#     Betriebsproblem, kein Abbruchgrund für diese Diagnose.)
last_trigger="$(systemctl show sharefyx-purge.timer --property=LastTriggerUSec --value 2>/dev/null || true)"
if [[ -z "$last_trigger" || "$last_trigger" == "n/a" ]]; then
  echo "WARNUNG: sharefyx-purge.timer ist nie gelaufen —" \
       "sudo systemctl enable --now sharefyx-purge.timer" >&2
else
  last_epoch="$(date -d "$last_trigger" +%s 2>/dev/null || echo 0)"
  now_epoch="$(date -u +%s)"
  age_s=$(( now_epoch - last_epoch ))
  if (( last_epoch == 0 || age_s > 172800 )); then
    echo "WARNUNG: letzter Purge-Lauf ist älter als 48h ($last_trigger) —" \
         "journalctl -u sharefyx-purge -n 20" >&2
  else
    echo "INFO letzter Purge-Lauf: $last_trigger" >&2
  fi
fi

# 12) Verwaiste oder kaputte `.share.yml`-Referenzen? (P6 Step 6, DoD: "diagnose.sh meldet
#     keine verwaisten Namen". `spacectl.py check` kennt jede `.share.yml` unter DATA_ROOT und
#     benutzt denselben YAML-Parser wie `AclReader` -- kein zweiter Parser hier in Bash (§2.2,
#     V51). Braucht DATA_ROOT/VENV aus local.env wie Prüfung 5. Seit P7 Block C deckt dieselbe
#     Prüfung zusätzlich die menschliche Space-Verwaltungsfläche ab -- ein per "Spaces
#     verwalten" angelegter oder entfernter Space hinterlässt hier dieselben Spuren wie einer
#     über `spacectl.py`.)
data_root=""
venv_python=""
if [[ -f "$LOCAL_ENV" ]]; then
  # shellcheck disable=SC1090
  eval "$(set -a && source "$LOCAL_ENV" && set +a && printf 'data_root=%q\nvenv_python=%q\n' \
    "${DATA_ROOT:-}" "${VENV:-}/bin/python3")"
fi
if [[ -z "$data_root" ]]; then
  echo "WARNUNG: kein DATA_ROOT aus $LOCAL_ENV ablesbar — Prüfung 12 übersprungen." >&2
elif [[ ! -x "$venv_python" ]]; then
  echo "WARNUNG: kein venv-Python unter $venv_python gefunden — Prüfung 12 übersprungen." >&2
else
  spacectl_py="$REPO_TOP/phase6_shares/scripts/spacectl.py"
  check_json="$("$venv_python" "$spacectl_py" --data-root "$data_root" check --json 2>/dev/null || echo '{}')"
  finding_count="$(printf '%s' "$check_json" | "$venv_python" -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("orphan_count", 0) + d.get("broken_count", 0))
except Exception:
    print(-1)
' 2>/dev/null || echo -1)"
  if [[ "$finding_count" == "-1" ]]; then
    echo "WARNUNG: spacectl.py check konnte nicht ausgewertet werden — von Hand prüfen:" \
         "$venv_python $spacectl_py --data-root $data_root check" >&2
  elif [[ "$finding_count" -gt 0 ]]; then
    echo "WARNUNG: $finding_count verwaiste/kaputte .share.yml-Referenz(en) —" \
         "$venv_python $spacectl_py --data-root $data_root check" >&2
  else
    echo "INFO keine verwaisten oder kaputten .share.yml-Referenzen" >&2
  fi
fi

# 13) Gesamtgröße aller `_assets/`-Verzeichnisse und der `.git`-Verzeichnisgröße im DATA_ROOT
#     (Phase 6.5 Step B5, §4 Punkt 7 im Plan: B1 = ja, Bilder werden mitcommittet, ein
#     entferntes Bild gibt keine Bytes frei -- Git-Historie wächst monoton. B2 = 5 MiB je Bild
#     OHNE Space-Gesamtbudget heißt "messen statt deckeln", diese Prüfung ist das Messgerät.
#     INFO, kein Abbruchkriterium -- dieselbe Kategorie wie Prüfung 9/11/12. `$data_root`
#     stammt aus Prüfung 12 oben, dieselbe `local.env`-Auflösung, kein zweiter Read nötig.)
if [[ -z "$data_root" ]]; then
  echo "WARNUNG: kein DATA_ROOT aus $LOCAL_ENV ablesbar — Prüfung 13 übersprungen." >&2
elif [[ ! -d "$data_root" ]]; then
  echo "WARNUNG: DATA_ROOT $data_root existiert nicht — Prüfung 13 übersprungen." >&2
else
  assets_bytes=0
  while IFS= read -r -d '' dir; do
    dir_bytes="$(du -sb "$dir" 2>/dev/null | cut -f1)"
    assets_bytes=$(( assets_bytes + ${dir_bytes:-0} ))
  done < <(find "$data_root" -mindepth 2 -maxdepth 2 -type d -name '_assets' -print0 2>/dev/null)
  git_dir="$data_root/.git"
  if [[ -d "$git_dir" ]]; then
    git_bytes="$(du -sb "$git_dir" 2>/dev/null | cut -f1)"
  else
    git_bytes=0
  fi
  assets_human="$(numfmt --to=iec --suffix=B "${assets_bytes:-0}" 2>/dev/null || echo "${assets_bytes:-0}B")"
  git_human="$(numfmt --to=iec --suffix=B "${git_bytes:-0}" 2>/dev/null || echo "${git_bytes:-0}B")"
  echo "INFO Bild-Assets gesamt: $assets_human (_assets/ über alle Spaces) · Git-Historie: $git_human ($git_dir)" >&2
fi

echo "DIAGNOSE: alle Prüfungen bestanden." >&2
exit 0
