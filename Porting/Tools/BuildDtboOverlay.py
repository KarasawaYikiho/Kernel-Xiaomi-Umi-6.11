#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Sequence


def find_dtc(out_dir: Path = Path("out")) -> str:
    for candidate in (out_dir / "scripts" / "dtc" / "dtc", Path("scripts") / "dtc" / "dtc"):
        if candidate.is_file():
            return str(candidate)
    return "dtc"


def decompile_dtb(dtb: Path, dtc: str) -> str:
    result = subprocess.run(
        [dtc, "-I", "dtb", "-O", "dts", "-s", str(dtb)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to decompile {dtb}")
    return result.stdout


def compile_overlay(dts: str, output: Path, dtc: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [dtc, "-I", "dts", "-O", "dtb", "-@", "-o", str(output), "-"],
        input=dts,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to compile {output}")


def generate_overlay_dts(board_id: int, msm_id: int, device_nodes: dict[str, str]) -> str:
    lines = ["/dts-v1/;", "/plugin/;", "", "/ {"]
    lines.extend(
        [
            "\tfragment@0 {",
            '\t\ttarget-path = "/";',
            "\t\t__overlay__ {",
            f"\t\t\tqcom,board-id = <0x{board_id:x}>;",
            f"\t\t\tqcom,msm-id = <{msm_id} 0x20001>;",
            "\t\t};",
            "\t};",
        ]
    )
    for index, (label, body) in enumerate(sorted(device_nodes.items()), start=1):
        safe_label = label.strip().lstrip("&")
        lines.extend(
            [
                f"\tfragment@{index} {{",
                f"\t\ttarget = <&{safe_label}>;",
                "\t\t__overlay__ {",
            ]
        )
        for raw in body.splitlines():
            line = raw.strip()
            if line:
                lines.append(f"\t\t\t{line}")
        lines.extend(["\t\t};", "\t};"])
    lines.append("};")
    return "\n".join(lines) + "\n"


def extract_overlay_nodes_from_dts(device_dts: str) -> dict[str, str]:
    # Conservative first framework: preserve explicit &label overlays already present in DTS.
    # Full structural DTB diffing is intentionally left to later device-specific tuning.
    nodes: dict[str, str] = {}
    marker = "&"
    pos = 0
    while True:
        start = device_dts.find(marker, pos)
        if start < 0:
            break
        brace = device_dts.find("{", start)
        if brace < 0:
            break
        label = device_dts[start + 1 : brace].strip().split()[0]
        depth = 1
        cur = brace + 1
        while cur < len(device_dts) and depth:
            if device_dts[cur] == "{":
                depth += 1
            elif device_dts[cur] == "}":
                depth -= 1
            cur += 1
        body = device_dts[brace + 1 : cur - 1].strip()
        if label and body:
            nodes[label] = body
        pos = cur
    return nodes


def build_overlay(device_dtb: Path, output: Path, board_id: int, msm_id: int, out_dir: Path) -> None:
    dtc = find_dtc(out_dir)
    device_dts = decompile_dtb(device_dtb, dtc)
    nodes = extract_overlay_nodes_from_dts(device_dts)
    overlay = generate_overlay_dts(board_id, msm_id, nodes)
    dts_out = output.with_suffix(".dts")
    dts_out.write_text(overlay, encoding="utf-8")
    compile_overlay(overlay, output, dtc)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a DTBO overlay scaffold from a kernel-built DTB")
    parser.add_argument("--device-dtb", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--board-id", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--msm-id", type=int, default=356)
    parser.add_argument("--out-dir", default="out")
    args = parser.parse_args(argv)
    build_overlay(Path(args.device_dtb), Path(args.output), args.board_id, args.msm_id, Path(args.out_dir))
    print(f"dtbo overlay written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
