#!/usr/bin/env bash
set -euo pipefail

# Run post-processing suite for phase2 artifacts.
# Usage: Run_Postprocess_Suite.sh

python_cmd=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -V >/dev/null 2>&1; then
    python_cmd="$cand"
    break
  fi
done

if [[ -z "$python_cmd" ]]; then
  echo "python interpreter not found" >&2
  exit 1
fi

steps=(
  "Build_Runtime_Validation_Template.py"
  "Parse_Runtime_Validation_Input.py"
  "Init_Driver_Integration_Manifest.py"
  "Build_Driver_Integration_Evidence.py"
  "Sync_Driver_Integration_Manifest.py"
  "Validate_Driver_Integration_Manifest.py"
  "Validate_Anykernel_Candidate.py"
  "Validate_Boot_Image.py"
  "Evaluate_Artifact.py"
  "Build_Driver_Integration_Status.py"
  "Build_Phase2_Report.py"
  "Suggest_Next_Focus.py"
  "Verify_Decision_Consistency.py"
  "Extract_Build_Errors.py"
  "Build_Artifact_Index.py"
  "Summarize_Artifacts_Markdown.py"
  "Validate_Phase2_Report.py"
  "Collect_Metrics_Json.py"
  "Build_Status_Badge_Line.py"
  "Build_Artifact_Checksums.py"
  "Build_Action_Validation_Checklist.py"
  "Build_Runtime_Validation_Summary.py"
  "Check_Artifact_Completeness.py"
)

status_file="artifacts/postprocess-status.txt"
mkdir -p "artifacts"
: > "$status_file"

for step in "${steps[@]}"; do
  script="Tools/Porting/${step}"
  if "$python_cmd" "$script"; then
    echo "${step}=ok" | tee -a "$status_file"
  else
    echo "${step}=failed" | tee -a "$status_file"
  fi
done
