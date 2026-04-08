#!/usr/bin/env bash
set -euo pipefail

mkdir -p artifacts
anykernel_ok=no
anykernel_has_imagegz=no
anykernel_has_dtb=no
anykernel_dtb_source=
anykernel_reason=imagegz-missing
imagegz_path=
template_source=

if [ -f out/arch/arm64/boot/Image.gz ]; then
  imagegz_path=out/arch/arm64/boot/Image.gz
elif [ -f artifacts/Image.gz ]; then
  imagegz_path=artifacts/Image.gz
fi

if [ -n "$imagegz_path" ]; then
  anykernel_has_imagegz=yes
  if [ -d anykernel3 ]; then
    template_source=existing-dir
  elif command -v git >/dev/null 2>&1; then
    anykernel_reason=clone-failed
    rm -rf anykernel3
    git clone --depth=1 https://github.com/osm0sis/AnyKernel3.git anykernel3 || true
    [ -d anykernel3 ] && template_source=git-clone
  else
    anykernel_reason=git-missing
  fi

  if [ -d anykernel3 ]; then
    if command -v zip >/dev/null 2>&1; then
      anykernel_reason=zip-build-failed
      cp -v "$imagegz_path" anykernel3/Image.gz || true

      # Optional: include first matched umi-related dtb as dtb
      if [ -s artifacts/umi_primary_dtb_paths.txt ]; then
        first_dtb="$(head -n1 artifacts/umi_primary_dtb_paths.txt)"
        if [ -f "$first_dtb" ]; then
          cp -v "$first_dtb" anykernel3/dtb || true
          anykernel_has_dtb=yes
          anykernel_dtb_source="$first_dtb"
        fi
      fi

      # Best-effort device hint
      sed -i 's/^device.name1=.*/device.name1=umi/' anykernel3/anykernel.sh || true

      if (cd anykernel3 && zip -r9 ../artifacts/AnyKernel3-umi-candidate.zip . -x ".git/*"); then
        anykernel_ok=yes
        anykernel_reason=ok
      fi
    else
      anykernel_reason=zip-command-missing
    fi
  fi
fi

{
  echo "anykernel_ok=$anykernel_ok"
  echo "reason=$anykernel_reason"
  echo "has_imagegz=$anykernel_has_imagegz"
  echo "imagegz_path=$imagegz_path"
  echo "has_dtb=$anykernel_has_dtb"
  echo "dtb_source=$anykernel_dtb_source"
  echo "template_source=$template_source"
} > artifacts/anykernel-info.txt
