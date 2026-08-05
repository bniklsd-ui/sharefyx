#!/usr/bin/env bash
# Reproduziert die einzige Webfont-Datei der UI (Plan §4.2, [VERIFY] V31): lädt Inter Variable
# (OFL-1.1, https://github.com/rsms/inter) vom offiziellen GitHub-Release, pinnt die optische
# Größe auf Textgröße (opsz=14 — die einzige, die diese UI benutzt), beschneidet die
# Gewichtsachse auf 380–620 (deckt 400/500/600 aus Plan §4.2 mit Marge ab, spart Bytes) und
# subsetzt danach auf den Google-Fonts-"latin"-Unicodebereich (deckt deutsche Umlaute/ß über
# Latin-1 Supplement ab). Ergebnis: eine variable WOFF2-Datei, Dateiname trägt einen Kurzhash
# des Inhalts — macht sie zu einem "gehashten Asset" für webui/static_routes.py, das solche
# Namen mit einem unveränderlichen Cache-Header ausliefert.
#
# Braucht `fonttools`+`brotli` (`pip install fonttools brotli` in der Projekt-venv, nicht im
# Repo verankert — kein Laufzeit-Import, nur dieses Build-Skript benutzt sie, P5-T "kein
# Build-Step" bleibt für die Auslieferung selbst gültig, das hier ist Zutatenbeschaffung, kein
# Bundler).
set -euo pipefail

RELEASE_URL="https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
EXPECTED_ZIP_SHA256="9883fdd4a49d4fb66bd8177ba6625ef9a64aa45899767dde3d36aa425756b11e"
UNICODES="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LAYOUT_FEATURES="kern,liga,calt,tnum,lnum,pnum"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fonts_dir="${script_dir}/../webui/static/fonts"
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

command -v pyftsubset >/dev/null || {
    echo "pyftsubset fehlt — 'pip install fonttools brotli' in der venv, dann erneut." >&2
    exit 1
}

echo "Lade Inter v4.1 …" >&2
curl -sL --max-time 60 -o "${work_dir}/Inter-4.1.zip" "${RELEASE_URL}"
actual_sha256="$(sha256sum "${work_dir}/Inter-4.1.zip" | cut -d' ' -f1)"
if [ "${actual_sha256}" != "${EXPECTED_ZIP_SHA256}" ]; then
    echo "SHA256-Abweichung beim Inter-Release — abgebrochen (erwartet ${EXPECTED_ZIP_SHA256}, erhalten ${actual_sha256})." >&2
    exit 1
fi

unzip -o -q "${work_dir}/Inter-4.1.zip" -d "${work_dir}/extracted" "InterVariable.ttf" "LICENSE.txt"

echo "Pinne opsz=14, beschneide wght auf 380:620 …" >&2
python3 -m fontTools.varLib.instancer -q \
    -o "${work_dir}/pinned.ttf" "${work_dir}/extracted/InterVariable.ttf" \
    opsz=14 wght=380:620

echo "Subsetze auf Latin …" >&2
pyftsubset "${work_dir}/pinned.ttf" \
    --output-file="${work_dir}/subset.woff2" \
    --flavor=woff2 \
    --unicodes="${UNICODES}" \
    --layout-features="${LAYOUT_FEATURES}" \
    --no-hinting

subset_sha8="$(sha256sum "${work_dir}/subset.woff2" | cut -c1-8)"
target="${fonts_dir}/InterVariable-subset.${subset_sha8}.woff2"

mkdir -p "${fonts_dir}"
rm -f "${fonts_dir}"/InterVariable-subset.*.woff2
cp "${work_dir}/subset.woff2" "${target}"
cp "${work_dir}/extracted/LICENSE.txt" "${fonts_dir}/OFL.txt"

echo "Fertig: ${target} ($(du -h "${target}" | cut -f1))" >&2
