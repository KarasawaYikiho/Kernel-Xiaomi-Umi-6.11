#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   CheckTargetKernelVersion.sh

source "Porting/Tools/Common.sh"
initialize_porting_paths

grep -E '^(VERSION|PATCHLEVEL|SUBLEVEL)\s*=\s*' "$KERNEL_DIR/Makefile"
