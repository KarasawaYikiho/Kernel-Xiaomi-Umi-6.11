#!/usr/bin/env bash
set -euo pipefail

# Run post-processing suite for phase2 artifacts.
# Usage: Run_Postprocess_Suite.sh

python3 tools/porting/Check_Artifact_Completeness.py || true
python3 tools/porting/Validate_Anykernel_Candidate.py || true
python3 tools/porting/Validate_Boot_Image.py || true
python3 tools/porting/Suggest_Next_Focus.py || true
python3 tools/porting/Extract_Build_Errors.py || true
python3 tools/porting/Build_Artifact_Index.py || true
python3 tools/porting/Summarize_Artifacts_Markdown.py || true
python3 tools/porting/Validate_Phase2_Report.py || true
python3 tools/porting/Collect_Metrics_Json.py || true
python3 tools/porting/Build_Status_Badge_Line.py || true
python3 tools/porting/Build_Artifact_Checksums.py || true
python3 tools/porting/Build_Action_Validation_Checklist.py || true
