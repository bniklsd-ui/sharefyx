"""Round-trip-treue Parsing/Serialisierung von Markdown-Dateien mit YAML-Frontmatter.

`python-frontmatter` wurde geprüft und verworfen: es sortiert Frontmatter-Keys
alphabetisch und wandelt ISO-8601-Timestamps in ein anderes String-Format um
(`2026-07-24T18:20:00Z` -> `2026-07-24 18:20:00+00:00`) — beides verletzt
Entscheidung A (Round-Trip-Treue ist nicht verhandelbar). Deshalb: eigener,
dünner Parser über PyYAML.
"""
from __future__ import annotations

import logging
import re

import yaml

logger = logging.getLogger(__name__)

# P10.5 Block 15.2 (Ultra-Review B20): die drei Begrenzer duerfen auch `\r\n` tragen — eine
# unter Windows gespeicherte Datei ist sonst "kein Frontmatter" und war (mit B3) ein Startblocker.
# Geschrieben wird weiter nur `\n` (`serialize()`); der Body behaelt seine Zeilenenden byteweise.
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?\r?\n)---\r?\n(.*)\Z", re.DOTALL)


class FrontmatterError(ValueError):
    """Text enthält keinen gültigen Frontmatter-Block."""


class _RoundTripLoader(yaml.SafeLoader):
    """SafeLoader ohne impliziten Timestamp-Resolver.

    Ohne diese Änderung castet PyYAML Strings wie `2026-08-02` oder
    `2026-07-24T18:20:00Z` beim Parsen in `datetime.date`/`datetime.datetime`
    — die Typinformation der Modellschicht (storage.models) entscheidet über
    solche Felder, nicht der YAML-Parser.
    """


_RoundTripLoader.yaml_implicit_resolvers = {
    key: [r for r in resolvers if r[0] != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class _RoundTripDumper(yaml.SafeDumper):
    """SafeDumper ohne impliziten Timestamp-Resolver (Gegenstück zum Loader).

    PyYAML entscheidet beim Dumpen unabhängig vom Loader, ob ein String in
    Quotes muss, um beim erneuten Parsen ein String zu bleiben. Ohne diese
    Änderung würde `2026-08-02` als `'2026-08-02'` schreiben, obwohl es nie
    unquoted eingelesen wurde.
    """


_RoundTripDumper.yaml_implicit_resolvers = {
    key: [r for r in resolvers if r[0] != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeDumper.yaml_implicit_resolvers.items()
}


def parse(text: str) -> tuple[dict, str]:
    """Zerlegt eine Datei in (Frontmatter-Felder, Body).

    Feldreihenfolge bleibt erhalten (Python-Dicts sind insertion-ordered).
    Werte, die wie Datum/Zeit aussehen, bleiben Strings — Typisierung ist
    Aufgabe der Modellschicht.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise FrontmatterError("kein gültiger Frontmatter-Block (führendes '---' fehlt oder unabgeschlossen)")
    raw_yaml, body = m.group(1), m.group(2)
    try:
        fields = yaml.load(raw_yaml, Loader=_RoundTripLoader)
    except yaml.YAMLError as exc:
        # 15.2: `YAMLError` ist kein `ValueError` — ohne diese Uebersetzung lief kaputtes YAML an
        # jedem `except ValueError` im Kern vorbei (Rebuild, Space-Umbenennung).
        raise FrontmatterError(f"Frontmatter ist kein gültiges YAML: {exc}") from exc
    if not isinstance(fields, dict):
        raise FrontmatterError("Frontmatter-Block ist kein YAML-Mapping")
    return fields, body


def inline_text(value) -> str:
    """Ein Nicht-String-Wert als Text — so, wie er im YAML stand (`2026`, `true`, `[a, b]`).

    P10.5 Block 15.3 (Ultra-Review B5): ein von Hand getippter Titel `[a, b]` war gemeint, wie
    er da steht; `str()` machte daraus `['a', 'b']` und aus `true` ein `True`."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    text = yaml.dump(
        value, Dumper=_RoundTripDumper, default_flow_style=True, allow_unicode=True, width=2**31,
    )
    return text.removesuffix("...\n").strip()


def _text_list(value) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        # `tags: abc` meint einen Tag — `list("abc")` machte drei daraus.
        value = [value]
    return [inline_text(v) for v in value if v is not None]


def normalize_item_fields(fields: dict, *, source=None) -> dict:
    """Kopie von `fields`, in der `title` ein String und `tags`/`links`/`share_read`/
    `share_write` Listen von Strings sind. `source` (Dateipfad) steht nur in der Warnung.

    P10.5 Block 15.3 (Ultra-Review B5): **Lesen ist nachsichtig.** Ein Hand-Edit wie
    `tags: [2026]` oder `title: [a, b]` kostete die Textsuche aller Nutzer bzw. (seit 15.2) die
    Datei beim Neuaufbau. Beide Lesepfade — `store._item_from_text()` und
    `index.row_from_file()` — rufen genau diese Funktion, damit Index und `get()` nie
    auseinanderlaufen. `parse()` selbst bleibt roh: `_write_version_only` schreibt zurück, was
    der Mensch schrieb. Erst der nächste echte Write normalisiert die Datei (`'2026'`).

    P10.5 Block 15.3b (E5 = A, Nikinger 2026-10-30): `share_read: fabian` (Skalar statt Liste)
    ist **eine** Freigabe an `fabian` — vorher sechs an `f`, `a`, `b`, …, und der erste Write
    schrieb diese Buchstabenliste auf die Platte. Weil das eine Rechteerweiterung ist, die am
    Re-Auth-Gate vorbeiläuft (der Datei-Weg lag nie dahinter), meldet jede solche Koerzion ein
    `WARNING` mit Pfad — bis der nächste Write die Datei in Listenform bringt."""
    out = dict(fields)
    if "title" in out:
        out["title"] = inline_text(out["title"])
    for key in ("tags", "links", "share_read", "share_write"):
        if key in out:
            if key.startswith("share_") and out[key] is not None and not isinstance(out[key], list):
                logger.warning(
                    "%s: `%s: %s` ist keine Liste — gelesen als eine Freigabe an %r.",
                    source or "<ohne Pfad>", key, inline_text(out[key]), inline_text(out[key]),
                )
            out[key] = _text_list(out[key])
    return out


def serialize(fields: dict, body: str) -> str:
    """Kehrt `parse` um. `serialize(*parse(x)) == x`, wenn `fields`/`body` unverändert sind."""
    raw_yaml = yaml.dump(
        fields,
        Dumper=_RoundTripDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"---\n{raw_yaml}---\n{body}"
