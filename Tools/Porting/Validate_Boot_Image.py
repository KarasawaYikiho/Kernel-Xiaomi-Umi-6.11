#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import os

ANDROID_MAGIC = b"ANDROID!"
ZIP_MAGICS = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")

ART = Path("artifacts")
OUT = ART / "bootimg-info.txt"
DEFAULT_REQUIRED_BYTES = 134217728  # 128 MiB


def write_kv(lines: list[str]) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_required_bytes(raw: str | None) -> tuple[int, str]:
    """
    Parse BOOTIMG_REQUIRED_BYTES safely.
    Returns (required_bytes, parse_note).

    parse_note values:
      - exact: valid integer parsed from env
      - default-empty: env missing/empty, fell back to default
      - default-invalid: env invalid, fell back to default
    """
    if raw is None or not str(raw).strip():
        return DEFAULT_REQUIRED_BYTES, "default-empty"

    try:
        return int(str(raw).strip()), "exact"
    except (TypeError, ValueError):
        return DEFAULT_REQUIRED_BYTES, "default-invalid"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_prefix(path: Path, n: int = 8) -> bytes:
    with path.open("rb") as f:
        return f.read(n)


def _detect_format(path: Path) -> tuple[str, str]:
    prefix = _read_prefix(path, 8)
    if prefix.startswith(ANDROID_MAGIC):
        return "android_bootimg", prefix.hex()
    if any(prefix.startswith(m) for m in ZIP_MAGICS):
        return "zip", prefix[:4].hex()
    if not prefix:
        return "empty", ""
    return "unknown", prefix.hex()


def main() -> int:
    required_bytes, parse_note = parse_required_bytes(os.getenv("BOOTIMG_REQUIRED_BYTES"))

    bootimg = ART / "boot.img"
    if not bootimg.exists():
        write_kv([
            "status=missing",
            "reason=bootimg-not-found",
            "path=",
            "size_bytes=0",
            "sha256=",
            f"required_bytes={required_bytes}",
            f"required_bytes_parse={parse_note}",
            "size_match=no",
            "flash_ready=no",
        ])
        print(f"wrote {OUT}: missing")
        return 0

    size = bootimg.stat().st_size
    sha = _sha256(bootimg)
    detected_format, header_magic = _detect_format(bootimg)

    # BOOTIMG_REQUIRED_BYTES is treated as the final target size.
    if detected_format != "android_bootimg":
        size_match = "yes" if (required_bytes <= 0 or size == required_bytes) else "no"
        status = "invalid_format"
        if detected_format == "zip":
            reason = "bootimg-is-zip-not-android-image"
        elif detected_format == "empty":
            reason = "bootimg-empty"
        else:
            reason = "bootimg-header-unrecognized"
    elif required_bytes <= 0:
        size_match = "yes"
        status = "ok"
        reason = "size-check-disabled"
    else:
        size_match = "yes" if size == required_bytes else "no"
        status = "ok" if size_match == "yes" else "size_mismatch"
        reason = "release-ready-size-ok" if size_match == "yes" else "size-not-target"

    write_kv([
        f"status={status}",
        f"reason={reason}",
        f"path={bootimg.as_posix()}",
        f"size_bytes={size}",
        f"sha256={sha}",
        f"required_bytes={required_bytes}",
        f"required_bytes_parse={parse_note}",
        f"format={detected_format}",
        f"header_magic={header_magic}",
        f"size_match={size_match}",
        f"flash_ready={'yes' if status == 'ok' and size_match == 'yes' else 'no'}",
    ])
    print(f"wrote {OUT}: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
