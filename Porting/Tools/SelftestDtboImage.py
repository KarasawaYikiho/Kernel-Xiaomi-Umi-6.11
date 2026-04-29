#!/usr/bin/env python3
from __future__ import annotations

import json
import struct
import tempfile
from pathlib import Path

import BuildDtboImage


def expect(name: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        dtb_dir = tmp / "dtbs"
        dtb_dir.mkdir()
        board_ids = tmp / "KonaBoardIds.json"
        out = tmp / "dtbo.img"

        (dtb_dir / "sm8250-xiaomi-umi.dtb").write_bytes(b"umi-dtb")
        (dtb_dir / "sm8250-xiaomi-pipa.dtb").write_bytes(b"pipa-dtb")
        board_ids.write_text(
            json.dumps(
                {
                    "_description": "test metadata is ignored",
                    "umi": {"board_id": 43, "msm_id": 356},
                    "pipa": {"board_id": 52, "msm_id": 356},
                    "missing": {"board_id": 99, "msm_id": 356},
                }
            ),
            encoding="utf-8",
        )

        rc = BuildDtboImage.main(
            [
                "--board-ids",
                str(board_ids),
                "--dtb-dir",
                str(dtb_dir),
                "--output",
                str(out),
            ]
        )
        expect("return code", rc, 0)

        data = out.read_bytes()
        expect("magic", struct.unpack_from(">I", data, 0)[0], 0xD7B7AB1E)
        expect("header size", struct.unpack_from(">I", data, 8)[0], 32)
        expect("entry size", struct.unpack_from(">I", data, 12)[0], 32)
        expect("entry count", struct.unpack_from(">I", data, 16)[0], 2)
        expect("entries offset", struct.unpack_from(">I", data, 20)[0], 32)
        expect("page size", struct.unpack_from(">I", data, 24)[0], 4096)
        expect("version", struct.unpack_from(">I", data, 28)[0], 0)

        first_size = struct.unpack_from(">I", data, 32)[0]
        first_offset = struct.unpack_from(">I", data, 36)[0]
        first_id = struct.unpack_from(">I", data, 40)[0]
        first_rev = struct.unpack_from(">I", data, 44)[0]
        first_custom0 = struct.unpack_from(">I", data, 48)[0]
        second_size = struct.unpack_from(">I", data, 64)[0]
        second_offset = struct.unpack_from(">I", data, 68)[0]
        second_id = struct.unpack_from(">I", data, 72)[0]
        second_rev = struct.unpack_from(">I", data, 76)[0]
        second_custom0 = struct.unpack_from(">I", data, 80)[0]
        expect("first id", first_id, 52)
        expect("first rev", first_rev, 356)
        expect("first custom board id", first_custom0, 52)
        expect("second id", second_id, 43)
        expect("second rev", second_rev, 356)
        expect("second custom board id", second_custom0, 43)
        expect("first dtb", data[first_offset:first_offset + first_size], b"pipa-dtb")
        expect("second dtb", data[second_offset:second_offset + second_size], b"umi-dtb")
        if len(data) % 4096 != 0:
            raise AssertionError("dtbo image must be page aligned")

    print("dtbo-image-selftest=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
