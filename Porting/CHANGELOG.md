# Porting Changelog

> Milestone-only changelog.

## 2026-03-26

- Tightened the postprocess chain so local reruns now rebuild driver integration evidence, re-sync the manifest, and validate AnyKernel/boot image inputs before regenerating the consolidated phase2 report.
- Preserved existing `artifacts/runtime-validation-input.md` content during postprocess reruns to avoid wiping manual device-side validation results.
- Prefer the local official UMI ROM package as the first release `boot.img` fallback and expose ROM boot size/hash alignment in `bootimg-info.txt`.
- Raised artifact readiness from a DTB-only heuristic to a ROM-aware gate that also records release readiness, AnyKernel validity, DTB manifest hits, and official boot image alignment across reports, badges, and metrics.
- Hardened shell entrypoints to auto-detect `python3` or `python`, so local Windows reruns of postprocess/build helpers no longer fail just because `python3` is absent.

## 2026-03-11

- Refactored postprocess scripts to share a centralized KV parser (`Tools/Porting/Kv_Utils.py`), removing duplicated parsing logic.
- Kept decision/report chain behavior intact while reducing maintenance overhead.
- Performed repo-wide documentation rewrite for consistency and readability.

## 2026-03-09

- Added AnyKernel candidate zip packaging in Phase2 workflow (`AnyKernel3-umi-candidate.zip`).
- Expanded migration statistics and diagnostics/reporting chain.
- Improved workflow reliability with concurrency control and timeout handling.
- Simplified compile flow by removing obsolete quality-gate path.

## 2026-03-08

- Initialized 5+ porting orchestrator skeleton.
- Added capability inventory and first classification/gap outputs.
- Started automated Phase2 migration/build attempts for `umi`.
