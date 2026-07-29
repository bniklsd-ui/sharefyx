---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase3_edge/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-29 (2026-07-28-Session „Token-Rotation live bestätigt" archiviert)
---

# Session-Archiv — Phase 3 Exposure & Betrieb

## Session stopped — 2026-07-28 (Token-Rotation live bestätigt, Abschluss-Punkte erledigt)

**Für den nächsten, kalten Leser:** direkte Fortsetzung des vorigen Blocks vom 2026-07-27 —
der Nikinger hat die dort skizzierte Rotationsfolge (niklas zuerst, dann fabians Erstausgabe)
selbst ausgeführt und die Session neu geladen. Diese Session hat nur noch die Bestätigung
und den Abschluss-Aufräumschritt gemacht, keine neuen Findings.

**Was passiert ist:**
1. Der Nikinger hat alle vier Rotationsschritte (Revoke+Issue, Export, `systemd-creds
   encrypt`, `systemctl restart`) für niklas und für fabians erste reguläre Ausgabe
   ausgeführt, danach die Connector-URLs in beiden Claude-Accounts aktualisiert (neue
   Adapter-Namen: `phase_3_final_niklas_sharefyx`, `phase_3_final_sharefyx_fabian`) und die
   Session neu geladen.
2. Beide neuen Connectors live gegen `list_spaces` geprüft: niklas sieht `{fabian:
   item_count 1, writable:false}` + `{niklas: item_count 5, writable:true}`; fabian sieht
   das Spiegelbild. Rule 4 (fremd sichtbar, fremd nicht schreibbar) hält nach der Rotation
   unverändert. Für niklas ist das die geprüfte Tiefe (`list_spaces`, `writable:true` korrekt
   gesetzt); ein echter Write über den neuen niklas-Connector wurde diese Session nicht
   zusätzlich gefahren — derselbe Principal-Resolution-Pfad wie beim fabian-Write unten, aber
   nicht separat belegt.
3. `itm_2dda3690` (fabian-Testitem, zuletzt Beleg für Zeile 5) über den neuen fabian-Connector
   archiviert (`update_item`, `status: archived`, v1→v2 — ein echter Write, geprüft) — der
   temporäre `sharefyx_phase_3_fabian`-Adapter ist damit vollständig durch die reguläre Ausgabe
   ersetzt, keine offenen Wegwerf-Items mehr.

**Damit erledigt aus der „noch offen"-Liste des vorigen Blocks:** Token-Rotation aller drei
Token, Archivierung von `itm_2dda3690`, Ablösung des temporären Connectors. **Weiterhin offen,
unverändert:** Zeile 6 (Reboot, passive Beobachtung), Zeilen 12/13 (nächste Phase, siehe B5),
Zeile 14 (optional, V8 geerbt).

**Nächster Schritt (konkret):** nichts Aktives mehr für P3 — abwarten, bis ein echter Reboot
(geplant oder Vorfall) beobachtet wird, dann Zeile 6 nachtragen und `ROADMAP.md`/Phase-Head/
Index von 🟡 auf ✅ heben. Bis dahin bleibt P3 funktional beendet, aber nicht live-verifiziert
im Sinne der Statusglyphen-Definition.

## Session stopped — 2026-07-27 (zweite Session, 10/13 belegt, nur noch Reboot + zwei akzeptierte Lücken offen)

**Für den nächsten, kalten Leser:** dieser Block folgt direkt auf den vorigen vom selben Tag
(2026-07-27) — der vorige stammt aus der Session, die P3 Steps 0–6 gebaut und B3/B4 live
gefunden/behoben hat; dieser hier ist eine neue, separate Session. **Kein neuer Bug.** Zwei
Befunde (B5, B6) erklären die verbleibenden Lücken vollständig, B6 hat sich während der Session
selbst aufgelöst. Volles Protokoll mit allen Belegen: `docs/concepts/P3_ABNAHME_2026-07-27.md`.

**Was diese Session gemacht hat, in Reihenfolge:**
1. `abnahme_run.sh start` gesetzt (Startzeitpunkt für `--since`).
2. Zeile 2 (Connector niklas Read+Write) selbst über die in dieser Session verfügbaren
   MCP-Connector-Tools gefahren (`savefyx_pashe_3_test`-Adapter) — echter `get_item` +
   `append_to_item` auf dem bestehenden Testitem `itm_53cf4e92` (v1→v2), kein neues Item
   angelegt (Wiederverwendung statt Duplikat, wie vom Nikinger angewiesen).
3. Erster `abnahme_run.sh run` — Zeilen 3–5 zu dem Zeitpunkt noch nicht möglich (kein
   fabian-Connector in der Session), B6 dokumentiert.
4. **Der Nikinger hat währenddessen einen temporären Connector `sharefyx_phase_3_fabian`
   hinzugefügt** (echter fabian-Token) — nach Session-Reload sichtbar. Damit Zeilen 5→4→3
   nachgeholt (Reihenfolge zwingend eingehalten: fabian musste bei Zeile 5 noch leer sein):
   `list_spaces` (leer, fremd niklas sichtbar) → `get_item` auf ein niklas-Item (gewrappt) →
   `append_to_item`-Versuch darauf (→ `write_denied`) → `create_item` + `get_item` im eigenen
   Space (`itm_2dda3690`).
5. Zweiter `abnahme_run.sh run` — fängt alle 10 Tool-Ereignisse aus beiden Spaces im selben
   `--since`-Fenster ein, inkl. des abgelehnten Schreibversuchs.

**Ehrlicher Stand nach dieser Session** (Details + CLI-Beleg: `P3_ABNAHME_2026-07-27.md` §2/§3):

| # | Zeile | Status | Beleg |
|---|---|---|---|
| 1 | `/health` außen | ✅ | unverändert |
| 2 | Connector niklas R+W | ✅ | echter `get_item`+`append_to_item`, v1→v2 |
| 3 | Connector fabian R+W | ✅ | echter `create_item`+`get_item`, `itm_2dda3690` |
| 4 | Cross-Space | ✅ | `get_item` gewrappt, `append_to_item` → `write_denied: niklas ist nicht dein Space` |
| 5 | `list_spaces` leerer fabian | ✅ | `item_count:0`, `writable:true`, vor Zeile 3/4 geprüft |
| 6 | Reboot-Test | ⬜ | Nikinger-Zeitfrage, weiterhin offen |
| 7 | Kill-Test | ✅ | aus vorigem Block, bewusst nicht wiederholt |
| 8 | Request-Log | ✅ | 10 echte Tool-Ereignisse im Fenster, beide Spaces, inkl. `"ok":false,"err":"write_denied"` |
| 9 | Token-Grep | ✅ | Beleg aus dem 09:xx-Lauf, bewusst nicht wiederholt (kein Token in den Prozess füttern) |
| 10 | Titel-/Body-Grep | ✅ | frisch bestätigt, leer |
| 11 | Fremdzugriff → 401 | ✅ | frisch bestätigt, 2×401 |
| 12 | Backup-Timer | ⬜ **real offen, akzeptiert** | `LastTriggerUSec` leer, Timer feuert erst `2026-07-28T00:00:35`; Nikinger-Entscheidung: akzeptieren statt abwarten |
| 13 | Restore-Nachweis | ❌ **kein Bug — B5** | Skript-Check negativ, weil das einzige Bundle (11:12 UTC) älter ist als der aktuelle HEAD; per `merge-base --is-ancestor` verifiziert (reine Zeitfrage, keine divergente Historie). Mechanismus selbst war unmittelbar nach diesem Bundle bereits `status=0/SUCCESS` |

**Nebenertrag:** `[VERIFY]` **V9 live geschlossen** — der `append_to_item`-Aufruf aus Zeile 2
erzeugte exakt zeitgleich (20:39:58) den erwarteten Commit im `DATA_ROOT`, damit ist bestätigt,
dass die systemd-Sandbox (`ProtectHome=read-only` + `ReadWritePaths`) Git-Commits dort zulässt.

**B6 aufgelöst:** die anfänglich fehlende Sichtbarkeit von `fabian` im `niklas`-`list_spaces`
war keine Rule-4-Lücke, sondern eine Henne-Ei-Situation — der Space `fabian` existierte zu dem
Zeitpunkt schlicht noch nicht. Nach dem ersten `create_item` über den neuen Connector zeigt
`niklas`s `list_spaces` `fabian` korrekt als fremden Space (`item_count:1`, `writable:false`).
Rule 4 funktioniert wie entworfen, kein `tools.py`-Befund.

**Nikinger-Entscheidung 2026-07-27, 21:1x CEST:** Zeilen 6 (Reboot), 12 (Backup-Timer) und 13
(Restore-Nachweis) werden **nicht mehr aktiv nachgeholt**, sondern auf die nächste Phase
verschoben — ein unbeabsichtigter Reboot ist ohnehin der reale Prüffall für Zeile 6; 12/13
lösen sich mit dem nächsten Backup-Zyklus (B5). Damit ist die Live-Abnahme für den P3-Abschluss
funktional beendet, aber **Status bleibt 🟡, nicht ✅** — `ROADMAP.md`s Statusglyphen definieren
✅ als „live-verifiziert", und Zeile 6 ist das per Definition nicht, solange kein echter Reboot
beobachtet wurde. `ROADMAP.md` entsprechend gesetzt (2026-07-27).

**Was diese Session zusätzlich erledigt hat:**
- Testitems archiviert: `itm_53cf4e92`, `itm_cc4866f3` (beide niklas, `status=archived`).
  `itm_2dda3690` (fabian) bleibt bewusst aktiv bis nach der Token-Rotation — einziges Item im
  fabian-Space, Beleg für Zeile 5.
- Dabei ein eigener Fehler sofort korrigiert: ein `append_to_item` hatte Zeilen 9/10
  versehentlich als „nicht leer" statt „leer" protokolliert (Tippfehler beim Schreiben, kein
  tatsächlicher Befund) — im selben Item mit einer KORREKTUR-Zeile richtiggestellt, bevor
  archiviert wurde.

**Was noch offen ist, für den nächsten Schritt:**
- Zeile 6 (Reboot) — verschoben, passive Beobachtung beim nächsten echten Vorfall.
- Zeilen 12/13 — verschoben, siehe B5.
- Zeile 14 (optional, Größenbudget) — weiterhin nicht angefasst.
- **Token-Rotation aller drei Token** (niklas, fabian, und der temporäre
  `sharefyx_phase_3_fabian` — für fabian ist das die erste reguläre Ausgabe, kein Vorgänger zum
  Zurückfallen) — **führt der Nikinger aus**, Details/Befehle: README.md „Rotation im
  Dienstbetrieb", `phase3_edge/CLAUDE.md` Runbook „Abschluss". Claude Code hat keinen
  passwordless-sudo-Zugriff auf diese Shell und darf Keyring/Connector-URLs ohnehin nicht
  selbst anfassen (Hard Rule 1).
- Nach der Rotation: `itm_2dda3690` archivieren, temporären Connector entfernen/regulär
  ersetzen.
- `phase3_edge/scripts/abnahme_run.sh` bleibt unangetastet (nicht von dieser Session verfasst);
  der bekannte `SHAREFYX_BACKUP_DIR`-Default-Fehler (`/var/backups/sharefyx` statt
  `/var/lib/sharefyx-backup`) besteht im Skript weiterhin, wurde per Environment-Variable
  umgangen.

**Nächster Schritt (konkret):** Nikinger rotiert alle drei Token nach README.md-Anleitung,
aktualisiert die Connector-URLs in beiden Claude-Accounts; danach `itm_2dda3690` archivieren
und den temporären Connector entfernen. Erst nach einem beobachteten echten Reboot wechselt
P3 von 🟡 auf ✅.

---

## Session stopped — 2026-07-27 (Live-Abnahme im Gang, für kalten Leser: 8/14 belegt, keine offenen Bugs)

**Für den nächsten, kalten Leser (Mensch oder Claude): das Wichtigste zuerst.** B3 und B4 sind
**behoben und in Produktion bestätigt** — `systemctl status sharefyx-backup.service` zeigt
für **beide** `ExecStart`-Prozesse `status=0/SUCCESS`. Die drei `FEHLER`-Zeilen im letzten
`abnahme_run.sh`-Lauf (#8, #12, #13) sind **keine neuen Bugs** — sie erklären sich vollständig
aus der Art, wie der Lauf aufgerufen wurde (siehe unten). Nicht erneut debuggen, nur korrekt
aufrufen.

**Woher das kommt:** dieselbe Session hat P3 Steps 0–6 gebaut (Commits `eb2038a`…`b228bcd`),
dann live gegen die echte VM abgenommen (Commits `7368f57` B3, `d05464e` B4). Ein **zweiter,
paralleler** Claude-Chat hat `phase3_edge/scripts/abnahme_run.sh` (Test-Runner) und
`docs/concepts/P3_ABNAHME_2026-07-27.md` (Protokollvorlage) geschrieben — beide geprüft
(kein Prompt-Injection-Risiko, kein `sudo`-Missbrauch), beide noch **uncommitted**, gehören
nicht dieser Session.

**Ehrlicher Stand der 14 Abnahmezeilen** (Plan §4 Step 7 / `phase3_edge/CLAUDE.md` Runbook):

| # | Zeile | Status | Beleg |
|---|---|---|---|
| 1 | `/health` außen | ✅ | mehrfach bestätigt, `uptime_s` vorhanden |
| 2 | Connector `niklas` R+W | ✅ | `itm_53cf4e92`/`itm_cc4866f3` real angelegt — kein sauberer Einzel-Lauf-Beleg |
| 3 | Connector `fabian` R+W | ⬜ | **noch nicht gemacht** |
| 4 | Cross-Space | ⬜ | **noch nicht gemacht** |
| 5 | `list_spaces` leerer `fabian` | ⬜ | **noch nicht gemacht** |
| 6 | Reboot-Test | ⬜ | Nikinger: „noch nicht möglich" (Stand vor dieser Notiz) |
| 7 | Kill-Test | ✅ | `abnahme_run.sh --with-kill`-Lauf: „wieder gesund", `uptime_s: 4` |
| 8 | Request-Log | ✅ **funktional**, ⬜ **im Skript unbewiesen** | 3 echte `"ev":"tool"`-Zeilen direkt im Journal gefunden (`list_spaces`, 2× `create_item`) — liegen nur außerhalb des `--since`-Fensters, weil Tests 2–5 nie unmittelbar vor einem `run` gemacht wurden |
| 9 | Token-Grep | ✅ | mehrfach leer |
| 10 | Titel-/Body-Grep | ✅ | mehrfach leer |
| 11 | Fremdzugriff → 401 | ✅ | 401 + `<redacted>` im Log |
| 12 | Backup-Timer | ⬜ **echt offen** | Timer nie selbst ausgelöst (nur der Service manuell) — `LastTriggerUSec` bleibt leer, bis der Timer selbst feuert (`NEXT` laut `list-timers`: 2026-07-28 00:04:56 CEST, `RandomizedDelaySec=900`) |
| 13 | Restore-Nachweis | ✅ **mechanisch bewiesen**, Skript-Check zeigt trotzdem FEHLER | `systemctl status` zweifelsfrei `status=0/SUCCESS` für `restore_check.sh` — `abnahme_run.sh`s **eigener** Default für `SHAREFYX_BACKUP_DIR` ist noch `/var/backups/sharefyx` (alt), nicht `/var/lib/sharefyx-backup` (B3-Fix); ohne `export SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup` findet der Skript-Check das Bundle nicht — das Skript gehört nicht dieser Session, wurde bewusst nicht selbst editiert |
| 14 | Größenbudget | ⬜ | optional, noch nicht angefasst |

**Für den nächsten sauberen Lauf, in dieser Reihenfolge:**

```bash
export SHAREFYX_HOST=savefyx-vmware-virtual-platform.tail89fc2a.ts.net
export SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data
export SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup   # B3-Fix — abnahme_run.sh kennt den neuen Pfad nicht selbst
./phase3_edge/scripts/abnahme_run.sh start
# → JETZT sofort, ohne Pause: Connector-Tests 2–5 fahren (niklas UND fabian, Cross-Space,
#   list_spaces bei leerem fabian) — das füllt gleichzeitig #2–#5 UND liefert die Tool-Events,
#   die #8 im richtigen Zeitfenster braucht
sudo -E ./phase3_edge/scripts/abnahme_run.sh run --with-kill | tee /tmp/p3-abnahme.txt
```

Danach bleibt real nur noch offen: #6 (Reboot, Nikinger-Zeitfrage), #12 (Timer muss selbst
feuern — warten oder als „Mechanismus bewiesen, Zeitplan nicht" akzeptieren, siehe §4 des
Protokolls), #14 (optional). Ergebnis in `docs/concepts/P3_ABNAHME_2026-07-27.md` §3.1 kleben,
dann an diese Session zurückgeben — Abschluss (Token-Rotation, Protokoll fertigstellen,
`ROADMAP.md`/`docs/INDEX.md`/dieser Phase-Head auf ✅) ist der letzte Schritt.

**Nächster Schritt (konkret):** wie oben — sauberer Lauf, dann zurück an Claude Code für den
Abschluss.

## Session stopped — 2026-07-27 (Step 6: Runbooks, `diagnose.sh`, Cloudflare-Rückbau)

**Ergebnis:** Step 6 abgeschlossen. `phase3_edge/scripts/diagnose.sh` (sechs Prüfungen,
degradiert sauber), Runbook „Connector zeigt Disconnected" + „Cloudflare-Rückbau" +
„Inbetriebnahme"-Platzhalter im Phase-Head. `phase2_mcp/CLAUDE.md`s Quick-Tunnel-Runbook durch
einen Verweis ersetzt.

**`diagnose.sh` real auf dieser VM gelaufen (read-only, kein Schreibzugriff):** Ergebnis —
Prüfung 1 (`systemctl is-active sharefyx-mcp`) schlägt korrekt fehl, weil die Unit hier noch
nicht installiert ist (Step 7). Ausgabe: `DIAGNOSE: sharefyx-mcp ist nicht aktiv (oder nicht
installiert). NÄCHSTER SCHRITT: journalctl -u sharefyx-mcp -n 50`, Exit 1. Das ist ein
korrekter, sauberer Abbruch — **nicht** das im Plan beschriebene „läuft durch, auch mit
absichtlich gestopptem Dienst" (dafür bräuchte es einen tatsächlich laufenden und dann gestoppten
Dienst). Die vollständige Prüfung aller sechs Schritte gegen einen echten, installierten Dienst
verschiebt sich damit explizit nach Step 7 — hier festgehalten, nicht stillschweigend als „Done"
gemeldet.

**`[VERIFY]` neu, benannt statt verschwiegen:** Prüfung 4s Grep-Muster gegen
`tailscale funnel status` (`"127.0.0.1:8765"`) beruht auf Tailscales dokumentiertem
Ausgabeformat, war aber auf dieser VM nie gegen ein echtes Tailscale zu verifizieren (Tailscale
fehlt seit Step 0). Erster echter Test in Step 7; bei Abweichung `diagnose.sh` dort korrigieren,
nicht den Fund hier überschreiben.

**Check 6s Grep-Muster (`'"status":401'`) passt zum echten `AccessLogASGI`-Output** — geprüft
gegen `request_log.py`s kompaktes `json.dumps(..., separators=(",", ":"))` (kein Leerzeichen
nach dem Doppelpunkt), nicht nur angenommen.

**Cloudflare-Rückbau ist ein Runbook-Eintrag, keine ausgeführte Aktion (Advisor-Vorgabe,
dieselbe Klasse wie `install_units.sh`):** `cloudflared` ist auf dieser VM installiert
(Step 0 C), aber die Deinstallation ist destruktiv und außerhalb des Repos — der Befehl steht im
Phase-Head-Runbook, der Nikinger führt ihn selbst aus.

**`phase2_mcp/CLAUDE.md` — Quick-Tunnel-Runbook ersetzt, nicht gelöscht:** die historischen
Abschnitte „Live-Stand"/„Sicherheitsvorfall" standen bereits vollständig in
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` und im archivierten P2-Step-7-Session-Block
(`phase2_mcp/SESSIONS_ARCHIVE.md`) — kein Informationsverlust durch das Kürzen. Die
Überschrift behält bewusst den Wortlaut „Quick-Tunnel-Probe", damit der bestehende Verweis
weiter oben im selben Dokument („Runbook „Quick-Tunnel-Probe" oben") gültig bleibt, statt eine
zweite Textstelle mitziehen zu müssen. Ersetzt durch einen dreiteiligen Verweis (P2-Nachweis,
P3-Betriebsweg, Verweis `phase3_edge/CLAUDE.md`) plus einem eigenen Absatz zu Cloudflare Named
Tunnel als dokumentiertem Ausweichweg — wie im Plan gefordert.

**Größenänderung:** `phase2_mcp/CLAUDE.md` von ~23KB auf ~19KB (Kürzung um die Cloudflare-
Voraussetzungen), `docs/INDEX.md`-Zeile nachgezogen.

**Tests:** keine neuen — Plan sieht für Step 6 keine automatisierten Tests vor (Runbook-Text und
ein Bash-Skript, das gegen eine echte Infrastruktur läuft). `.venv/bin/python -m pytest -q` →
**168/168 grün**, unverändert gegenüber Step 5 (Kontrollzahl, keine Regression durch die
Doku-Änderungen).

**Modul-Status oben nachgezogen** (Zeile 7: ⬜ → ✅, 0 Tests — begründet).

**Offen für den Nikinger, vor Step 7 zu klären (Zusammenfassung, unverändert seit früheren
Steps, hier gebündelt vor dem Abschlussbericht):**
1. `mcp_smoke.py`/P3-N-Grenzfrage (Step 2) — `logging.basicConfig` → `configure_logging`
   umstellen oder nicht.
2. Tailscale-Installation + Tailnet-Voraussetzungen (Step 0) — einziges echtes Gate vor Step 7.
3. Cloudflare-Rückbau (dieser Step) — Befehl steht im Runbook, Ausführung ist Sache des
   Nikingers.

**Nachtrag zu diesem Block (Advisor-Fund, nach dem ursprünglichen Commit ergänzt):** der
„Inbetriebnahme"-Runbook-Abschnitt oben war noch der leere Platzhalter aus Step 0/1 —
nachgezogen mit der vollständigen Befehlsfolge und der 14-Zeilen-Abnahmematrix aus Plan §4
Step 7, angepasst an das tatsächlich Gebaute (vier `local.env`-Variablen, zwei Backup-Units,
`diagnose.sh` als Vorab-Check vor Schritt 7). Ohne diese Ergänzung hätte der Nikinger für Step 7
den 46KB-Plan öffnen müssen, obwohl der Phase-Head genau dafür da ist. Reine Doku-Ergänzung,
kein Code, keine neuen Tests — `pytest` bleibt bei 168/168.

**Nächster Schritt (konkret):** Step 7 — Live-Abnahme. Läuft komplett beim Nikinger gegen die
echte Infrastruktur; Claude Code liefert die Befehlsfolge aus dem Plan und wertet die
Ergebnisse aus, führt aber nichts davon selbst aus (echter `DATA_ROOT`, echter Keyring, echte
Token, echte Claude-Accounts).

**[2026-07-27, während der Live-Abnahme] Fund B3, behoben — `sharefyx-backup.service` scheiterte
real auf der VM:** `mkdir: cannot create directory '/var/backups/sharefyx': Permission denied`.
Ursache: der Dienst läuft als unprivilegierter `User=savefyx`; `/var/backups` gehört auf
Debian/Ubuntu root und ist für andere Nutzer nicht beschreibbar. Kein Unit-Test hat das
gefangen, weil `test_units.py` reines Textparsen ist und nie einen echten systemd-Prozess unter
echtem `User=`-Sandbox startet — genau die Klasse Fund, die laut Plan nur unter echter
Infrastruktur (V9-Nachbarschaft) sichtbar wird.

**Behoben:** `phase3_edge/systemd/sharefyx-backup.service` benutzt jetzt `StateDirectory=
sharefyx-backup` statt eines literalen `/var/backups/sharefyx`. systemd legt
`/var/lib/sharefyx-backup` bei **jedem** Start selbst an, bereits mit der richtigen
Eigentümerschaft (`User=`/`Group=` des Dienstes) — kein manuelles `chown`, auf keiner Maschine,
jemals nötig (dieselbe Maschinenunabhängigkeits-Logik wie bei den vier `local.env`-Variablen).
`SHAREFYX_BACKUP_DIR` zeigt entsprechend jetzt auf `/var/lib/sharefyx-backup` statt
`/var/backups/sharefyx` — `/var/lib` ist ohnehin die FHS-korrekte Konvention für
dienst-verwaltete Zustandsdaten, `/var/backups` eher für administrator-initiierte Backups mit
Root-Rechten gedacht.

**Auf der VM anzuwenden:** `sudo phase3_edge/scripts/install_units.sh` erneut laufen lassen
(re-templated die Unit, `daemon-reload`, `sharefyx-mcp` erneut `enable --now` — unschädlich,
bereits laufend), danach `sudo systemctl start sharefyx-backup.service` erneut versuchen.

**Nebenbefund, nicht behoben (gehört nicht mir):** `phase3_edge/scripts/abnahme_run.sh` — vom
Nikinger über eine parallele Claude-Sitzung geschrieben, nicht Teil dieser Session — hat
weiterhin `/var/backups/sharefyx` als Default für `SHAREFYX_BACKUP_DIR` (Zeile 27). Beim nächsten
Lauf `SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup` explizit exportieren, sonst findet Test 13
das neue Bundle nicht. Bewusst nicht eigenmächtig editiert — das Skript gehört einer anderen
Sitzung, die den Nikinger direkt informiert bekommt.

**Tests:** keine Änderung nötig, `.venv/bin/python -m pytest -q` → weiterhin **168/168 grün**
(kein Test prüfte den literalen Pfadwert, nur Secret-Shape und `/home/savefyx`-Freiheit).

**[2026-07-27, dieselbe Live-Abnahme] Fund B4, behoben — nächster Fehlschlag, nachdem B3 den
Weg freigemacht hatte:** `backup_data_root.sh` erstellte das Bundle jetzt korrekt (B3-Fix
funktioniert), scheiterte aber bei der Verifikation:
`error: need a repository to verify a bundle`. Ursache: `git bundle verify "$bundle"` lief ohne
`-C`/`--git-dir` — `git bundle verify` braucht zwingend eine Repo-Umgebung zum Dispatchen (auch
ohne externe Prerequisites zu prüfen), und ohne `WorkingDirectory=` im Unit ist das
Arbeitsverzeichnis unter systemd `/`, kein Git-Repo. `git bundle create` (Zeile davor) hatte
bereits korrekt `-C "$DATA_ROOT"` — die `verify`-Zeile war die einzige Lücke.

**Warum kein Test das gefangen hat, obwohl `test_backup_creates_verifiable_bundle` genau diesen
Pfad prüft:** `subprocess.run(["bash", str(BACKUP_SCRIPT)], ...)` ohne `cwd=` erbt pytests
eigenes Arbeitsverzeichnis — und das ist zufällig dieses Repo selbst, also zufällig ein
Git-Repo. Der Test bestand, weil der Testkontext unbeabsichtigt genau die Bedingung lieferte,
die unter systemd fehlt. Klassischer „bestanden aus Zufall, nicht aus Korrektheit"-Fall.

**Behoben, zweifach (Skript + Unit, nicht nur eins von beiden):**
- `backup_data_root.sh`: `git bundle verify` → `git -C "$DATA_ROOT" bundle verify` — die
  eigentliche Korrektur, unabhängig von jeder Unit-Konfiguration richtig.
- `phase3_edge/systemd/sharefyx-backup.service`: `WorkingDirectory=__REPO_ROOT__` ergänzt
  (fehlte bisher, `sharefyx-mcp.service` hat es bereits) — Verteidigung in der Tiefe, falls ein
  künftiges Skript in dieser Unit denselben Fehler macht.
- **Testlücke geschlossen, nicht nur der Bug:** alle `subprocess.run`-Aufrufe in
  `test_backup_scripts.py`, die die Skripte direkt starten, laufen jetzt mit `cwd="/"` —
  reproduziert exakt die systemd-Realität ohne `WorkingDirectory=`, statt sich auf das
  zufällige Repo-cwd von pytest zu verlassen. Der Fake-`git`-Wrapper im
  Korruptions-Test musste dafür von einer festen `$1`/`$2`-Positionsprüfung auf einen
  Substring-Check (`"bundle verify"` irgendwo in `"$*"`) umgestellt werden, weil `-C
  "$DATA_ROOT"` jetzt vor `bundle verify` steht.

**Tests:** `.venv/bin/python -m pytest -q` → **168/168 grün**, `test_backup_scripts.py` einzeln
gegen `cwd="/"` gegengeprüft (alle sieben grün) — die Testverschärfung selbst wurde vor dem Fix
kurz gegen den ungefixten Stand laufen lassen und schlug dort korrekt fehl (Beweis, dass sie den
echten Fehler jetzt fängt), nicht nur behauptet.

## Session stopped — 2026-07-27 (Step 5: Backup und Restore-Nachweis)

**Ergebnis:** Step 5 abgeschlossen. `backup_data_root.sh` (git bundle + Verify + Retention),
`restore_check.sh` (Klon + HEAD/Tree-Vergleich), `sharefyx-backup.service`/`.timer` (Platzhalter,
nicht installiert — Step 7).

**`git bundle create` schlägt auf einem leeren Repo fehl** ("Refusing to create empty bundle") —
jede Testfixture (`data_root`) legt deshalb einen echten Commit an, nicht nur ein leeres
`git init`.

**Zeitstempel-Kollisionsfalle umgangen, nicht nur vermieden (Advisor-Fund, dieselbe Klasse Fehler
wie `mcp_smoke.py` in P2, siehe archivierter Step-7-Block):** `test_backup_retention_keeps_newest_n`
läuft das Skript **nicht** in einer Schleife (bei Sekundenauflösung würden mehrere Bundles
denselben Dateinamen bekommen und sich überschreiben). Stattdessen legt der Test fünf Fake-Bundles
mit distinktem, sortierbarem Namen vor und ruft das Skript nur einmal für das echte, aktuelle
Bundle auf. Der Dateiname selbst trägt jetzt zusätzlich Mikrosekunden (`%6N`, keine Doppelpunkte)
statt nur Sekunden — doppelte Absicherung für den Fall eines künftigen Schleifen-Aufrufs.

**`test_backup_fails_and_cleans_up_on_corrupt_bundle` — echte Korruption, nicht simuliert
(Advisor-Vorschlag umgesetzt):** ein frisch geschriebenes, gültiges Bundle besteht die eigene
`git bundle verify` selbstverständlich. Der Test schiebt stattdessen einen Fake-`git`-Wrapper vor
den echten auf `$PATH`, der `bundle verify` immer mit Exit 1 abbrechen lässt und alles andere an
das echte `git` durchreicht — prüft damit den tatsächlichen Cleanup-Zweig (`rm -f` + Exit ≠ 0),
nicht nur seine Absicht.

**`git bundle verify` schreibt die Ref-Liste auf stdout, die Bestätigung auf stderr** (empirisch
geprüft, nicht angenommen) — im Skript deshalb explizit `>&2` umgeleitet, sonst hätte Hard Rule 7
(stdout nur maschinenlesbares JSON) auf einem Zwischenschritt gebrochen, den der Plan nicht
erwähnt.

**`SHAREFYX_BACKUP_DIR` ist Konfiguration im Skript (Umgebungsvariable, kein Literal), aber ein
fester Wert in der Unit** (`/var/backups/sharefyx`, Plan §4 Step 5 "Ziel ist Konfiguration ...,
kein Literal im Skript"). Bewusst **kein** fünfter Platzhalter/`local.env`-Eintrag: anders als
`REPO_ROOT`/`DATA_ROOT` ist ein Backup-Zielverzeichnis kein Wert, der zwischen Maschinen
tatsächlich variieren muss — ein FHS-üblicher Pfad reicht, ohne `install_units.sh` und
`local.env.example` um eine fünfte Variable zu erweitern.

**`install_units.sh` unverändert lauffähig für die neuen Units:** es verarbeitet generisch alle
`*.service`/`*.timer` in `phase3_edge/systemd/` (so in Step 4 vorbereitet) — die zwei neuen
Backup-Units laufen ohne Skriptänderung durch dieselbe Platzhalter-Ersetzung und
Unresolved-Placeholder-Prüfung.

**`test_units.py` (Step 4) erweitert, nicht dupliziert:** zwei neue Tests
(`test_all_units_have_no_secret_shaped_value`, `test_all_units_have_no_hardcoded_machine_paths`)
laufen über **alle** Unit-Dateien im Verzeichnis, nicht nur die MCP-Unit — sonst hätte die
Token-Klartext-Versicherung aus Step 4 die beiden neuen Backup-Units stillschweigend
ausgenommen.

**Tests** (`phase3_edge/tests/test_backup_scripts.py`, alle sieben aus dem Plan, gegen
Wegwerf-Git-Repos unter `tmp_path`, nie den echten `DATA_ROOT`): `test_backup_creates_verifiable_bundle`,
`test_backup_emits_single_json_line_on_stdout`, `test_backup_retention_keeps_newest_n`,
`test_backup_fails_and_cleans_up_on_corrupt_bundle`, `test_restore_check_matches_head_and_tree`,
`test_restore_check_detects_divergence`, `test_scripts_have_no_hardcoded_paths`. Plus zwei in
`phase3_edge/tests/test_units.py` (siehe oben).

**Verifiziert:** `.venv/bin/python -m pytest -q` → **168/168 grün** (159 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 6: ⬜ → ✅, 9 Tests).

**Offen für den Nikinger, weiterhin unverändert:**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2.
2. Tailscale ist auf dieser VM weiterhin nicht installiert — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 6 — Runbooks, `diagnose.sh`, Cloudflare-Rückbau. Der
Cloudflare-Uninstall selbst ist ein Befehl **für den Nikinger** (destruktive Aktion auf der
realen Maschine, außerhalb des Repos) — Claude Code liefert nur den Runbook-Text, führt ihn
nicht aus.

## Session stopped — 2026-07-27 (Step 4: systemd-Units)

**Ergebnis:** Step 4 abgeschlossen. `phase3_edge/systemd/sharefyx-mcp.service` (Platzhalter,
nicht auf der VM installiert), `phase3_edge/scripts/install_units.sh`, plus `/health` trägt jetzt
`uptime_s` (P3-I).

**`uptime_s` war im Plan §4 keinem Step zugewiesen — Lücke geschlossen, nicht stillschweigend
übersprungen (Advisor-Fund):** P3-I ("genau ein neues Feld") steht in §0.5, §1.1 und in Step 7s
Abnahmematrix (Zeile 1), aber in keinem der Steps 0–7 als Liefergegenstand. Step 6
(`diagnose.sh`, Prüfung 2) und der Disconnected-Runbook setzen das Feld aber voraus. Hier in
Step 4 gebaut, bevor Step 6 es braucht: `app.py :: create_app()` setzt `app.state.start_time =
time.monotonic()` **pro App-Instanz** (nicht Modulebene — sonst teilten sich mehrere
`create_app()`-Aufrufe, z. B. in Tests, einen Startzeitpunkt), `_health()` berechnet
`uptime_s = int(time.monotonic() - request.app.state.start_time)`. `app.py` steht in P3-Ns
Berührungsliste, keine Scope-Erweiterung.

**`test_health_ok` aus P2 korrekt rot geworden, wie von seinem eigenen Kommentar angekündigt:**
der Test prüft absichtlich die exakte Schlüsselmenge der `/health`-Antwort ("fängt eine spätere
Erweiterung um ein zusätzliches Feld ab"). Mit `uptime_s` dazu aktualisiert
(`{"status","service","version","uptime_s"}`), `isinstance(..., int)` und `>= 0` geprüft.
`test_health_leaks_no_space_names` bleibt unverändert grün — `uptime_s` leakt nichts.

**`local.env.example` trug echte Maschinenpfade dieser VM — korrigiert (Advisor-Fund):**
`REPO_ROOT`/`DATA_ROOT`/`VENV` zeigten auf `/home/savefyx/...`. P3-Js eigene Begründung für das
Platzhalterschema ist Maschinenunabhängigkeit ("der Kollege oder eine zweite VM sollen dasselbe
Repo benutzen können"), und §5 Akzeptanzkriterium 8 nennt „kein Maschinenzustand im Repo" — ein
kopiertes Beispiel mit dieser VMs echten Pfaden hätte plausibel, aber falsch ausgesehen. Jetzt
`/path/to/savefxy` etc.

**`install_units.sh` bricht vor jedem `/etc`- oder `systemctl`-Zugriff ab, wenn `local.env`
fehlt** — genau der Pfad, den der Test ausübt, ohne root-Rechte oder einen echten systemd
anzufassen. Verarbeitet generisch alle `*.service`/`*.timer` in `phase3_edge/systemd/` (Step 5
liefert die Backup-Units in dasselbe Verzeichnis, ohne dass dieses Skript sich ändern muss),
prüft nach der Platzhalter-Ersetzung per Regex, ob `__[A-Z_]+__` noch irgendwo übrig ist, und
löscht eine unvollständige Zieldatei sofort statt sie stehen zu lassen. **Die Unit ist nach
diesem Step bewusst noch nicht auf der VM installiert** — das ist Step 7.

**`V9` (`ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT`) bleibt
offen** — laut Plan nur zur Laufzeit prüfbar, `test_units.py` ist reines Textparsen. Der bereits
in Step 0 bestätigte Fund (Git-Identität `Space Server`/`space-server@localhost` liegt im
`DATA_ROOT` selbst, nicht nur in `~/.gitconfig`) ist der Ausgangspunkt für den ersten
Write-Test in Step 7 — dorthin verschoben, nicht hier vorweggenommen.

**Tests** (`phase3_edge/tests/test_units.py`, alle sechs aus dem Plan):
`test_unit_restarts_on_failure`, `test_unit_loads_credential_encrypted`,
`test_unit_binds_loopback_only`, `test_unit_has_no_secret_shaped_value`,
`test_unit_placeholders_are_unresolved_in_repo`,
`test_install_script_refuses_without_local_env` (kopiert `scripts/`+`systemd/` in ein
Wegwerf-Verzeichnis ohne `local.env` — hermetisch, unabhängig davon, ob auf dieser Maschine
zufällig ein echtes `phase3_edge/local.env` existiert). Plus die aktualisierten
`test_health_ok`/-Assertions in `phase2_mcp/tests/test_app.py`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **159/159 grün** (153 + 6 neue).

**Modul-Status oben nachgezogen** (Zeile 5: ⬜ → ✅, 6 Tests).

**Offen für den Nikinger (nicht blockierend für Steps 5–6, aber noch nicht gemeldet):**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2 — ob `mcp_smoke.py` auf `configure_logging()`
   umgestellt werden soll (Zweizeiler), steht weiterhin offen.
2. Tailscale ist auf dieser VM weiterhin nicht installiert (Step 0) — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 5 — Backup- und Restore-Skripte (`git bundle` + Verify +
Retention), Backup-Timer. Beide Skripte laufen in Tests ausschließlich gegen Wegwerf-Git-Repos
unter `tmp_path`, nie gegen den echten `DATA_ROOT`.

## Session stopped — 2026-07-27 (Step 3: Credentials über systemd)

**Ergebnis:** Step 3 abgeschlossen. `credentials.py :: load_space_map()` liest jetzt zuerst ein
von systemd bereitgestelltes Credentials-Verzeichnis, Keyring bleibt Fallback.
`phase3_edge/scripts/export_space_map.py` (neu) exportiert die Space-Map aus dem Keyring als
JSON auf stdout, für `systemd-creds encrypt`.

**`[VERIFY]` V4 und V5 — bereits in Step 0 beantwortet, hier nur referenziert (kein zweiter
Inventarlauf):** V4 (`systemd-creds` vorhanden, systemd 255 ≥ 250, `has-tpm2` → partial →
Host-Key-Verschlüsselung) und V5 (`keyring.backends.SecretService.Keyring`, Priorität 5) stehen
im „Umgebungsstand"-Abschnitt oben und in `SESSIONS_ARCHIVE.md`, Step-0-Block.

**Plan §2.3 war mit sich selbst im Widerspruch — aufgelöst, nicht stillschweigend
weggelesen:** der Plantext sagt, `export_space_map.py` solle
„`credentials.load_space_map()` **aus dem Keyring** (explizit, nicht über die neue
Verzweigung)" lesen — aber `load_space_map()` **ist** ab diesem Step die neue Verzweigung, ein
Aufruf kann nicht zugleich sie selbst und ihre Umgehung sein. Auflösung (Advisor-Review): die
reine Keyring-Leselogik wurde in eine eigene Funktion `load_space_map_from_keyring()`
ausgelagert. `load_space_map()` ruft sie als Fallback; `export_space_map.py` ruft sie direkt.
Ein Leser, zwei Aufrufer, keine Verzweigung im Export-Pfad. `issue()`/`revoke()` bleiben laut
Plan-Vorgabe **unverändert** (0 Zeilen Diff) und rufen weiterhin `load_space_map()` auf — das ist
unschädlich, weil `$CREDENTIALS_DIRECTORY` in ihrem einzigen realen Aufrufkontext
(`issue_token.py`, interaktiv) nie gesetzt ist.

**Der Fallback-Warnhinweis geht auf den Modul-Logger, nicht auf `sharefyx.request`**
(Advisor-Fund): fehlt die Credential-Datei trotz gesetztem Verzeichnis, loggt `load_space_map()`
über `logging.getLogger(__name__)` — landet also auf dem normalen stderr-Handler aus
`configure_logging()`, nicht im JSON-Request-Log. Der Request-Logger ist laut Plan §3.1 für
`ev="tool"`/`ev="http"` reserviert; eine freie Textmeldung dort wäre zwar gültiges JSON
(`JsonLineFormatter` serialisiert auch einen bloßen String), aber strukturell falsch auf einem
Stream, dessen Vertrag eine Feld-Whitelist ist.

**Test-Ladepfad für `export_space_map.py` (Advisor-Fund):** `phase3_edge/` ist kein Python-Paket
(Plan §1.2), ein normaler `import` aus `phase2_mcp/tests/test_credentials.py` funktioniert
deshalb nicht. Geladen über `importlib.util.spec_from_file_location(...)` gegen den absoluten
Pfad — hält `capsys` für den stdout/stderr-Split nutzbar, im Unterschied zu einem
Subprocess-Aufruf. Da `export_space_map.py`s `from mcpserver import credentials` denselben
gecachten Modul-Objekt-Namen trifft wie der Testcode, wirkt der `fake_keyring`-Monkeypatch aus
`test_credentials.py` transparent auch dort — kein zweiter Fake nötig.

**Doku:** `README.md`, Abschnitt „Token ausgeben, rotieren, widerrufen" um „Rotation im
Dienstbetrieb (ab P3)" erweitert — der volle Vierschritt aus P3-M (Token neu ausgeben → Export →
`systemctl restart` → Connector-URL aktualisieren), inklusive des Satzes, dass ein vergessener
Restart wie „Connector kaputt" aussieht, aber ein 401 auf die alte Credential-Datei im tmpfs ist.

**Tests** (`phase2_mcp/tests/test_credentials.py`, alle sechs aus dem Plan, mit `monkeypatch`
auf `$CREDENTIALS_DIRECTORY` und dem bestehenden `fake_keyring`-Fixture — nie der echte
Keyring): `test_load_space_map_prefers_credentials_dir`,
`test_load_space_map_falls_back_when_credentials_dir_unset`,
`test_load_space_map_falls_back_when_credential_file_missing`,
`test_load_space_map_raises_on_malformed_credential`,
`test_export_writes_json_to_stdout_and_note_to_stderr`,
`test_export_contains_no_plaintext_token`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **153/153 grün** (147 + 6 neue). Alle
bestehenden `test_credentials.py`-Tests (die alte `load_space_map()`-Aufrufe machen) liefen
unverändert grün weiter — `$CREDENTIALS_DIRECTORY` ist in der Testumgebung nie gesetzt, der
Fallback greift transparent.

**Modul-Status oben nachgezogen** (Zeile 4: ⬜ → ✅, 6 Tests).

**Nächster Schritt (konkret):** Step 4 — systemd-Units (`sharefyx-mcp.service`,
`install_units.sh`). `test_unit_has_no_secret_shaped_value` ist die billigste Versicherung gegen
den Token-Klartext-Vorfall, der in P2 zweimal passiert ist.

## Session stopped — 2026-07-27 (Step 2: Request-Log)

**Ergebnis:** Step 2 abgeschlossen. `mcpserver/request_log.py` (neu) liefert beide Ereignisarten
aus Plan §3; `ToolCallLogMiddleware` läuft in `create_app()`, `AccessLogASGI` in `serve.py`.

**`[VERIFY]` V3 aufgelöst, gegen den echten `fastmcp==3.4.4`-Code, nicht nur die Doku geprüft:**
`Middleware.on_call_tool(context: MiddlewareContext[CallToolRequestParams], call_next)`,
`context.message.name` trägt den Tool-Namen, Registrierung über `mcp.add_middleware(...)` in
`app.py :: create_app()` — alles wie im Plan angenommen. **Eine Abweichung vom Plan-Wortlaut,
empirisch begründet:** `request_log.py`s Moduldocstring-Skizze nennt `ERROR_CLASSES:
dict[type[Exception], str]`. Das ist mit dem echten `FastMCP.call_tool()`-Pfad nicht umsetzbar —
gelesen bis in `server.py`: die Middleware-Kette ruft die Kernlogik über `call_next()` auf, und
jede dort erhobene `FastMCPError`/`ToolError` (`ToolError` erbt von `FastMCPError`) wird
unverändert weitergereicht. `tools.py :: map_storage_error()` hat die ursprüngliche
`storage`-Exception zu diesem Zeitpunkt bereits in eine `ToolError` mit Präfix-Text übersetzt
(`"conflict: …"`, `"item_not_found: …"`, …) — ein Typ-Dict würde hier immer denselben einen Typ
treffen. `classify_error()` parst deshalb den Nachrichtenpräfix vor dem ersten `":"` statt den
Exception-Typ zu prüfen. Volle Begründung im Moduldocstring von `request_log.py`.

**`space`-Feld — Semantik bewusst festgelegt, nicht nur implizit:** `_current_space()` liefert
den **authentifizierten Aufrufer** (`Principal.space`), nicht den Zielraum des Tool-Aufrufs. Bei
`get_item`/`update_item` gegen einen fremden Space steht im Log also weiterhin der eigene Space,
nicht der fremde. Das beantwortet Plan §3.4 Frage 2 ("mein Account oder der des Kollegen?")
korrekt; für einen Rule-4-Nachweis (wer hat wohin geschrieben) ist das Request-Log bewusst nicht
die Quelle — das leisten die Tool-Fehlerklasse (`write_denied`) und `test_tools.py`/`test_app.py`
(Advisor-Fund, sonst hätte ein kalter Leser beim Debuggen einer Cross-Space-Ablehnung den
Zielraum im Log vermutet).

**`err: "internal"` ist ein Sammelbecken, nicht nur der Whitelist-Fallback — festgehalten für
Step 7:** die Whitelist (`conflict`, `item_not_found`, `write_denied`, `invalid`) lässt
`auth_error`, `space_not_found` und FastMCPs generisches `"Error calling tool …"` alle in
`internal` fallen. Das ist Plan-konform, bedeutet aber: `err: "internal"` in `journald` kann
sowohl „ungültiger Token mitten im Aufruf" als auch „echter Store-Bug" heißen. Kein Blocker für
P3 (keine Abnahmezeile hängt an der Unterscheidung), aber falls Step 7 auf `internal`-Zeilen
stößt, ist das der erste Ort zum Nachschauen, nicht ein Bug im Logging.

**`TokenScrubbingFilter` erweitert** (`logging_setup.py`, im P3-N-Berührungsbereich): scrubbt
jetzt auch String-Werte innerhalb eines Dict-`record.msg` (vorher nur reine String-Messages) —
sonst wäre der Filter auf dem Request-Log-Pfad ein stiller No-op gewesen, praktisch redundant zu
`AccessLogASGI`s eigener Pfad-Redaktion, aber echte Verteidigung in der Tiefe statt einer
Behauptung. Eigener Test in `test_logging.py`
(`test_scrubbing_filter_redacts_token_in_dict_message`), da die P3-Tests den Filter nicht über
`configure_logging()` einbinden.

**Zirkelimport vermieden:** `request_log.py` importiert `_TOKEN_SEGMENT_RE` aus
`logging_setup.py` auf Modulebene; `logging_setup.py :: configure_logging()` importiert
`JsonLineFormatter`/`LOGGER_NAME` aus `request_log.py` **lazy** (innerhalb der Funktion) — zum
Aufrufzeitpunkt ist `logging_setup` bereits vollständig geladen, kein Zirkelbezug beim
Modul-Import.

**`mcp_smoke.py` bewusst nicht angefasst — P3-N-Grenzfall, an den Nikinger gemeldet:** Step 2s
„Done when" verlangt einen manuellen `mcp_smoke.py`-Lauf mit sichtbaren JSON-Zeilen. `mcp_smoke.py`
ruft aber `logging.basicConfig()` statt `configure_logging()` und geht nie durch `serve.py`
(reines In-Process-`ASGITransport`, kein `AccessLogASGI`) — selbst mit funktionierendem
Tool-Log wäre die Ausgabe ein Python-Dict-Repr, kein JSON. `mcp_smoke.py` steht nicht in P3-Ns
„genau anfassen"-Liste; sie ist als abschließende Aufzählung gelesen worden (wie schon bei
`tools.py`/`server.py`), deshalb keine Änderung dort. Stattdessen manuell gegen ein Wegwerf-Skript
(nie eingecheckt, aus dem Scratchpad gelöscht) verifiziert, das genau den echten Produktionspfad
fährt — `configure_logging()` + `create_app()` + `AccessLogASGI`, `FakeResolver` statt echtem
Keyring, temporäres `DATA_ROOT`: `GET /health` und ein Fremdzugriff mit falschem Token erzeugten
korrekt geformte, redigierte JSON-Zeilen auf stderr (`{"ts":"…","ev":"http","method":"GET",
"path":"/health","status":200,"ms":0}` bzw. mit `path":"/mcp/<redacted>","status":401`). Das ist
strengeres Beweismaterial als `mcp_smoke.py` liefern könnte, weil es den echten `serve.py`-Pfad
inklusive `AccessLogASGI` prüft, den `mcp_smoke.py` konstruktionsbedingt nie durchläuft. Für den
Nikinger: falls `mcp_smoke.py` künftig JSON-Request-Logs zeigen soll, ist das eine bewusste
P3-N-Erweiterung (ein Zweizeiler: `logging.basicConfig` → `configure_logging`), keine
Kleinigkeit, die einfach nachgezogen wird.

**Tests** (alle acht aus dem Plan, `phase2_mcp/tests/test_request_log.py`, plus einer in
`test_logging.py` für die Filter-Erweiterung): `test_json_line_is_valid_json`,
`test_tool_event_has_tool_space_and_duration`, `test_tool_event_error_carries_class_not_message`,
`test_tool_event_never_contains_item_title` (gestärkt gegen eine Tautologie-Falle — prüft jetzt
zuerst `len(tool_events) == 6`, bevor die Abwesenheit des Markers behauptet wird; Advisor-Fund:
sonst wäre der Test identisch grün gegen eine Middleware geblieben, die gar nichts loggt),
`test_http_event_redacts_token_segment`, `test_http_event_logs_401_status`,
`test_logging_failure_does_not_break_tool_call`, `test_request_logger_does_not_propagate_to_root`,
`test_scrubbing_filter_redacts_token_in_dict_message`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **147/147 grün** (138 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 3: ⬜ → ✅, 9 Tests). Rotation läuft nach diesem Commit.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` LoadCredential-Pfad,
`export_space_map.py`. Alle Tests mit `monkeypatch` auf `$CREDENTIALS_DIRECTORY` und einem
Fake-Keyring, nie der echte Keyring.

## Session stopped — 2026-07-27 (Step 1: Gerüst und `SPACE_ALLOWED_HOSTS`)

**Ergebnis:** Step 1 abgeschlossen. `phase3_edge/` ist jetzt ein vollständiges (Nicht-Python-)
Verzeichnis mit Test-Anschluss; `SPACE_ALLOWED_HOSTS` existiert als Konfiguration statt
CLI-Zufall (P3-C).

**Dateien:**
- `phase3_edge/local.env.example` — Vorlage mit vier Platzhaltern (`REPO_ROOT`, `DATA_ROOT`,
  `VENV`, `ALLOWED_HOSTS`), ausschließlich Kommentare + Beispielpfade, kein echter Hostname,
  kein Token. `phase3_edge/local.env` selbst ist ab jetzt in `.gitignore` (Kommentar erklärt
  warum: Maschinenpfade, kein Geheimnis — der Hostname steht ohnehin in CT-Logs).
- `phase3_edge/tests/__init__.py` — leer, wie im Plan-Dateibaum vorgesehen (P1/P2 kommen ohne
  aus, P3 bekommt es laut Plan explizit, hier übernommen statt hinterfragt).
- `pytest.ini`: `testpaths` um `phase3_edge/tests` erweitert.
- `mcpserver/config.py`: `Settings.allowed_hosts: tuple[str, ...] = ()` neu, geparst über
  `_parse_allowed_hosts()` aus `SPACE_ALLOWED_HOSTS` (Komma-getrennt, `strip()`, leere Einträge
  verworfen, fehlende Variable → leeres Tupel — dieselbe Kein-Default-auf-echten-Wert-Logik wie
  bei `SPACE_DATA_ROOT`).
- `mcpserver/app.py`: `create_app()` berechnet `hosts = list(allowed_hosts) if allowed_hosts
  else (list(settings.allowed_hosts) or None)` — expliziter Parameter gewinnt, danach Settings,
  sonst FastMCPs eigener Default. Docstring ergänzt.
- `scripts/serve.py`: **unverändert**, wie geplant — `--allowed-host` bleibt `action="append"`,
  `default=None`; die neue Präzedenz lebt vollständig in `create_app()`.

**Tests** (`phase2_mcp/tests/test_config.py`, `test_app.py`, alle fünf aus dem Plan):
`test_allowed_hosts_defaults_to_empty`, `test_allowed_hosts_parses_comma_list`,
`test_allowed_hosts_strips_whitespace_and_drops_empties`,
`test_create_app_prefers_explicit_allowed_hosts_over_settings`,
`test_create_app_uses_settings_allowed_hosts`. Die beiden `app.py`-Tests patchen
`mcpserver.app.build_mcp` gegen eine `_CapturingFastMCP`-Stub-Klasse (`http_app()` zeichnet den
übergebenen `allowed_hosts`-Wert auf) statt den vollen FastMCP-Stack zu starten — Präzedenz ist
reine Verdrahtungslogik in `create_app()`, kein FastMCP-Verhalten (das deckt bereits
`test_asgi.py`/der Rest von `test_app.py` aus P2 ab).

**Verifiziert:**
- `.venv/bin/python -m pytest -q` → **138/138 grün** (133 Baseline + 5 neue).
- `bash scripts/dev_install.sh` (venv aktiviert) lief durch: nur `storage` und `mcpserver`
  editable installiert, `phase3_edge/` lautlos übersprungen (kein `pyproject.toml`) — Plan-Aussage
  in §1.2 damit real geprüft, nicht nur zitiert.

**Modul-Status oben nachgezogen** (Zeile 2: ⬜ → ✅, 5 Tests). Ab diesem Block gilt die
Rotationsregel: der Step-0-Block wandert über `scripts/rotate_session_block.sh phase3_edge`
nach `SESSIONS_ARCHIVE.md`.

**Nächster Schritt (konkret):** Step 2 — `mcpserver/request_log.py` (Tool- und HTTP-Log). Der
wichtigste Test dort ist `test_tool_event_never_contains_item_title` — er prüft eine Zusage,
keine Implementierung.

## Session stopped — 2026-07-27 (Step 0: Doku-Drift, Verifikation, Umgebungsinventar)

**Ergebnis:** Step 0 abgeschlossen. Kein Feature-Code — Haushalt vor dem ersten Baustein.

**A · Doku-Drift geschlossen** (Quelle: `PHASE2_CLOSEOUT_HANDOVER.md` §6 + Plan §0.4/§6):
- Root-`CLAUDE.md`: R5 „OAuth ist Phase 5" → **Phase 4** korrigiert (deckt sich mit der
  ROADMAP-Korrektur vom 2026-07-25, die bereits vorher galt, aber in R5 nicht nachgezogen war).
- Root-`CLAUDE.md`: R4 um die datierte Ergänzung zu Tailscale Funnel erweitert (§0.4 des Plans,
  wörtlich übernommen) — der ursprüngliche Cloudflare-Satz bleibt stehen, er beschreibt weiterhin
  korrekt, was dort gilt.
- Root-`CLAUDE.md`, „Current state": aktive Phase auf **P3** umgestellt, P2 in einen eigenen
  ✅-Absatz nach dem Muster von Phase 1 verschoben (inkl. Hinweis, dass der formale
  Abschluss-Handover jetzt existiert — der Satz „Formaler Phasenabschluss … steht noch aus" war
  mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt). `down:`-Karte von `phase2_mcp/CLAUDE.md`
  auf `phase3_edge/CLAUDE.md` umgehängt.
- `ROADMAP.md` und `phase2_mcp/CLAUDE.md`: `` `fastmcp` über Streamable HTTP `[VERIFY]` `` →
  Marker entfernt (live widerlegt, siehe P2-Abnahme).
- `ROADMAP.md`, Header-Card `down:`: `phase2_mcp_plan.md` und `phase3_edge_plan.md` ergänzt.
- `ROADMAP.md`, P3-Zeile: ⬜ → 🔄.
- `ROADMAP.md`, „Zurückgestellt aus P2": MCP-Revisions-Eintrag von Datum auf **Trigger**
  umgestellt (P3-E) — „erstes `fastmcp`-Release mit Support", nicht der 2026-07-28-Termin.
- `docs/INDEX.md`: neuer Abschnitt „Active phase (3)" mit drei Zeilen (Plan, Phase-Head, leeres
  Archiv); P2-Abschnitt nach „Completed phases" verschoben (🔄 → 📗); Zeile für
  `PHASE2_CLOSEOUT_HANDOVER.md` ergänzt; „Concept docs"-Fußnote von „P3–P5"/„P1- und P2-Pläne"
  auf „P4–P5"/„P1-, P2- und P3-Pläne" korrigiert.
- `ROADMAP.md`, P2-Abschnitt: der Satz „Fehlt noch: der formale Phasenabschluss (Browser-Webchat)"
  war mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt und stand — anders als in Root-`CLAUDE.md`
  — noch drin. Ersetzt durch „Handover an P3: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`",
  spiegelt jetzt den P1-Abschnitt, der denselben Satz für P1→P2 trägt.
- `phase2_mcp/CLAUDE.md`: `updated:`-Feld der Header-Card war bei diesem Commit stehen geblieben
  (`2026-07-26 (B2 behoben)`), obwohl der Scope-Absatz sich änderte — auf 2026-07-27 nachgezogen.

**Abweichung vom Plan, benannt:** `phase3_edge/CLAUDE.md` und `SESSIONS_ARCHIVE.md` (Plan-Step 1)
wurden bereits in Step 0 angelegt — minimal (L1-Card, Modul-Status, dieser Block), Scope/Runbooks
folgen wie geplant in Step 1. Grund: Hard Rule 8 verlangt den Phase-Head im selben Commit wie
jeden Step-Abschluss, und `docs/INDEX.md` braucht in diesem Commit bereits einen realen
Link-Empfänger statt eines toten Links.

**Sicherheits-Check vor dem Commit:** Die drei neuen, unversionierten Dateien
(`PHASE2_CLOSEOUT_HANDOVER.md`, `phase3_edge_plan.md`, `phase2_mcp_uebersicht.svg`) wurden vor
dem Staging mit `grep -aoE '[A-Za-z0-9_-]{32,}'` auf token-förmige Strings geprüft — Treffer
waren ausschließlich Testfunktionsnamen aus dem Plan. Das SVG (P2-Architekturdiagramm) enthält
nur den literalen Platzhalter `‹token›`, keinen echten Wert. Die SVG ist kein `.md` und damit
laut `docs/INDEX.md`-Scope („L0 map of every project .md") nicht indexpflichtig — bewusst nicht
aufgenommen, hier vermerkt statt stillschweigend übergangen.

**B · Verifikationsdurchlauf:**
- `git status` vor dem Commit: nur die drei erwarteten neuen Dateien untracked, sonst sauber.
- `docs/test-results/` existiert nicht (per `ls`, nicht per Doku-Aussage geprüft).
- Oversize-Check (`find … -size +40k`): zwei Treffer, `phase2_mcp_plan.md` und
  `phase3_edge_plan.md` — beide 📕, damit erlaubt.
- `pytest -q` über `.venv/bin/python -m pytest` (nicht System-Python): **133/133 grün**, deckt
  sich mit ROADMAP/Handover-Baseline.

**C · Umgebungsinventar** (alles `[VERIFY]`, read-only, kein Eingriff in echten `DATA_ROOT`/Keyring/Token):

| Prüfung | Ergebnis |
|---|---|
| Python | 3.12.3 |
| venv (für `ExecStart`, V6) | `/home/savefyx/dev/savefxy/.venv/bin/python` — Symlink-Kette über `python3` → System-`/usr/bin/python3.12`; der venv-Pfad selbst ist der korrekte `ExecStart`-Wert (aktiviert `pyvenv.cfg`/site-packages), nicht das Symlink-Ziel |
| `fastmcp` (V2) | **3.4.4 exakt installiert** — deckt sich bereits mit dem P3-D-Pin, keine Änderung nötig |
| Keyring-Backend (V5) | `keyring.backends.SecretService.Keyring` (priority 5), Chainer als Default-Frontend — deckt sich mit dem in P2 vom Nikinger bestätigten Roundtrip |
| systemd (V4) | Version 255 (≥250 ✓) |
| `systemd-creds` (V4) | vorhanden; `has-tpm2` → **„partial"**, kein volles TPM2-Sealing verfügbar (`+system`/`+subsystem`/`+libraries`, `-firmware`/`-driver`), Exit 3. `systemd-creds encrypt` fällt in diesem Fall auf Host-Key-Verschlüsselung zurück — für P3-F ausreichend (die Datei ist eine Hash-Map, kein umkehrbares Geheimnis; siehe Plan-Begründung) |
| Tailscale (V7) | **NICHT installiert** — `tailscale: command not found`. Echter Befund, kein „nichts zu tun": vor Step 7 (und vor jedem Live-Test von Step 4/6 gegen einen echten Funnel) muss der Nikinger Tailscale installieren, dem Tailnet beitreten, MagicDNS + HTTPS-Zertifikate aktivieren und `nodeAttrs: funnel` im Policy-File setzen. Blockiert **nicht** Steps 1–6 (reiner Code/Test-Weg), blockiert **Step 7**. |
| Dateisystem `DATA_ROOT` | `ext4` bestätigt — P1-Bedingung für `flock` weiterhin erfüllt |
| `cloudflared` | vorhanden unter `/usr/local/bin/cloudflared`, **kein** systemd-Service registriert (nur die P2-Quick-Tunnel-Nutzung von Hand) — Rückbau bleibt wie geplant Aufgabe von Step 6 |
| Git-Identität in `DATA_ROOT` | vorhanden (`Space Server` / `space-server@localhost`) — relevant für den in Plan §4 Step 4 benannten `ProtectSystem=strict`/Git-Commit-Fallstrick, dort real zu prüfen |

**Verifiziert:** `pytest -q` (via `.venv/bin/python -m pytest`) → 133/133 grün. `git status` vor
Commit sauber bis auf die drei erwarteten neuen Dateien. Secret-Scan der drei Dateien negativ.

**Nächster Schritt (konkret):** Step 1 — `phase3_edge/`-Gerüst vervollständigen
(`local.env.example`, `tests/__init__.py`, `.gitignore`-Ergänzung, `pytest.ini`-Erweiterung) und
Konfiguration (`SPACE_ALLOWED_HOSTS` in `config.py`/`app.py`, fünf Tests laut Plan). **Vor
Step 7** braucht es zusätzlich eine Nikinger-Aktion außerhalb des Plans selbst: Tailscale auf
dieser VM installieren und die Tailnet-Voraussetzungen (V7) einrichten — sonst lässt sich der
Runbook-Teil aus Step 7 nicht gegenprüfen.

