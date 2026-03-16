#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ART = Path("artifacts")
MANIFEST = ART / "driver-integration-manifest.txt"
OUT = ART / "driver-integration-manifest-sync.txt"

REFERENCE_REPORT = Path("Porting/Reference-Drivers-Analysis.md")
ROM_REPORT = Path("Porting/OfficialRom-Umi-Os1.0.5.0-Analysis.md")

BASE_REQUIRED = [
    "display_pipeline",
    "audio_stack",
    "camera_sensor_module",
    "camera_isp_path",
    "thermal_power_tuning",
]

REF_REQUIRED = [
    "ref_driver_xiaomi_path_alignment",
    "ref_driver_camera_path_alignment",
    "ref_driver_display_path_alignment",
    "ref_driver_thermal_path_alignment",
]

ROM_REQUIRED = [
    "rom_boot_chain_consistency",
    "rom_dtbo_consistency",
    "rom_vbmeta_consistency",
    "rom_dynamic_partition_baseline",
]


def _normalize_item(s: str) -> str:
    return s.strip().lower().replace(" ", "_")


def _read_manifest() -> tuple[list[str], set[str], set[str], set[str]]:
    comments: list[str] = []
    integrated: set[str] = set()
    pending: set[str] = set()
    unknown: set[str] = set()

    if not MANIFEST.exists():
        return comments, integrated, pending, unknown

    for raw in MANIFEST.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            comments.append("")
            continue
        if line.startswith("#"):
            comments.append(line)
            continue
        if line.startswith("integrated:"):
            item = _normalize_item(line.split(":", 1)[1])
            if item:
                integrated.add(item)
            continue
        if line.startswith("pending:"):
            item = _normalize_item(line.split(":", 1)[1])
            if item:
                pending.add(item)
            continue
        unknown.add(line)

    return comments, integrated, pending, unknown


def _has_text(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle.lower() in path.read_text(encoding="utf-8", errors="ignore").lower()


def _detect_dynamic_partition_signal() -> bool:
    return (
        _has_text(ROM_REPORT, "dynamic partition")
        or _has_text(ROM_REPORT, "dynamic_partitions_op_list")
        or _has_text(ROM_REPORT, "dynamic partitions operation")
    )


def main() -> int:
    ART.mkdir(parents=True, exist_ok=True)

    comments, integrated, pending, unknown = _read_manifest()

    required = {_normalize_item(x) for x in BASE_REQUIRED + REF_REQUIRED + ROM_REQUIRED}

    # If reports are missing, keep related tasks pending explicitly.
    reference_ready = REFERENCE_REPORT.exists()
    rom_ready = ROM_REPORT.exists()

    if not reference_ready:
        required.add("reference_driver_analysis_generation")
    if not rom_ready:
        required.add("official_rom_baseline_generation")

    # ROM evidence checks: if we have report but key signals are missing, keep explicit pending items.
    if rom_ready and not _detect_dynamic_partition_signal():
        required.add("rom_dynamic_partition_baseline")

    # Ensure every required item is either integrated or pending.
    for item in required:
        if item not in integrated:
            pending.add(item)

    # integrated wins over pending when both exist.
    pending = {x for x in pending if x not in integrated}

    out_lines: list[str] = []
    out_lines.append("# Driver integration manifest")
    out_lines.append("# Mark completed work with: integrated:<item>")
    out_lines.append("# Keep unfinished work as: pending:<item>")
    out_lines.append("# Auto-synced by Tools/Porting/Sync_Driver_Integration_Manifest.py")
    out_lines.append("")
    out_lines.append("# Core integration backlog")
    for item in sorted({ _normalize_item(x) for x in BASE_REQUIRED }):
        prefix = "integrated" if item in integrated else "pending"
        out_lines.append(f"{prefix}:{item}")

    out_lines.append("")
    out_lines.append("# Reference driver alignment backlog")
    for item in sorted({ _normalize_item(x) for x in REF_REQUIRED }):
        prefix = "integrated" if item in integrated else "pending"
        out_lines.append(f"{prefix}:{item}")

    out_lines.append("")
    out_lines.append("# Official ROM validation backlog")
    for item in sorted({ _normalize_item(x) for x in ROM_REQUIRED }):
        prefix = "integrated" if item in integrated else "pending"
        out_lines.append(f"{prefix}:{item}")

    extra_items = sorted((integrated | pending) - required)
    if extra_items:
        out_lines.append("")
        out_lines.append("# Extra custom items")
        for item in extra_items:
            prefix = "integrated" if item in integrated else "pending"
            out_lines.append(f"{prefix}:{item}")

    if unknown:
        out_lines.append("")
        out_lines.append("# Unknown legacy lines preserved for manual review")
        for raw in sorted(unknown):
            out_lines.append(f"# legacy:{raw}")

    MANIFEST.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    sync_lines = [
        f"status=ok",
        f"reference_report_ready={'yes' if reference_ready else 'no'}",
        f"rom_report_ready={'yes' if rom_ready else 'no'}",
        f"integrated_count={len(integrated)}",
        f"pending_count={len(pending)}",
        f"unknown_legacy_lines={len(unknown)}",
    ]
    OUT.write_text("\n".join(sync_lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
