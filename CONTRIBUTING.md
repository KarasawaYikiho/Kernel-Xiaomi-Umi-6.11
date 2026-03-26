# Contributing

[中文贡献指南（CONTRIBUTING.zh-CN.md）](./CONTRIBUTING.zh-CN.md)

Thanks for improving **Kernel-Xiaomi-Umi**.

## Scope

This repository is a **porting orchestrator** (workflow + scripts + diagnostics), not a full kernel source tree.

## Before You Start

1. Read `README.md`
2. Read `Porting/README.md`
3. Read `Tools/Porting/README.md`
4. Check latest `PORTING_PLAN.md` and `Porting/CHANGELOG.md`

## Branch Strategy

Follow `Porting/BRANCHING.md`:

- `port/phase*` for phase work
- `port/hotfix-*` for urgent fixes

## Pull Request Requirements

Use the PR template and include:

- What changed and why
- Validation evidence (run/artifacts/local sanity check)
- Risk and rollback notes for workflow/script changes

## Reference Source Policy

Approved external references:

- `SO-TS/android_kernel_xiaomi_sm8250`
- `yefxx/xiaomi-umi-linux-kernel`
- `UtsavBalar1231/android_kernel_xiaomi_sm8150`
- `UtsavBalar1231/display-drivers`
- `UtsavBalar1231/camera-kernel`
- Author-ID discovery source: `liyafe1997` (Strawing)

Rules:

- Treat author IDs as discovery inputs; select concrete repos before integration.
- Use references as donor/comparison inputs only.
- No blind subtree copy.
- No proprietary ROM blob import.

## Quality Expectations

- Update docs when behavior/outputs change.
- Prefer reproducible CI changes over local-only tweaks.
- Place new diagnostics under `Tools/Porting/` and document them.
- Keep `Porting/CHANGELOG.md` milestone-focused and concise.

## Security

- Do not commit secrets/tokens.
- Keep `.gitignore` clean.
- Treat generated artifacts as disposable unless intentionally tracked.
