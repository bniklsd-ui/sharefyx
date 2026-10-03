#!/usr/bin/env bash
#
# archive_index_entries.sh — die datierten Nachtraige der INDEX-Eintraege verbatim in ein
# L3-Archiv verschieben (Gate/Z, 2026-10-03; Nikinger-Entscheidung 2026-10-03).
#
# **Was das loest.** `docs/INDEX.md` waechst nicht an einem Stueck, sondern an den *Nachtraegen*:
# jeder Session-Eintrag haengt seinen datierten Nachtrag an die Zeile des betroffenen Dokuments.
# Am 2026-10-03 waren das **37.391 B von 71.491 B** (43 von 93 Eintraegen) — mehr als die Haelfte
# der Datei, und der Grund fuer die Ueberschreitung, die P9-3 und V145 seit Wochen als ungeklaert
# fuehren. Die `updated:`-Kette des INDEX ist davon **nicht** betroffen (1.155 B, am 2026-10-03
# rotiert) — wer die Datei rotieren wollte, hat die falsche Stelle angefasst.
#
# **Was NICHT wandert.** Der *Kopf* jedes Eintrags (Glyph, Groesse, Ein-Satz-Zusammenfassung) ist der
# Inhalt der Karte; nur der datierte Nachtrag ist Chronik. Und die Groessenangabe muss auf der
# **ersten physischen Zeile** jedes Eintrags stehen bleiben, weil `doc_health.py ::
# _index_line_for()` genau eine physische Zeile liest — das ist keine Formalie, sondern die
# Bedingung dafuer, dass `oversize` die Datei ueberhaupt pruefen kann.
#
# **Ein logischer Eintrag ist ein Bullet plus seine Folgezeilen.** Fuenf Eintraege der Karte
# erstrecken sich ueber mehrere physische Zeilen (die Phase-9-Zeilen sind beim Umbruch des
# Dateikopfes auseinandergefallen). Das Skript arbeitet deshalb auf logischen Eintraegen und nicht
# auf Zeilen — die erste Fassung schnitt an physischen Zeilen und haette bei genau diesen fuenf
# Eintraegen mitten in einem Nachtrag abgeschnitten.
#
# **Nichts wird abgetippt.** Die Nachtraege werden per python geschnitten, die Reassemblierung wird
# gegen das Original geprueft, jeder Nachtrag wird nach dem Schreiben byte-identisch im Archiv
# wiedergefunden. Fuenf Gegenproben vor dem Schreiben, Abbruch ohne jede Zielberuehrung bei
# Abweichung:
#   (a) Byte-Buchhaltung: je Eintrag gilt original = kopf + nachrag, und im INDEX steht danach
#       kopf + zeiger
#   (b) `cmp` der Reassemblierung des Originals aus (neuem INDEX + Archiv)
#   (c) jeder verschobene Nachtrag byte-identisch im Archiv wiedergefunden
#   (d) kein datierter Nachtrag bleibt im INDEX zurueck (Gegenprobe gegen einen blinden Schnitt)
#   (e) jede Groessenangabe steht weiterhin auf der ersten physischen Zeile ihres Eintrags, und
#       jede Zeile, die `benannt statt versteckt` traegt, traegt es weiterhin (sonst waere die
#       Datei nach der Rotation fuer `doc_health` eine *neue* Oversize ohne Benennung)
#
# **(d) ist der Rueckfall, nicht die traegende Pruefung — das war zuerst falsch behauptet.**
# `phase9_hardening/tests/test_index_archive.py :: test_a_weakened_cut_anchor_is_caught_before_
# anything_is_written` hat es nachgewiesen: nimmt man dem Anker die `**`-Alternative, greift
# zuerst die Satzgrenzen-Pruefung (der Kopf endet dann auf `**`) und (d) kommt gar nicht dazu.
# Mit dem heutigen Anker — erster Treffer — ist ein "zu spaeter" Schnitt nicht erzeugbar, ohne
# dieses Skript zu veraendern. (d) bleibt als Vorabversion desselben Satzes, den
# `test_no_entry_line_carries_a_dated_addendum_any_more` am echten Artefakt prueft; eine Zeile
# fuer den Fall, dass jemand den Anker erweitert.
#
# **Bekannte Kosmetik, bewusst so:** bekommt eine Zeile, die schon einen Zeiger traegt, einen
# neuen Nachtrag, dann steht am Ende zwei Zeiger. Der Grund ist die Regel, die jetzt gilt
# (Kartenzeilen bekommen keine Nachtraege mehr), und der Gegenfall waere ein Skript, das dem
# Autor eine Zeile in einer fremden Datei umbaut, um die Beweis-Kette zu retten.
#
# **Aufruf:**   scripts/archive_index_entries.sh [repo_root]
# **Exit:**     0 = verschoben · 1 = Abbruch, nichts geaendert · 2 = nichts zu tun (kein Eintrag
#               traegt einen datierten Nachtrag) · 3 = Archiv fehlt und wird nicht angelegt
#
# **Danach von Hand:** 1) Groessenangabe der Karte selbst in `docs/INDEX.md` auf den neuen Stand
# bringen (gleiche Zeichenzahl, sonst verschiebt sich die Zahl selbst) · 2) `docs/INDEX.md`-Zeile
# fuer das neue Archiv ergaenzen · 3) P9-3/V145 auf das neue Kriterium umstellen.

set -euo pipefail

REPO_ROOT="${1:-.}"
INDEX="${REPO_ROOT}/docs/INDEX.md"
ARCHIVE="${REPO_ROOT}/docs/INDEX_ENTRIES_ARCHIVE.md"

[[ -f "$INDEX" ]] || { echo "ABBRUCH: ${INDEX} nicht gefunden" >&2; exit 1; }
[[ -f "$ARCHIVE" ]] || { echo "ABBRUCH: ${ARCHIVE} nicht gefunden — L3-Archiv mit L1-Card anlegen — es ist nicht angelegt worden, das Skript legt es nicht an" >&2; exit 3; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
die() { echo "ABBRUCH: $*" >&2; exit 1; }

cp "$INDEX" "$WORK/index.orig"
cp "$ARCHIVE" "$WORK/archive.orig"

# ---------------------------------------------------------------- schneiden
# Logische Eintraege: Bullet-Zeile plus Folgezeilen, die weder neuer Bullet noch Ueberschrift
# noch Tabellenzeile noch Leerzeile sind. Schneidepunkt je Eintrag: die ERSTE Stelle, an der ein
# datierter Nachtrag beginnt (`[YYYY-MM-DD`). Alles davor ist Kopf, alles danach wandert.
python3 - "$INDEX" > "$WORK/plan.json" <<'PYEOF'
import json, re, sys

ADDENDA_RE = re.compile(r"(?:\*\*)?\[(?:20\d\d-\d\d-\d\d)")
SIZE_RE = re.compile(r"\*\*[0-9.,]+\s?(?:B|KB)\b")
lines = open(sys.argv[1], encoding="utf-8").read().splitlines(keepends=True)

def is_start(line: str) -> bool:
    return line.startswith("- [") or line.startswith("#") or line.startswith("|") or not line.strip()

groups, cur = [], None
for i, line in enumerate(lines):
    if line.startswith("- ["):
        if cur is not None:
            groups.append(cur)
        cur = [i]
    elif cur is not None and not is_start(line):
        cur.append(i)
    else:
        if cur is not None:
            groups.append(cur); cur = None
if cur is not None:
    groups.append(cur)

plan = []
for g in groups:
    text = "".join(lines[i] for i in g)
    m = ADDENDA_RE.search(text)
    if not m:
        continue
    # Ziel der Kachel: der Pfad im Link, eindeutig genug fuer eine Abschnitts-Ueberschrift
    lm = re.search(r"^- \[([^\]]+)\]", lines[g[0]])
    label = lm.group(1) if lm else f"zeile-{g[0] + 1}"
    plan.append({
        "first": g[0], "last": g[-1],
        "label": label,
        "head": text[: m.start()],
        "addenda": text[m.start():],
        "size_on_first_line": bool(SIZE_RE.search(lines[g[0]])),
    })

json.dump({"groups": len(groups), "plan": plan}, sys.stdout)
PYEOF

PLAN_COUNT="$(python3 -c "import json,sys; print(len(json.load(open(sys.argv[1]))['plan']))" "$WORK/plan.json")"
if [[ "$PLAN_COUNT" == "0" ]]; then
  echo "Nichts zu tun: kein Eintrag traegt einen datierten Nachtrag."
  exit 2
fi
echo "Verschoben werden: ${PLAN_COUNT} von $(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['groups'])" "$WORK/plan.json") logischen Eintraegen"

# ---------------------------------------------------------------- Gegenproben (a) und (d) auf dem Plan
python3 - "$WORK/plan.json" <<'PYEOF' || exit 1
import json, re, sys
plan = json.load(open(sys.argv[1]))["plan"]
for p in plan:
    if not p["addenda"].strip():
        print(f"ABBRUCH: {p['label']}: leerer Nachtrag am Schnitt", file=sys.stderr); sys.exit(1)
    head = p["head"].rstrip()
    if head and not head.endswith(("·", "—", "–", "-", "|", "(", ",", ":", ";", "!", "?", ".")):
        print(f"ABBRUCH: {p['label']}: der Kopf endet mitten im Satz ({head[-40:]!r}) — "
              "der Schnittpunkt ist vermutlich falsch", file=sys.stderr)
        sys.exit(1)
    if not p["head"].endswith(" "):
        print(f"ABBRUCH: {p['label']}: der Kopf endet nicht auf einem Leerzeichen "
              f"({p['head'][-12:]!r}) — der Zeiger braucht keine eigene Nahtstelle", file=sys.stderr)
        sys.exit(1)
    if not p["addenda"].endswith("\n"):
        print(f"ABBRUCH: {p['label']}: der Nachtrag endet nicht mit einem Zeilenumbruch — die "
              "Reassemblierung setzt genau einen wieder ein und waere sonst still falsch", file=sys.stderr)
        sys.exit(1)
    if not re.match(r"(?:\*\*)?\[20\d\d-\d\d-\d\d", p["addenda"]):
        print(f"ABBRUCH: {p['label']}: Nachtrag beginnt nicht mit einem datierten "
              f"Nachtrag ({p['addenda'][:20]!r})", file=sys.stderr); sys.exit(1)
print(f"OK  {len(plan)} Schnitte plausibel")
PYEOF

# ---------------------------------------------------------------- Archiv anhaengen
# Ohne fuehrendes Leerzeichen: **jeder** Kopf endet auf einem Leerzeichen (vom Planer geprueft),
# also ist die Nahtstelle genau ein Leerzeichen und der Kopf bleibt byteweise unangetastet.
POINTER_TAIL="· **[Details im Archiv](INDEX_ENTRIES_ARCHIVE.md)**"

python3 - "$WORK/plan.json" "$ARCHIVE" <<'PYEOF'
import json, re, sys

plan = json.load(open(sys.argv[1]))["plan"]
archive = open(sys.argv[2], encoding="utf-8").read().rstrip("\n")
anchor = re.search(r"^# (.+)$", archive.split("\n", 12)[0] + "\n", re.M)

blocks = []
for p in plan:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", p["label"]).strip("-")
    body = p["addenda"].strip("\n")
    blocks.append(f"\n## `{p['label']}`\n\n{body}\n")

with open(sys.argv[2], "w", encoding="utf-8") as fh:
    fh.write(archive + "\n" + "".join(blocks))
PYEOF

# ---------------------------------------------------------------- INDEX umschreiben
# Der Kopf bleibt **byteweise** stehen, der Nachtrag fällt weg, und der Zeiger wird **an genau
# dieselbe Stelle** gesetzt — kein `rstrip`, kein eingefügter Zeilenumbruch. Danach ist
# `kopf + zeiger` == `kopf + zeiger` und `kopf + nachtrag` == Original; die Gegenprobe (b) prüft
# beides. Ein Zeilenumbruch an dieser Stelle ist ein Fehler, den die Reassemblierung sofort zeigt.
python3 - "$WORK/plan.json" "$INDEX" <<'PYEOF'
import json, sys

plan = json.load(open(sys.argv[1]))["plan"]
lines = open(sys.argv[2], encoding="utf-8").read().splitlines(keepends=True)
pointer = "**Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**"

# Von hinten nach vorn: die Zeilennummern der noch nicht bearbeiteten Eintraege bleiben gueltig.
for p in sorted(plan, key=lambda p: p["first"], reverse=True):
    entry = "".join(lines[p["first"]: p["last"] + 1])
    assert entry.count(p["addenda"]) == 1, f"{p['label']}: Nachtrag nicht eindeutig im Eintrag"
    lines[p["first"]: p["last"] + 1] = [entry.replace(p["addenda"], "", 1) + pointer + "\n"]

with open(sys.argv[2], "w", encoding="utf-8") as fh:
    fh.write("".join(lines))
PYEOF

# ---------------------------------------------------------------- Gegenproben (b) (c) (d) (e)
python3 - "$WORK/index.orig" "$WORK/archive.orig" "$INDEX" "$ARCHIVE" <<'PYEOF' || { cp "$WORK/index.orig" "$INDEX"; cp "$WORK/archive.orig" "$ARCHIVE"; exit 1; }
import re, sys

orig, arch_old, new, arch_new = (open(p, encoding="utf-8").read() for p in sys.argv[1:5])
# **Bewusst kein Markdown-Link.** `doc_health._index_line_for()` erkennt eine Zeile an
# `](pfad)` und wertet den Zeiger dann als die INDEX-Zeile des Archivs aus — der erste
# Lauf liess deshalb „glyph='🔗'" fuer ein Archiv, das keine Zeile hatte. Ein Zeiger, der
# wie ein Eintrag aussieht, ist fuer einen Zeiger die falsche Form.
POINTER = "**Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**"
# **Dieselbe Form wie `doc_health.py :: _named_size_is_current` akzeptiert** — exakte Bytezahl in
# Bold oder gerundete `~NNKB`. Der erste Entwurf prüfte nur die Bold-Form und brach bei der
# P8.6-Zeile ab, die `~106KB` schreibt: ein Wächter, strenger als die Regel, die er verteidigt,
# verteidigt sie nicht.
SIZE_ON_LINE_RE = re.compile(r"\*\*[0-9.,]+\s?(?:B|KB)\b|~[0-9]+KB")
# Der Abschnittskoerper laeuft bis zum naechsten `## ` oder Dateiende — **nicht** bis zum ersten
# Zeilenumbruch: ein Nachtrag aus fuenf physischen Zeilen wird von `(.*?)\n` auf eine Zeile
# gekuerzt, und die Reassemblierung schlaegt dann genau an dieser Stelle fehl.
# **Alle** Abschnitte, nicht nur die neu angehaengten: der Zeiger der Karten-Zeile der Karte
# selbst zeigt auf einen Abschnitt aus einem *frueheren* Lauf. Nur die neuen werden fuer (c)
# gemeldet, die Zuordnung beim (b)-Abgleich darf aber nur die Archive insgesamt kennen.
new_sections = re.findall(r"\n## `([^`]+)`\n\n(.*?)(?=\n## `|\Z)", arch_new[len(arch_old):], re.S)
sections = re.findall(r"^## `([^`]+)`\n\n(.*?)(?=^## `|\Z)", arch_new, re.S | re.M)

# (c) jeder verschobene Nachtrag byte-identisch im Archiv wiedergefunden
for label, body in new_sections:
    if body.strip() not in arch_new:
        print(f"ABBRUCH: {label}: Nachtrag nicht byte-identisch im Archiv", file=sys.stderr); sys.exit(1)

# (d) im INDEX darf kein datierter Nachtrag einer Eintragszeile mehr stehen
for line in new.splitlines():
    if line.startswith("- [") and re.search(r"(?:\*\*)?\[(?:20\d\d-\d\d-\d\d)", line):
        print(f"ABBRUCH: im INDEX steht noch ein datierter Nachtrag: {line[:70]}", file=sys.stderr); sys.exit(1)

# (e) jede Groessenangabe und jede Benennung steht weiter auf der ersten physischen Zeile
for line in new.splitlines():
    if line.startswith("- [") and ("benannt statt versteckt" in line or "benannt statt verstopft" in line):
        if not SIZE_ON_LINE_RE.search(line):
            print(f"ABBRUCH: Benennung ohne Groessenangabe auf der ersten Zeile: {line[:70]}", file=sys.stderr)
            sys.exit(1)

# (b) Reassemblierung: INDEX + Archiv-Nachtraege == Original, byteweise.
#
# **Nach Etikett, nicht nach Reihenfolge.** Die erste Fassung nahme "der n-te Zeiger gehoert zum
# n-ten Archivabschnitt" — das stimmt nur, wenn *jeder* Zeiger ein neu eingefuegter ist, also
# genau beim ersten Lauf. Beim zweiten Lauf (und ab dem naechsten Session-Block jeder weitere) sind
# 43 Zeiger alt und einer neu, und die Zuordnung verschiebt sich: die Reassemblierung laeuft dann
# in einen StopIteration. Der Test `test_a_roundtrip_restores_the_original_byte_for_byte` hat das
# gefunden, weil er genau den Alltagsfall baut — ein INDEX, der schon rotiert ist, plus *ein*
# neuer Nachtrag. Der Etikett-Schluessel ist zugleich die ehrlichere Pruefung: sie schlaegt auch dann
# fehl, wenn ein Zeiger ohne Abschnitt dasteht.
bodies = dict(sections)
# **Nur die Zeiger dieses Laufs** werden zurueckgesetzt. Ein Zeiger aus einem frueheren Lauf steht
# im Original genauso, wie er in der neuen Datei steht — ihn wieder aufzukleben wuerde das Original
# an dieser Stelle veraendern und die Reassemblierung sinnlos machen. Genau daran ist die erste
# Etikett-Fassung gescheitert: sie hat *alle* Zeiger zurueckgesetzt und damit genau die Eintraege
# beschaedigt, die gar nicht angefasst wurden.
touched = {label for label, _ in new_sections}
rebuilt, current = [], None
for line in new.splitlines(keepends=True):
    m = re.match(r"^- \[([^\]]+)\]", line)
    if m:
        current = m.group(1)
    if line.rstrip("\n").endswith(POINTER) and current in touched:
        if current not in bodies:
            print(f"ABBRUCH: Zeiger fuer '{current}' hat keinen Abschnitt im Archiv", file=sys.stderr)
            sys.exit(1)
        rebuilt.append(line.rstrip("\n")[: -len(POINTER)] + bodies[current].rstrip("\n") + "\n")
    else:
        rebuilt.append(line)
rebuilt = "".join(rebuilt)
if rebuilt != orig:
    for i, (a, b) in enumerate(zip(rebuilt, orig)):
        if a != b:
            print(f"ABBRUCH: Reassemblierung weicht bei Byte {i} ab: {rebuilt[i-40:i+40]!r}", file=sys.stderr)
            break
    else:
        print(f"ABBRUCH: Laenge {len(rebuilt)} statt {len(orig)}", file=sys.stderr)
    sys.exit(1)

print(f"OK  (b) Reassemblierung byte-identisch ({len(orig)} B)")
print(f"OK  (c) {len(new_sections)} Nachtraege byte-identisch im Archiv")
print("OK  (d) kein datierter Nachtrag mehr im INDEX")
print("OK  (e) jede Groessenangabe steht auf der ersten physischen Zeile")
PYEOF

echo "OK  docs/INDEX.md:        $(wc -c < "$WORK/index.orig") B -> $(wc -c < "$INDEX") B"
echo "OK  docs/INDEX_ENTRIES_ARCHIVE.md: $(wc -c < "$WORK/archive.orig") B -> $(wc -c < "$ARCHIVE") B"
echo "    Backups: ${WORK}.orig — die Gegenproben haben vor dem Schreiben geprueft, die Originale"
echo "    liegen zusaetzlich unter /tmp/opencode, falls du den Lauf zuruecknehmen willst."
echo
echo "Danach von Hand: 1) Groessenangabe der Karten-Zeile auf den neuen Stand 2) INDEX-Zeile fuer"
echo "das Archiv 3) P9-3/V145 auf das neue Kriterium 4) Backup-Verzeichnis loeschen"
