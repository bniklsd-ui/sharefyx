"""Gemeinsame Bild-Fixtures für die Test-Suite (P10.5, Block 3, LG-8 / P1-Öffnung 15).

**Warum es diese Datei gibt.** Seit P10.5 Block 3 bereinigt `Store.put_asset()` jedes Bild
(Exif, GPS, XMP, IPTC, PNG-Textfelder) und ist dabei **fail-closed**: eine Struktur, die der
Stripper nicht vollständig versteht, ergibt `ValidationError`. Der alte Dummy-Header
„\\x89PNG\\r\\n\\x1a\\n + Rest" ist damit **kein Bild mehr** — jede Bild-Fixture der Suite
braucht echte Bytes.

Die Bytes werden hier **gebaut** (Plan Block 3, Schritt 3.4: keine Binärdateien im Repo), an
**einer** Stelle: acht Testdateien in fünf Paketen brauchen dieselbe Fixture, und acht Kopien
eines Builders sind acht Stellen, an denen er veralten kann.

**Weg dorthin:** `pytest.ini` setzt `pythonpath = phase1_storage/tests` — deshalb ist dieses
Modul aus jedem Testpaket importierbar (`from sharefyx_image_bytes import png_bytes`).
Skripte, die **ohne** pytest laufen (`phase2_mcp/scripts/mcp_smoke.py`), tragen ihre eigene
Kopie: sie können sich nicht auf eine Test-Infrastruktur verlassen.
"""
from __future__ import annotations

import zlib


def png_bytes(*, payload: bytes = b"\x00\xff\x00\x00", text: bytes | None = None) -> bytes:
    """Ein 1×1-PNG als **echte** Bytes.

    * `payload` — der Inhalt des `IDAT`-Chunks (das „Bild“). Die Bytes stehen **wörtlich** in
      der Datei (Stufe 0 = „gespeichert“), damit ein Marker im Bildinhalt dort auch wieder
      auftaucht: sonst beweist die Prüfung „der Marker kommt in keiner Antwort vor“ nichts,
      weil er nie in der Datei war.
    * `text` — ein `tEXt`-Chunk („Comment\\0“ + Text). **Wird beim Hochladen entfernt**
      (LG-8) — die Fixture braucht ihn also nur, um das zu prüfen.
    """
    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        body = chunk_type + data
        return (
            len(data).to_bytes(4, "big")
            + body
            + (zlib.crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
        )

    ihdr = (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 2, 0, 0, 0])
    parts = [chunk(b"IHDR", ihdr)]
    if text is not None:
        parts.append(chunk(b"tEXt", b"Comment\x00" + text))
    parts += [chunk(b"IDAT", zlib.compress(payload, 0)), chunk(b"IEND", b"")]
    return b"\x89PNG\r\n\x1a\n" + b"".join(parts)
