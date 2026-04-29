#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import BuildDtboOverlay


def load_board_ids(path: Path) -> dict[str, dict[str, int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {key: value for key, value in raw.items() if isinstance(value, dict) and "board_id" in value}


def build_overlays(board_ids: dict[str, dict[str, int]], dtb_dir: Path, output_dir: Path, out_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    built = 0
    for codename, metadata in sorted(board_ids.items()):
        candidates = [dtb_dir / f"sm8250-xiaomi-{codename}.dtb"]
        candidates.extend(sorted(dtb_dir.glob(f"sm8250-xiaomi-{codename}-*.dtb")))
        device_dtb = next((path for path in candidates if path.is_file()), None)
        if device_dtb is None:
            continue
        output = output_dir / f"sm8250-xiaomi-{codename}.dtbo"
        BuildDtboOverlay.build_overlay(
            device_dtb,
            output,
            int(metadata.get("board_id", 0)),
            int(metadata.get("msm_id", 356)),
            out_dir,
        )
        built += 1
    print(f"kona-dtbo-overlays-built={built}")
    return 0 if built else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Xiaomi Kona DTBO overlay scaffolds from kernel-built DTBs")
    parser.add_argument("--board-ids", required=True)
    parser.add_argument("--dtb-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--out-dir", default="out")
    args = parser.parse_args(argv)
    return build_overlays(
        load_board_ids(Path(args.board_ids)),
        Path(args.dtb_dir),
        Path(args.output_dir),
        Path(args.out_dir),
    )


if __name__ == "__main__":
    raise SystemExit(main())
