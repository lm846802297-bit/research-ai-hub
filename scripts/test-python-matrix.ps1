# Run the same Python test matrix locally on Windows without GitHub-hosted runners.
# Requires uv and network access to download managed Python interpreters/packages.
$ErrorActionPreference = "Stop"

$Uv = Get-Command uv -ErrorAction SilentlyContinue
if (-not $Uv) {
    throw "uv was not found. Install it from https://docs.astral.sh/uv/getting-started/installation/ and reopen PowerShell."
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $RepoRoot
try {
    $Versions = @("3.11", "3.12", "3.13")
    $Failures = [System.Collections.Generic.List[string]]::new()

    foreach ($Version in $Versions) {
        Write-Host ""
        Write-Host "========== Python $Version ==========" -ForegroundColor Cyan

        & uv python install $Version
        if ($LASTEXITCODE -ne 0) {
            $Failures.Add("$Version (interpreter installation)")
            continue
        }

        & uv run --isolated --python $Version --with-editable ".[dev]" python -m pytest -q
        if ($LASTEXITCODE -ne 0) {
            $Failures.Add("$Version (pytest)")
        }
    }

    if ($Failures.Count -gt 0) {
        Write-Host ""
        Write-Host "FAILED: $($Failures -join ', ')" -ForegroundColor Red
        exit 1
    }

    Write-Host ""
    Write-Host "PASS: Python 3.11, 3.12, and 3.13 test suites all passed." -ForegroundColor Green
}
finally {
    Pop-Location
}
