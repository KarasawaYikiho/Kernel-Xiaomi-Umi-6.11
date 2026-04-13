#!/usr/bin/env bash
set -euo pipefail

# Normalize BOOTIMG_REQUIRED_BYTES from environment and export a safe integer value.
# - Empty input -> default
# - Non-integer input -> default (with warning)
# - Integer input (including <=0) -> preserved as-is

DEFAULT_BOOTIMG_REQUIRED_BYTES=134217728
raw="${BOOTIMG_REQUIRED_BYTES:-$DEFAULT_BOOTIMG_REQUIRED_BYTES}"
raw="${raw//[[:space:]]/}"

if [[ -z "$raw" ]]; then
  raw="$DEFAULT_BOOTIMG_REQUIRED_BYTES"
fi

if [[ "$raw" =~ ^-?[0-9]+$ ]]; then
  normalized="$raw"
else
  normalized="$DEFAULT_BOOTIMG_REQUIRED_BYTES"
  echo "::warning::Invalid bootimg_required_bytes input '$raw', fallback to $DEFAULT_BOOTIMG_REQUIRED_BYTES"
fi

echo "BOOTIMG_REQUIRED_BYTES=$normalized" >> "$GITHUB_ENV"
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "bootimg_required_bytes_normalized=$normalized" >> "$GITHUB_OUTPUT"
fi

echo "normalized_bootimg_required_bytes=$normalized"
