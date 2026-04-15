# Contributing

Thanks for improving Kernel-Xiaomi-Umi.

## Scope

Porting orchestrator (workflow + scripts + diagnostics), not kernel source.

## Before You Start

1. Read `README.md`
2. Read `Porting-Plan.md`
3. Check `Porting/CHANGELOG.md`

## Branch Strategy

- `port/phase*` — Phase work
- `port/hotfix-*` — Urgent fixes

## PR Requirements

- What changed and why
- Validation evidence
- Risk notes for workflow/script changes

## Source Rules

Reference sources are listed in `README.md` and `Porting/README.md`.

- Author IDs are discovery inputs
- No blind subtree copy
- No proprietary blob import

## Quality

- Update docs when behavior changes
- Require CI evidence
- Keep `CHANGELOG.md` concise
- Follow the repository hygiene rules in `README.md`

## Security

- No secrets in commit
- Keep `.gitignore` clean
