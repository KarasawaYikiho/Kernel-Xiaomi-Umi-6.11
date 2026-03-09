#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


def parse_build_exit(path: Path) -> tuple[int | None, int | None]:
    defconfig_rc = None
    build_rc = None
    if not path.exists():
        return defconfig_rc, build_rc
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("defconfig_rc="):
            try:
                defconfig_rc = int(line.split("=", 1)[1].strip())
            except Exception:
                pass
        elif line.startswith("build_rc="):
            try:
                build_rc = int(line.split("=", 1)[1].strip())
            except Exception:
                pass
    return defconfig_rc, build_rc


def main() -> int:
    mode = (sys.argv[1] if len(sys.argv) > 1 else "warn").strip().lower()
    if mode not in {"warn", "strict"}:
        mode = "warn"

    root = Path.cwd()
    cfg_path = root / "porting" / "quality-gates.json"
    out_path = root / "artifacts" / "quality-gate.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    hard_fails: list[str] = []
    warns: list[str] = []

    if not cfg_path.exists():
        hard_fails.append(f"missing config: {cfg_path}")
    else:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        required_files = [Path(p) for p in cfg.get("required_files", [])]
        warn_files = [Path(p) for p in cfg.get("warn_files", [])]

        for p in required_files:
            if not (root / p).exists():
                hard_fails.append(f"missing required file: {p}")

        for p in warn_files:
            if not (root / p).exists():
                warns.append(f"missing optional file: {p}")

    defconfig_rc, build_rc = parse_build_exit(root / "artifacts" / "build-exit.txt")
    if defconfig_rc is None or build_rc is None:
        hard_fails.append("build-exit.txt missing parsable defconfig_rc/build_rc")
    else:
        if defconfig_rc != 0:
            hard_fails.append(f"defconfig_rc={defconfig_rc}")
        if build_rc != 0:
            hard_fails.append(f"build_rc={build_rc}")

    lines = [
        f"quality_gate_mode={mode}",
        f"hard_fail_count={len(hard_fails)}",
        f"warn_count={len(warns)}",
        ""
    ]
    if hard_fails:
        lines.append("[hard_fail]")
        lines.extend(f"- {x}" for x in hard_fails)
        lines.append("")
    if warns:
        lines.append("[warn]")
        lines.extend(f"- {x}" for x in warns)
        lines.append("")

    if not hard_fails and not warns:
        lines.append("quality_gate=clean")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    if mode == "strict" and hard_fails:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
