# Security Policy

## Supported Scope

This repository is an orchestration/tooling project.
Security fixes apply to:

- GitHub workflows
- Scripts under `Tools/Porting/`
- Documentation that can affect secure operation

## Reporting a Vulnerability

Please open a private security report through GitHub Security Advisories when possible.
If unavailable, open an issue with minimal reproduction details (without sensitive data) and mark it as security-related.

Include:

- Affected file(s) and path(s)
- Impact description
- Reproduction steps
- Suggested fix (optional)

## Response Expectations

- Initial triage target: within 72 hours
- Status updates: provided during investigation
- Confirmed issues: patched with changelog note and risk summary

## Sensitive Data Rules

- Never commit tokens, credentials, or private keys.
- Keep build artifacts free of secrets.
- Avoid embedding local machine paths in externally shared reports unless required for diagnosis.
