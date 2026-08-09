#!/usr/bin/env bash
#
# deploy.sh — baut ein neues Release-Verzeichnis, prüft es, legt den `current`-Symlink um und
# rollt bei einem gescheiterten Health-Gate von allein zurück (Plan §5 Step 8, P5-AB).
#
# Bis Step 8 lief der Dienst direkt aus dem Git-Arbeitsverzeichnis: ein Editor-Speichern wirkte
# sofort auf die laufende Instanz, und ein Rollback gab es nicht. Danach zählt nur noch, was
# deployt wurde.
#
# **Quelle ist das lokale Repo, nicht GitHub** (Nikinger-Entscheidung 2026-08-05: „von GitHub
# klonen nur Leute, die das Projekt selber hosten wollen"). Der Klon bringt die Remote-Refs mit,
# `deploy.sh origin/main` funktioniert also weiterhin — nach einem vorherigen `git fetch`.
#
# Konfiguration ausschließlich über Umgebungsvariablen, kein Literal im Skript (dasselbe Muster
# wie phase3_edge/scripts/backup_data_root.sh):
#   SHAREFYX_RELEASES_DIR   Pflicht — Verzeichnis, in dem Releases entstehen
#   SHAREFYX_CURRENT_LINK   Pflicht — der Symlink, den der Dienst benutzt
#   SHAREFYX_SOURCE_REPO    Optional, Default: das Repo, in dem dieses Skript liegt
#   SHAREFYX_KEEP_RELEASES  Optional, Default 5
#   SHAREFYX_SERVICE        Optional, Default sharefyx-mcp
#   SHAREFYX_SYSTEMCTL      Optional, Default "systemctl" — siehe unten
#   SHAREFYX_PORT           Optional, Default 8765 — siehe [SEAM] unten
#   SHAREFYX_HEALTH_TIMEOUT Optional, Default 30 (Sekunden)
#   SHAREFYX_DATA_ROOT      Optional — wenn gesetzt, Pre-Deploy-Bundle des DATA_ROOT
#   SHAREFYX_BACKUP_DIR     Pflicht, sobald SHAREFYX_DATA_ROOT gesetzt ist
#   SHAREFYX_SKIP_TESTS     Optional, "1" überspringt den pytest-Lauf im Release
#   SHAREFYX_ALLOW_STALE_UPDATELOG  Optional, "1" überspringt das Update-Log-Gate (P6-X)
#
# [SEAM] Blue/Green (P5-AC): der Zielport steht in GENAU EINER Variablen (SHAREFYX_PORT) und wird
# an GENAU EINER Stelle benutzt (der Health-Gate-Basis-URL unten). Der spätere Weg — Template-Unit
# `sharefyx-mcp@.service` plus Zielwechsel über `tailscale serve`/`funnel` — steht im Phase-Head,
# zusammen mit der Bedingung, unter der er überhaupt sinnvoll wird: ab dann müssen alle
# Schemaänderungen expand/contract-fähig sein, weil zwei Farben dieselbe `auth.sqlite3`, denselben
# Index und dasselbe Git-Repo benutzen. In dieser Phase wird das NICHT gebaut.
#
# Ausgabe: genau eine JSON-Zeile auf stdout (Hard Rule 7), aller Fortschritt auf stderr.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

GIT_REF="${1:-}"
if [[ -z "$GIT_REF" ]]; then
  echo "Aufruf: $0 <git-ref>   z.B. $0 main" >&2
  exit 1
fi

RELEASES_DIR="${SHAREFYX_RELEASES_DIR:?SHAREFYX_RELEASES_DIR muss gesetzt sein}"
CURRENT_LINK="${SHAREFYX_CURRENT_LINK:?SHAREFYX_CURRENT_LINK muss gesetzt sein}"
SOURCE_REPO="${SHAREFYX_SOURCE_REPO:-$REPO_DIR}"
KEEP="${SHAREFYX_KEEP_RELEASES:-5}"
SERVICE="${SHAREFYX_SERVICE:-sharefyx-mcp}"
# Warum konfigurierbar und nicht schlicht `systemctl`: dieses Skript MUSS als `savefyx` laufen,
# nicht als root. `/var/lib/sharefyx-backup` gehört `savefyx` (der Backup-Timer läuft unter
# diesem Konto); ein Pre-Deploy-Bundle, das root dort hineinschreibt, könnte der Timer bei seiner
# nächsten Retention nicht mehr löschen — ein Backup-Verzeichnis, das langsam vollläuft und
# niemandem auffällt. Nur der Neustart einer System-Unit braucht Rechte, und genau dieser eine
# Aufruf wird deshalb eskaliert: SHAREFYX_SYSTEMCTL="sudo systemctl".
SYSTEMCTL="${SHAREFYX_SYSTEMCTL:-systemctl}"
PORT="${SHAREFYX_PORT:-8765}"
HEALTH_TIMEOUT="${SHAREFYX_HEALTH_TIMEOUT:-30}"

BASE_URL="http://127.0.0.1:${PORT}"   # [SEAM] die einzige Stelle, die den Port benutzt

# -- 1) Pre-Deploy-Backup ---------------------------------------------------------------------
# Unabhängig vom Backup-Timer: ein Deploy ist der Moment, in dem man ein frisches Backup will,
# nicht eines von heute Nacht. Das DATA_ROOT-Bundle entsteht über das VORHANDENE Skript aus P3 —
# ein zweiter Backup-Weg wäre ein zweiter Weg, der falsch sein kann.
if [[ -n "${SHAREFYX_DATA_ROOT:-}" ]]; then
  echo "Pre-Deploy-Backup des DATA_ROOT" >&2
  SHAREFYX_DATA_ROOT="$SHAREFYX_DATA_ROOT" \
  SHAREFYX_BACKUP_DIR="${SHAREFYX_BACKUP_DIR:?SHAREFYX_BACKUP_DIR muss gesetzt sein, wenn SHAREFYX_DATA_ROOT gesetzt ist}" \
    "$REPO_DIR/phase3_edge/scripts/backup_data_root.sh" >/dev/null
else
  echo "HINWEIS: SHAREFYX_DATA_ROOT nicht gesetzt — kein Pre-Deploy-Bundle." >&2
fi

# -- 2) Release bauen -------------------------------------------------------------------------
# Zeitstempel wie in backup_data_root.sh: Mikrosekunden, keine Doppelpunkte im Pfad, bleibt
# lexikografisch sortierbar (rollback.sh verlässt sich genau darauf).
timestamp="$(date -u +%Y%m%dT%H%M%S.%6NZ)"
release="$RELEASES_DIR/$timestamp"
mkdir -p "$RELEASES_DIR"

# Ein Release, das den Gate nicht besteht, darf nicht liegenbleiben: es würde einen der KEEP
# Plätze belegen und sähe im Verzeichnis aus wie ein gültiger Rollback-Kandidat. Dieselbe
# Begründung, aus der backup_data_root.sh ein unverifiziertes Bundle löscht.
cleanup_release() {
  if [[ -n "${release:-}" && -d "$release" ]]; then
    echo "entferne unvollständiges Release: $release" >&2
    rm -rf "$release"
  fi
}

echo "klone $SOURCE_REPO -> $release" >&2
if ! git clone --no-hardlinks --quiet "$SOURCE_REPO" "$release" >&2; then
  cleanup_release
  echo "ABBRUCH: git clone fehlgeschlagen." >&2
  exit 1
fi
if ! git -C "$release" checkout --quiet "$GIT_REF" >&2; then
  cleanup_release
  echo "ABBRUCH: git ref '$GIT_REF' nicht auscheckbar." >&2
  exit 1
fi
release_sha="$(git -C "$release" rev-parse HEAD)"
echo "Release-Stand: $release_sha ($GIT_REF)" >&2

# -- 2.5) Update-Log-Gate ----------------------------------------------------------------------
# P6-X: ein Deploy ohne frischen `docs/UPDATE_LOG.md`-Eintrag darf nicht durchlaufen — sonst
# sieht ein Mensch eine funktionale Änderung (z. B. die künftige Sichtbarkeitsumstellung, P6-L)
# nie im Banner, weil niemand daran gedacht hat, den Eintrag vor dem Deploy zu schreiben. Läuft
# HIER, nicht erst nach venv/pip/pytest: ein sicher vermeidbarer Abbruch soll in Sekunden kommen,
# nicht nach dem teuersten Teil des Skripts. Liest `$release/docs/UPDATE_LOG.md` — den Checkout,
# nie die Arbeitskopie eines anderen Prozesses.
if [[ "${SHAREFYX_ALLOW_STALE_UPDATELOG:-}" != "1" ]]; then
  update_log="$release/docs/UPDATE_LOG.md"
  # `|| true`: kein Treffer (fehlende Datei, kein `##`-Datum) ist ein erwarteter Fall, den die
  # `if` unten behandelt — ohne das würde `pipefail` (`grep` liefert 1) die Zuweisung unter
  # `set -e` als Skriptfehler werten und mit einer rohen Bash-Fehlermeldung statt der eigenen
  # ABBRUCH-Zeile abbrechen.
  top_date="$(grep -m1 -E '^## [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$update_log" 2>/dev/null | sed -E 's/^## //' || true)"
  # UTC UND lokal akzeptiert: das Skript ist sonst durchgehend UTC, aber ein Deploy kurz nach
  # Mitternacht Lokalzeit liegt in UTC noch am Vortag — ein falscher Abbruch bei einem
  # legitimen, tagesaktuellen Eintrag wäre der schlechtere Fehler als eine zu großzügige Prüfung.
  today_utc="$(date -u +%F)"
  today_local="$(date +%F)"
  if [[ -z "$top_date" || ( "$top_date" != "$today_utc" && "$top_date" != "$today_local" ) ]]; then
    cleanup_release
    echo "ABBRUCH: docs/UPDATE_LOG.md trägt keinen Eintrag vom heutigen Tag (oberste Überschrift: '${top_date:-keine gefunden}', erwartet $today_utc oder $today_local). Neuen Eintrag ergänzen oder SHAREFYX_ALLOW_STALE_UPDATELOG=1 setzen." >&2
    exit 1
  fi
  echo "Update-Log aktuell: $top_date" >&2
fi

# -- 3) venv + Installation -------------------------------------------------------------------
# `scripts/dev_install.sh` DES RELEASES, nicht des Arbeitsverzeichnisses: die Paketliste gehört
# zum ausgecheckten Stand. Es nimmt alle `phase*_*/`-Pakete auf — kein zweiter Installationsweg.
echo "erzeuge venv + installiere Pakete" >&2
if ! python3 -m venv "$release/.venv" >&2; then
  cleanup_release
  echo "ABBRUCH: venv konnte nicht erzeugt werden." >&2
  exit 1
fi
if ! ( cd "$release" && PATH="$release/.venv/bin:$PATH" bash "$release/scripts/dev_install.sh" >&2 ); then
  cleanup_release
  echo "ABBRUCH: Installation der Pakete fehlgeschlagen (braucht Netz für pip)." >&2
  exit 1
fi

# -- 4) Tests im Release ----------------------------------------------------------------------
if [[ "${SHAREFYX_SKIP_TESTS:-}" == "1" ]]; then
  echo "HINWEIS: SHAREFYX_SKIP_TESTS=1 — pytest im Release übersprungen." >&2
else
  echo "pytest im Release" >&2
  if ! ( cd "$release" && "$release/.venv/bin/python" -m pytest -q >&2 ); then
    cleanup_release
    echo "ABBRUCH: Tests im Release rot — der Symlink bleibt unberührt." >&2
    exit 1
  fi
fi

# -- 5) Symlink umlegen -----------------------------------------------------------------------
previous_target=""
if [[ -L "$CURRENT_LINK" ]]; then
  previous_target="$(readlink -f "$CURRENT_LINK")"
fi

# `ln -sfn` auf einen existierenden Symlink ist unlink+symlink — dazwischen existiert kurz gar
# kein Link. `mv -T` ersetzt ihn in einem einzigen `rename()`.
tmp_link="${CURRENT_LINK}.deploy.$$"
ln -s "$release" "$tmp_link"
mv -T "$tmp_link" "$CURRENT_LINK"
echo "Symlink: $CURRENT_LINK -> $release" >&2

# -- 6) Neustart ------------------------------------------------------------------------------
echo "starte $SERVICE neu" >&2
$SYSTEMCTL restart "$SERVICE" >&2 || true

# -- 7) Health-Gate ---------------------------------------------------------------------------
# ABWEICHUNG vom Plan-Wortlaut, bewusst und dokumentiert: der Plan verlangt „eine
# authentifizierte API-Probe". Eine echte Anmeldung bräuchte Passwort UND TOTP-Seed auf der
# Platte — Hard Rule 1 verbietet das ausnahmslos. Die vier Proben unten beweisen dasselbe, ohne
# ein Geheimnis anzulegen: der Stack ist vollständig gemountet (/health, /ui/login) UND der
# Auth-Gate ist scharf (/api/v1/me ohne Cookie und /mcp/ ohne Bearer antworten 401). Ein Deploy,
# der versehentlich die Authentisierung ausbaut, fällt hier auf — genau darum ging es.
probe() {
  curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$1" 2>/dev/null || echo "000"
}

gate_ok=0
deadline=$(( SECONDS + HEALTH_TIMEOUT ))
while (( SECONDS < deadline )); do
  if [[ "$(probe "$BASE_URL/health")" == "200" ]]; then
    gate_ok=1
    break
  fi
  sleep 1
done

failed_probe=""
if (( gate_ok == 1 )); then
  for spec in "/ui/login:200" "/api/v1/me:401" "/mcp/:401"; do
    path="${spec%:*}"
    want="${spec##*:}"
    got="$(probe "$BASE_URL$path")"
    if [[ "$got" != "$want" ]]; then
      failed_probe="$path erwartet $want, erhalten $got"
      gate_ok=0
      break
    fi
    echo "OK  $path -> $got" >&2
  done
else
  failed_probe="/health kam innerhalb von ${HEALTH_TIMEOUT}s nicht auf 200"
fi

if (( gate_ok == 0 )); then
  echo "HEALTH-GATE GESCHEITERT: $failed_probe" >&2
  echo "rolle automatisch zurück" >&2
  # Beim ALLERERSTEN Deploy gibt es kein vorheriges Release; `rollback.sh` bricht dann korrekt
  # ab und diese Warnung erscheint. Das ist kein Betriebsproblem: vor dem Cutover zeigt die
  # systemd-Unit noch auf das Arbeitsverzeichnis, der Symlink ist zu diesem Zeitpunkt für den
  # laufenden Dienst bedeutungslos. Genau deshalb steht im Runbook der erste Deploy VOR dem
  # Cutover — ein erster Deploy, der schiefgeht, darf nichts umwerfen.
  SHAREFYX_RELEASES_DIR="$RELEASES_DIR" SHAREFYX_CURRENT_LINK="$CURRENT_LINK" \
    SHAREFYX_SERVICE="$SERVICE" SHAREFYX_SYSTEMCTL="$SYSTEMCTL" "$SCRIPT_DIR/rollback.sh" >/dev/null || \
    echo "WARNUNG: kein Rollback möglich (kein vorheriges Release?) — von Hand prüfen!" >&2

  # Fund beim ersten echten Probelauf dieses Skripts: ein zurückgerolltes Release bleibt liegen
  # (absichtlich — man will hineinsehen können), ist aber das JÜNGSTE Verzeichnis. Ohne diese
  # Markierung wäre es beim nächsten Rollback das Ziel: man landete auf genau dem Stand, der
  # eben nachweislich den Health-Gate gerissen hat. Das `.failed`-Suffix nimmt es aus rollback.shs
  # Kandidatenliste heraus, ohne es zu löschen.
  failed_release="${release}.failed"
  if mv -T "$release" "$failed_release" 2>/dev/null; then
    echo "Release als gescheitert markiert: $failed_release" >&2
    release="$failed_release"
  fi

  printf '{"ts":"%s","action":"deploy","result":"rolled_back","release":"%s","sha":"%s","reason":"%s"}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$release" "$release_sha" "$failed_probe"
  exit 1
fi

# -- 8) Retention -----------------------------------------------------------------------------
mapfile -t releases < <(find "$RELEASES_DIR" -mindepth 1 -maxdepth 1 -type d | sort)
count=${#releases[@]}
if (( count > KEEP )); then
  to_delete=$(( count - KEEP ))
  for ((i = 0; i < to_delete; i++)); do
    # Nie das Ziel des aktiven Symlinks löschen, auch wenn die Retention es rechnerisch träfe.
    if [[ "$(readlink -f "${releases[$i]}")" == "$(readlink -f "$CURRENT_LINK")" ]]; then
      echo "übersprungen (ist das aktive Release): ${releases[$i]}" >&2
      continue
    fi
    echo "entfernt (Retention, KEEP=$KEEP): ${releases[$i]}" >&2
    rm -rf "${releases[$i]}"
  done
fi

printf '{"ts":"%s","action":"deploy","result":"ok","release":"%s","sha":"%s","ref":"%s","previous":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" "$release" "$release_sha" "$GIT_REF" "$previous_target"
