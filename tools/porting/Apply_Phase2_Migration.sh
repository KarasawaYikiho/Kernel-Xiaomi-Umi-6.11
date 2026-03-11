#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   Apply_Phase2_Migration.sh <device>

DEVICE="${1:-umi}"

chmod +x tools/porting/Phase2_Apply.sh
./tools/porting/Phase2_Apply.sh "$PWD/source" "$PWD/target" "$DEVICE"
