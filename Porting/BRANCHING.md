# Branching Strategy

- `main`: integration branch
- `port/phase0-*`: baseline lock/planning
- `port/phase1-*`: inventory/gap/classification
- `port/phase2-*`: migration/build/packaging pipeline
- `port/phase3-*`: subsystem feature ports
- `port/hotfix-*`: urgent CI/script fixes

## Merge Gate Checklist

- [ ] Workflow run completed with uploaded artifacts
- [ ] `phase2-report.txt` exists and is readable
- [ ] `build-exit.txt` status matches expected phase outcome
- [ ] Meaningful change noted in `CHANGELOG.md`
- [ ] README/docs updated when behavior changed
