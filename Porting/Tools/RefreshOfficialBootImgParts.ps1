param(
    [string]$OfficialBootImg = ''
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($OfficialBootImg)) {
    $configLines = python "Porting/Tools/ExportPortConfig.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to load port config defaults"
    }

    foreach ($line in $configLines) {
        if ($line -like 'OFFICIAL_BOOTIMG_DEFAULT=*') {
            $OfficialBootImg = $line.Substring('OFFICIAL_BOOTIMG_DEFAULT='.Length)
            break
        }
    }
}

if (-not (Test-Path -LiteralPath $OfficialBootImg -PathType Leaf)) {
    throw "Official boot image not found: $OfficialBootImg"
}

python "Porting/Tools/SplitOfficialBootImg.py" --input "$OfficialBootImg"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Refreshed split boot baseline from: $OfficialBootImg"
Write-Host "Review: Porting/OfficialRomBaseline/BootImgParts and Manifest.json"
