"""Round-trip-treue Parsing/Serialisierung von Markdown-Dateien mit YAML-Frontmatter.

`python-frontmatter` wurde geprüft und verworfen: es sortiert Frontmatter-Keys
alphabetisch und wandelt ISO-8601-Timestamps in ein anderes String-Format um
(`2026-07-24T18:20:00Z` -> `2026-07-24 18:20:00+00:00`) — beides verletzt
Entscheidung A (Round-Trip-Treue ist nicht verhandelbar). Deshalb: eigener,
dünner Parser über PyYAML.
"""
from __future__ import annotations

import re

import yaml

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n(.*)\Z", re.DOTALL)


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
    fields = yaml.load(raw_yaml, Loader=_RoundTripLoader)
    if not isinstance(fields, dict):
        raise FrontmatterError("Frontmatter-Block ist kein YAML-Mapping")
    return fields, body


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
