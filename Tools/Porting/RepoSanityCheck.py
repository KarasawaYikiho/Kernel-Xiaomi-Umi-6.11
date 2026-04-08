#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import py_compile

ROOT = Path(__file__).resolve().parents[2]
TOOLS_PORTING = ROOT / "Tools" / "Porting"
PORTING_DOCS = ROOT / "Porting"


def check_python_compile() -> list[str]:
    errs: list[str] = []
    py_files = sorted(TOOLS_PORTING.glob("*.py"))
    if not py_files:
        return ["no python files found under Tools/Porting"]
    for p in py_files:
        try:
            py_compile.compile(str(p), doraise=True)
        except Exception as e:  # pragma: no cover
            errs.append(f"py_compile failed: {p.relative_to(ROOT)} :: {e}")
    return errs


def check_workflow_script_refs() -> list[str]:
    errs: list[str] = []
    wf = ROOT / ".github" / "workflows" / "Phase2-Port-Umi.yml"
    if not wf.exists():
        return ["missing workflow: .github/workflows/Phase2-Port-Umi.yml"]
    text = wf.read_text(encoding="utf-8")

    sh_refs = re.findall(r"\./Tools/Porting/([\w\-]+\.sh)", text)
    py_refs = re.findall(r"python3?\s+Tools/Porting/([\w\-]+\.py)", text)

    for r in sorted(set(sh_refs)):
        if not (TOOLS_PORTING / r).exists():
            errs.append(f"missing script referenced by workflow: Tools/Porting/{r}")

    for r in sorted(set(py_refs)):
        if not (TOOLS_PORTING / r).exists():
            errs.append(f"missing python tool referenced by workflow: Tools/Porting/{r}")

    return errs


def check_markdown_links() -> list[str]:
    errs: list[str] = []
    md_files = list(ROOT.glob("*.md"))
    md_files += list(PORTING_DOCS.glob("*.md"))
    md_files += list(TOOLS_PORTING.glob("*.md"))

    for md in md_files:
        txt = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", txt):
            link = m.group(1).strip().strip("<>")
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if link.startswith("./"):
                link = link[2:]
            target = (md.parent / link).resolve()
            if not target.exists():
                errs.append(f"broken link: {md.relative_to(ROOT)} -> {link}")
    return errs


def main() -> int:
    errors = []
    errors.extend(check_python_compile())
    errors.extend(check_workflow_script_refs())
    errors.extend(check_markdown_links())

    report = {
        "ok": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
