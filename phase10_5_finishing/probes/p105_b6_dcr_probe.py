#!/usr/bin/env python3
"""6.0 / [VERIFY V209] — was sendet der **aktuelle** opencode beim DCR?

Der P10-Befund (Register PA-1) stammt von opencode **1.18.33**: der DCR-Request trug
`application_type: null` und `redirect_uris: ["http://127.0.0.1:19876/mcp/oauth/callback"]`.
Der Plan (Block 6, Schritt 6.0) verlangt, das gegen die **heutige** Version nachzumessen —
der Rückgabe-Auslöser ist namentlich: nennt der Request `localhost` oder `[::1]`, fällt
P10.5-O (nur `127.0.0.1`, expliziter Port) und der Nikinger entscheidet neu.

**Wiederverwendung statt Kopie:** die Messanordnung (Wegwerf-App auf dem internen Port, der
protokollierende plain-http-Proxy mit Issuer-Rewrite, der isolierte opencode-Aufruf) steht
vollständig in `phase10_inventory/probes/p10_m3_dcr_probe.py` (P10, Block M3). Dieses Skript
importiert sie per `importlib` und überschreibt genau zwei Konstanten:

* `OC_BIN` — der isoliert installierte opencode (npm: `opencode-ai@latest`), **nicht** die
  Installation des Nikingers (`~/.nvm/.../opencode`), deren Konfiguration unangetastet bleibt
  (eigene `XDG_*`-Verzeichnisse, s. M3-Probe).
* `OUT_JSON` — das Ergebnis landet **hier**, nicht in `phase10_inventory/probes/` (dort liegt
  die eingecheckte P10-Baseline `p10_m3_dcr.json`; die wird nicht überschrieben).

Der M3b-Teil (vorregistrierter Client bis `initialize`) läuft hier nicht — er ist für V209
ohne Aussagekraft und würde die Frage „was sendet opencode" nicht beantworten.

Ausgabe: JSON auf stdout (Hard Rule 7) + `p105_b6_dcr.json` neben diesem Skript.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
M3_PROBE = REPO_ROOT / "phase10_inventory" / "probes" / "p10_m3_dcr_probe.py"
OC_BIN = "/tmp/opencode/p105-b6-oc/node_modules/.bin/opencode"
OUT_JSON = Path(__file__).resolve().parent / "p105_b6_dcr.json"


def _load_m3_probe():
    spec = importlib.util.spec_from_file_location("p10_m3_dcr_probe", M3_PROBE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _oc_version() -> str:
    try:
        out = subprocess.run([OC_BIN, "--version"], capture_output=True, text=True, timeout=60)
        return out.stdout.strip() or out.stderr.strip()
    except Exception as exc:  # pragma: no cover - Messgerät, kein Produktcode
        return f"unbekannt ({exc})"


def main() -> int:
    m3 = _load_m3_probe()
    m3.OC_BIN = OC_BIN
    m3.OUT_JSON = OUT_JSON
    rc = m3.main(["--skip-m3b"])

    # `m3.main()` schreibt eine hart kodierte Versionsangabe (1.18.33, der P10-Stand) — hier
    # durch den **gemessenen** Wert der installierten Version ersetzen.
    if OUT_JSON.exists():
        data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        data["opencode_version"] = _oc_version()
        data["opencode_binary"] = OC_BIN
        data["m3b_skipped"] = True
        OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(data, ensure_ascii=False, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
