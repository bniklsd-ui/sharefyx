#!/usr/bin/env python3
"""p10_m8_vision_probe.py — M8 (P10-Plan §4, Register BT-11, D-14): trägt ein lokales
Vision-Modell die Sichtprüfungen?

**Architektur (2026-10-19, nach der Korrektur im Session-Block):** die Messung läuft
NICHT auf der sharefyx-VM (5,8 GiB RAM, keine GPU — P9-C8: `ollama` dort `inactive`),
sondern gegen **CT 111**, den dedizierten Vision-Container mit der RTX 3060
(`http://192.168.68.140:11434`, einziger 11434-Listener laut P9-22-Beweis). Dort steht
der Incumbent `qwen3-vl:8b` (Step C), gegen den die drei Mitbewerber aus dem Plan fahren
(qwen2.5vl:7b, minicpm-v:8b, llama3.2-vision:11b) — Pulls dorthin, sequenziell, mit
`/api/delete` zwischendurch, damit CT 111 nicht volläuft.

**Prüfregel (P9-Session-Block 2026-10-05, `sichtpruefung_automation_conventions.md`):**
eine Frage, deren Antwort vorher bekannt ist — ein Modell, das die bekannte Antwort
verneint oder Inhalte erfindet, fällt. Genau das ist der Modus von
`probes/fixtures/questions.json` (6 Fragen: 5 gebaute Fallen + 1 echtes UI-Bild), gebaut
von `probes/p10_m8_fixtures.py`. Die Kategorie `empty_area` ist bewusst dieselbe Falle,
an der `qwen3-vl:8b` am 2026-10-05 mit „drei Panels mit erfundenen Inhalten" gescheitert ist.

**Urteil (`judge_contains`):** Liste von Gruppen; jede Gruppe ist eine Liste akzeptabler
Substrings. Bestanden = jede Gruppe hat ≥ 1 Treffer in der Antwort (case-insensitive,
denkt `<think>…</think>` vorher weg — qwen3-vl denkt sichtbar). Ausgabe: genau ein
JSON-Objekt auf stdout (Hard Rule 7), Logs auf stderr. Exit 0 auch bei durchgefallenen
Modellen (das ist ein Messergebnis, P10-7), Exit 3 bei Infra-Fehler (Endpoint weg —
gleiche Code-Zahl wie `mcp_local_vision_server.py`).

**Mit `--out`** wird das Ergebnis in die Sammeldatei `p10_m8_vision.json` gemergt
(Schlüssel = Modellname), damit ein Lauf alle vier Modelle in einer Datei trägt.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DIR = Path(__file__).resolve().parent
DEFAULT_ENDPOINT = "http://192.168.68.140:11434"  # CT 111 (RTX 3060) — siehe Docstring
PROMPT_SUFFIX = " Antworte kurz und konkret auf Deutsch."

MIME_BY_SUFFIX = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _post(endpoint: str, path: str, payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        endpoint.rstrip("/") + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _strip_thinking(text: str) -> str:
    out, skip = [], False
    for line in text.splitlines(keepends=True):
        low = line.lower()
        if "<think>" in low:
            skip = True
        if not skip:
            out.append(line)
        if "</think>" in low:
            skip = False
    return "".join(out).strip()


def _image_payload(path: Path) -> str:
    data = path.read_bytes()
    mime = MIME_BY_SUFFIX.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"unbekannter Bildtyp: {path.suffix} ({path})")
    return base64.b64encode(data).decode()


def _judge(answer: str, groups: list[list[str]]) -> dict:
    low = answer.lower()
    hits = []
    for group in groups:
        found = [alt for alt in group if alt.lower() in low]
        hits.append(found)
    return {"passed": all(hits), "group_hits": hits}


def run_model(endpoint: str, model: str, questions: dict, timeout: int) -> dict:
    results = []
    for qid, spec in questions.items():
        paths = []
        for name in spec["images"]:
            p = Path(name)
            paths.append(p if p.is_absolute() else DIR / "fixtures" / name)
        images = [_image_payload(p) for p in paths]
        t0 = time.monotonic()
        try:
            r = _post(endpoint, "/api/generate", {
                "model": model,
                "prompt": spec["q"] + PROMPT_SUFFIX,
                "images": images,
                "stream": False,
                "options": {"temperature": 0},
            }, timeout)
        except urllib.error.URLError as exc:
            return {"error": f"infra: {exc}", "model": model, "endpoint": endpoint}
        dur = round(time.monotonic() - t0, 1)
        raw = r.get("response", "")
        answer = _strip_thinking(raw)
        verdict = _judge(answer, spec["judge_contains"])
        results.append({
            "id": qid,
            "images": spec["images"],
            "question": spec["q"],
            "known": spec["known"],
            "raw_chars": len(raw),
            "answer": answer,
            "duration_s": dur,
            **verdict,
        })
        _log(f"[{model}] {qid}: {'PASS' if verdict['passed'] else 'FAIL'} ({dur}s, {len(raw)} raw Zeichen)")
    passed = sum(1 for r in results if r["passed"])
    return {
        "model": model,
        "endpoint": endpoint,
        "results": results,
        "passed": passed,
        "total": len(results),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    ap.add_argument("--model", required=True)
    ap.add_argument("--questions", default=str(DIR / "fixtures" / "questions.json"))
    ap.add_argument("--out", default=str(DIR / "p10_m8_vision.json"))
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    questions = json.loads(Path(args.questions).read_text())
    _log(f"M8 gegen {args.endpoint}, Modell {args.model}, {len(questions)} Fragen")
    try:
        summary = run_model(args.endpoint, args.model, questions, args.timeout)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}))
        return 3

    out_path = Path(args.out)
    collected = json.loads(out_path.read_text()) if out_path.exists() else {}
    if "error" not in summary:
        collected[args.model] = summary
        out_path.write_text(json.dumps(collected, ensure_ascii=False, indent=1))
        _log(f"Ergebnis nach {out_path} gemergt ({len(collected)} Modelle)")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if "error" not in summary else 3


if __name__ == "__main__":
    sys.exit(main())
