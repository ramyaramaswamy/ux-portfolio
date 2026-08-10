#!/bin/bash
set -euo pipefail

SRC_DIR="${1:-TV pics}"
OUT_DIR="${2:-$SRC_DIR/jpg}"
QUALITY="${3:-90}"

mkdir -p "$OUT_DIR"

shopt -s nullglob nocaseglob
files=("$SRC_DIR"/*.heic)
shopt -u nocaseglob

if [ ${#files[@]} -eq 0 ]; then
  echo "No HEIC files found in: $SRC_DIR"
  exit 0
fi

count=0
total=${#files[@]}
for f in "${files[@]}"; do
  count=$((count + 1))
  base="$(basename "$f")"
  name="${base%.*}"
  out="$OUT_DIR/$name.jpg"

  if [ -f "$out" ]; then
    echo "[$count/$total] skip (exists): $out"
    continue
  fi

  echo "[$count/$total] $base -> $out"
  sips -s format jpeg -s formatOptions "$QUALITY" "$f" --out "$out" >/dev/null
done

echo "Done. Converted to: $OUT_DIR (quality=$QUALITY)"
