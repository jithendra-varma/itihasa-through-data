#!/usr/bin/env bash
# Download the third-party source texts used by the study (not redistributed here) and verify them.
set -euo pipefail
D="$(cd "$(dirname "$0")/../data" && pwd)"
curl -sSL -o "$D/vedic_index_cologne_vei.txt" \
  "https://raw.githubusercontent.com/sanskrit-lexicon/csl-orig/master/v02/vei/vei.txt"
T=$(mktemp -d)
for id in vedicindexofname01macduoft vedicindexofname02macduoft; do
  curl -sSL -o "$T/$id.txt" "https://archive.org/download/$id/${id}_djvu.txt"
done
cat "$T/vedicindexofname01macduoft.txt" "$T/vedicindexofname02macduoft.txt" > "$D/vedic_index_1912_ocr.txt"
echo "Checksums (expected values used in the study):"
echo "bcdaadf64ab64338278fe70f8d539d833220bdbade54b635ef5141f16c6d109e  vedic_index_cologne_vei.txt (Cologne CDSL, csl-orig master, 2 Nov 2026)"
echo "48151a869ec159dc6d2bc79f6485d53c8858c8e1a9114d00aaa8a46370e664aa  vedic_index_1912_ocr.txt (archive.org djvu text)"
( cd "$D" && sha256sum vedic_index_cologne_vei.txt vedic_index_1912_ocr.txt )
echo "If the Cologne checksum differs, the transcription has been revised upstream since the study."
