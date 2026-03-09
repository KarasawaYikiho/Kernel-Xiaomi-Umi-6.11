#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   check_target_kernel_version.sh

grep -E '^(VERSION|PATCHLEVEL|SUBLEVEL)\s*=\s*' target/Makefile
