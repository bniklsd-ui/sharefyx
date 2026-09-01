#!/usr/bin/env bash
# Reproduziert die zwei Webfont-Dateien der UI (Plan §4.C1, P8-G, [VERIFY] V83/V84): lädt
# IBM Plex Sans Variable (OFL-1.1, https://github.com/IBM/plex) und IBM Plex Mono (OFL-1.1) vom
# offiziellen GitHub-Release, pinnt die Gewichtsachse auf 380–620 (deckt 400/500/600 aus
# Plan §4.C1 mit Marge ab, spart Bytes), und subsetzt beide auf den Google-Fonts-"latin"-
# Unicodebereich (deckt deutsche Umlaute/ß über Latin-1 Supplement ab). Sans-Datei ist variabel
# (weight axis), Mono ist statisch (Regular = 400) — Mono braucht keine Instancierung. Ergebnis:
# zwei WOFF2-Dateien, Dateinamen tragen einen Kurzhash des Inhalts — macht sie zu "gehashten
# Assets" für webui/static_routes.py, das solche Namen mit einem unveränderlichen Cache-Header
# ausliefert.
#
# Pins (beide URLs und SHAs verifiziert am 2026-09-01 gegen github.com/IBM/plex/releases):
#   Sans  : @ibm/plex-sans-variable@0.2.0  →  plex-sans-variable.zip
#           (Font-Version IBM PLEX SANS VAR V3.0, 2024-12-12)
#   Mono  : @ibm/plex-mono@2.5.0           →  ibm-plex-mono.zip
#           (Font-Version IBM PLEX MONO V2.5, 2026-04-21)
#
# Braucht `fonttools`+`brotli` (`pip install fonttools brotli` in der Projekt-venv, nicht im
# Repo verankert — kein Laufzeit-Import, nur dieses Build-Skript benutzt sie, P5-T "kein
# Build-Step" bleibt für die Auslieferung selbst gültig, das hier ist Zutatenbeschaffung, kein
# Bundler).
set -euo pipefail

SANS_RELEASE_URL="https://github.com/IBM/plex/releases/download/@ibm/plex-sans-variable@0.2.0/plex-sans-variable.zip"
SANS_ZIP_SHA256="f83825d527be6cd39c8971c932b9bf22688a3ad3e5ac6305b6143d02f52b87b6"
SANS_TTF_IN_ZIP="fonts/complete/ttf/IBM Plex Sans Var-Roman.ttf"

MONO_RELEASE_URL="https://github.com/IBM/plex/releases/download/@ibm/plex-mono@2.5.0/ibm-plex-mono.zip"
MONO_ZIP_SHA256="6d23f01257663d8cc49a0d64c22ced630b79e0e2a0ac08a0da86e9a38bbc481c"
MONO_TTF_IN_ZIP="ibm-plex-mono/fonts/complete/ttf/IBMPlexMono-Regular.ttf"

UNICODES="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LAYOUT_FEATURES_SANS="kern,liga,calt,tnum,lnum,pnum"
LAYOUT_FEATURES_MONO="kern,liga,calt,tnum"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fonts_dir="${script_dir}/../webui/static/fonts"
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}"' EXIT

command -v pyftsubset >/dev/null || {
    echo "pyftsubset fehlt — 'pip install fonttools brotli' in der venv, dann erneut." >&2
    exit 1
}

mkdir -p "${fonts_dir}"

echo "Lade Plex Sans v0.2.0 (variable) …" >&2
curl -sL --max-time 60 -o "${work_dir}/plex-sans-variable.zip" "${SANS_RELEASE_URL}"
actual_sha256="$(sha256sum "${work_dir}/plex-sans-variable.zip" | cut -d' ' -f1)"
if [ "${actual_sha256}" != "${SANS_ZIP_SHA256}" ]; then
    echo "SHA-256-Abweichung beim Plex-Sans-Release — abgebrochen (erwartet ${SANS_ZIP_SHA256}, erhalten ${actual_sha256})." >&2
    exit 1
fi
unzip -o -q "${work_dir}/plex-sans-variable.zip" -d "${work_dir}/sans" "${SANS_TTF_IN_ZIP}" "fonts/complete/ttf/license.txt"

echo "Lade Plex Mono v2.5.0 (statisch) …" >&2
curl -sL --max-time 60 -o "${work_dir}/ibm-plex-mono.zip" "${MONO_RELEASE_URL}"
actual_sha256="$(sha256sum "${work_dir}/ibm-plex-mono.zip" | cut -d' ' -f1)"
if [ "${actual_sha256}" != "${MONO_ZIP_SHA256}" ]; then
    echo "SHA-256-Abweichung beim Plex-Mono-Release — abgebrochen (erwartet ${MONO_ZIP_SHA256}, erhalten ${actual_sha256})." >&2
    exit 1
fi
unzip -o -q "${work_dir}/ibm-plex-mono.zip" -d "${work_dir}/mono" "${MONO_TTF_IN_ZIP}" "ibm-plex-mono/fonts/complete/ttf/license.txt"

echo "Pinne Sans-wght auf 380:620 …" >&2
python3 -m fontTools.varLib.instancer -q \
    -o "${work_dir}/sans-pinned.ttf" "${work_dir}/sans/${SANS_TTF_IN_ZIP}" \
    wght=380:620

echo "Subsetze Sans auf Latin …" >&2
pyftsubset "${work_dir}/sans-pinned.ttf" \
    --output-file="${work_dir}/plex-sans-subset.woff2" \
    --flavor=woff2 \
    --unicodes="${UNICODES}" \
    --layout-features="${LAYOUT_FEATURES_SANS}" \
    --no-hinting

echo "Subsetze Mono auf Latin …" >&2
pyftsubset "${work_dir}/mono/${MONO_TTF_IN_ZIP}" \
    --output-file="${work_dir}/plex-mono-subset.woff2" \
    --flavor=woff2 \
    --unicodes="${UNICODES}" \
    --layout-features="${LAYOUT_FEATURES_MONO}" \
    --no-hinting

sans_sha8="$(sha256sum "${work_dir}/plex-sans-subset.woff2" | cut -c1-8)"
mono_sha8="$(sha256sum "${work_dir}/plex-mono-subset.woff2" | cut -c1-8)"
sans_target="${fonts_dir}/IBMPlexSans-subset.${sans_sha8}.woff2"
mono_target="${fonts_dir}/IBMPlexMono-subset.${mono_sha8}.woff2"

rm -f "${fonts_dir}"/IBMPlexSans-subset.*.woff2
rm -f "${fonts_dir}"/IBMPlexMono-subset.*.woff2
cp "${work_dir}/plex-sans-subset.woff2" "${sans_target}"
cp "${work_dir}/plex-mono-subset.woff2" "${mono_target}"
cp "${work_dir}/sans/fonts/complete/ttf/license.txt" "${fonts_dir}/OFL.txt"

echo "Fertig:" >&2
echo "  ${sans_target} ($(du -h "${sans_target}" | cut -f1))" >&2
echo "  ${mono_target} ($(du -h "${mono_target}" | cut -f1))" >&2
echo "  ${fonts_dir}/OFL.txt (Plex OFL-1.1)" >&2