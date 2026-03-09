#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   apply_phase2_migration.sh <device>

DEVICE="${1:-umi}"

chmod +x tools/porting/phase2_apply.sh
./tools/porting/phase2_apply.sh "$PWD/source" "$PWD/target" "$DEVICE"
