#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from Kv_Utils import parse_kv

ART = Path("artifacts")
PACK_INFO = ART / "umi_bundle" / "pack-info.txt"
OUT = ART / "flash-readiness.txt"


def parse_count(value: str) -> int:
    return int(re.sub(r"\D", "", value or "0") or 0)


def main() -> int:
    ART.mkdir(parents=True, exist_ok=True)
    if not PACK_INFO.exists():
        OUT.write_text("status=unknown\nreason=pack-info-missing\n", encoding="utf-8")
        print("pack-info missing")
        return 0

    pack = parse_kv(PACK_INFO)
    dtb = parse_kv(ART / "dtb-postcheck.txt")
    anykernel = parse_kv(ART / "anykernel-info.txt")
    anykernel_validate = parse_kv(ART / "anykernel-validate.txt")
    bootimg = parse_kv(ART / "bootimg-info.txt")

    xiaomi_dtb_count = parse_count(pack.get("umi_bundle_xiaomi_dtb_count", "0"))
    hint = pack.get("flash_ready_hint", "no")
    manifest_hit = parse_count(dtb.get("hit", "0"))
    anykernel_ok = anykernel.get("anykernel_ok", "no") == "yes"
    anykernel_validate_ok = anykernel_validate.get("status", "unknown") in (
        "ok",
        "unknown",
    )
    bootimg_ok = bootimg.get("status", "missing") == "ok"
    bootimg_rom_aligned = (
        bootimg.get("rom_size_match", "unknown") == "yes"
        and bootimg.get("rom_sha256_match", "unknown") == "yes"
    )

    status = "not_ready"
    reason = "insufficient-xiaomi-dtb"
    if xiaomi_dtb_count >= 1 and hint == "candidate":
        if not anykernel_ok:
            reason = "candidate-missing-anykernel"
        elif not anykernel_validate_ok:
            reason = "candidate-anykernel-invalid"
        elif manifest_hit <= 0:
            reason = "candidate-dtb-manifest-miss"
        else:
            status = "candidate"
            reason = "structure-ok-need-runtime-test"

    release_status = "blocked"
    release_reason = "bootimg-not-ready"
    if bootimg_ok:
        release_status = "ready" if bootimg_rom_aligned else "needs-review"
        release_reason = (
            "rom-aligned-bootimg" if bootimg_rom_aligned else "bootimg-not-rom-matched"
        )

    OUT.write_text(
        "\n".join(
            [
                f"status={status}",
                f"reason={reason}",
                f"xiaomi_dtb_count={xiaomi_dtb_count}",
                f"manifest_hit={manifest_hit}",
                f"anykernel_ok={'yes' if anykernel_ok else 'no'}",
                f"anykernel_validate_ok={'yes' if anykernel_validate_ok else 'no'}",
                f"release_status={release_status}",
                f"release_reason={release_reason}",
                f"bootimg_status={bootimg.get('status', 'missing')}",
                f"bootimg_rom_size_match={bootimg.get('rom_size_match', 'unknown')}",
                f"bootimg_rom_sha256_match={bootimg.get('rom_sha256_match', 'unknown')}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT}: {status}/{release_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
