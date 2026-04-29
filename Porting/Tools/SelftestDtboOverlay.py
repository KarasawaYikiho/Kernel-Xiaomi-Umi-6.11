#!/usr/bin/env python3
from __future__ import annotations

import BuildDtboOverlay


def expect_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing expected overlay text: {needle}")


def main() -> int:
    overlay = BuildDtboOverlay.generate_overlay_dts(
        board_id=43,
        msm_id=356,
        device_nodes={
            "ufs_mem_hc": 'status = "ok";\nqcom,disable-lpm;',
            "qupv3_se4_i2c": 'status = "ok";',
        },
    )
    expect_contains(overlay, "/plugin/;")
    expect_contains(overlay, "qcom,board-id = <0x2b>;")
    expect_contains(overlay, "qcom,msm-id = <356 0x20001>;")
    expect_contains(overlay, "target = <&ufs_mem_hc>;")
    expect_contains(overlay, 'status = "ok";')
    expect_contains(overlay, "target = <&qupv3_se4_i2c>;")
    print("dtbo-overlay-selftest=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
