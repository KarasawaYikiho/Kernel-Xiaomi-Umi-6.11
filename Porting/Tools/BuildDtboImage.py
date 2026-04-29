#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Sequence


DT_TABLE_MAGIC = 0xD7B7AB1E
HEADER_SIZE = 32
ENTRY_SIZE = 32
PAGE_SIZE = 4096
VERSION = 0


def align(value: int, page_size: int = PAGE_SIZE) -> int:
    return ((value + page_size - 1) // page_size) * page_size


def load_board_ids(path: Path) -> dict[str, dict[str, int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict[str, int]] = {}
    for key, value in raw.items():
        if key.startswith("_") or not isinstance(value, dict):
            continue
        if "board_id" not in value:
            continue
        out[str(key)] = {
            "board_id": int(value.get("board_id", 0)),
            "msm_id": int(value.get("msm_id", 356)),
        }
    return out


def candidate_dtb_paths(dtb_dir: Path, codename: str) -> list[Path]:
    paths: list[Path] = []
    paths.extend(sorted(dtb_dir.glob(f"sm8250-xiaomi-{codename}*.dtbo")))
    exact = dtb_dir / f"sm8250-xiaomi-{codename}.dtb"
    paths.append(exact)
    paths.extend(sorted(dtb_dir.glob(f"sm8250-xiaomi-{codename}-*.dtb")))
    seen: set[Path] = set()
    out: list[Path] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out


def collect_entries(board_ids: dict[str, dict[str, int]], dtb_dir: Path) -> list[tuple[str, bytes, dict[str, int]]]:
    entries: list[tuple[str, bytes, dict[str, int]]] = []
    for codename in sorted(board_ids):
        for path in candidate_dtb_paths(dtb_dir, codename):
            if path.is_file():
                entries.append((path.stem.removeprefix("sm8250-xiaomi-"), path.read_bytes(), board_ids[codename]))
                break
        else:
            print(f"WARNING: no DTB/DTBO found for {codename}", file=sys.stderr)
    return entries


def build_dtbo_image(entries: list[tuple[str, bytes, dict[str, int]]], output: Path) -> None:
    if not entries:
        raise ValueError("no DTB/DTBO entries to pack")

    table_offset = HEADER_SIZE
    data_offset = table_offset + len(entries) * ENTRY_SIZE
    entry_table = bytearray(len(entries) * ENTRY_SIZE)
    payload = bytearray()

    for index, (name, data, metadata) in enumerate(entries):
        if not data:
            raise ValueError(f"empty DTB/DTBO payload for {name}")
        entry_offset = index * ENTRY_SIZE
        dt_offset = data_offset + len(payload)
        struct.pack_into(">I", entry_table, entry_offset, len(data))
        struct.pack_into(">I", entry_table, entry_offset + 4, dt_offset)
        board_id = int(metadata.get("board_id", 0))
        msm_id = int(metadata.get("msm_id", 0))
        struct.pack_into(">I", entry_table, entry_offset + 8, board_id)
        struct.pack_into(">I", entry_table, entry_offset + 12, msm_id)
        struct.pack_into(">I", entry_table, entry_offset + 16, board_id)
        struct.pack_into(">I", entry_table, entry_offset + 20, msm_id)
        payload.extend(data)
        if len(payload) % 4:
            payload.extend(b"\0" * (4 - len(payload) % 4))

    total_size = align(data_offset + len(payload))
    header = bytearray(HEADER_SIZE)
    struct.pack_into(">I", header, 0, DT_TABLE_MAGIC)
    struct.pack_into(">I", header, 4, total_size)
    struct.pack_into(">I", header, 8, HEADER_SIZE)
    struct.pack_into(">I", header, 12, ENTRY_SIZE)
    struct.pack_into(">I", header, 16, len(entries))
    struct.pack_into(">I", header, 20, table_offset)
    struct.pack_into(">I", header, 24, PAGE_SIZE)
    struct.pack_into(">I", header, 28, VERSION)

    image = header + entry_table + payload
    image.extend(b"\0" * (total_size - len(image)))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(image)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an Android dtbo.img from kernel-built DTBs/DTBOs")
    parser.add_argument("--board-ids", required=True)
    parser.add_argument("--dtb-dir", required=True)
    parser.add_argument("--output", default="artifacts/dtbo.img")
    args = parser.parse_args(argv)

    board_ids = load_board_ids(Path(args.board_ids))
    entries = collect_entries(board_ids, Path(args.dtb_dir))
    build_dtbo_image(entries, Path(args.output))
    print(f"dtbo.img written: {args.output} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
