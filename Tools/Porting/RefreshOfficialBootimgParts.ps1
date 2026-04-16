param(
    [string]$OfficialBootimg = 'D:\GIT\MIUI_UMI\boot.img'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $OfficialBootimg -PathType Leaf)) {
    throw "Official boot image not found: $OfficialBootimg"
}

python "Tools/Porting/SplitOfficialBootimg.py" --input "$OfficialBootimg"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Refreshed split boot baseline from: $OfficialBootimg"
Write-Host "Review: Porting/OfficialRomBaseline/boot.img.parts and Manifest.json"
