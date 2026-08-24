param(
    [switch]$SkipLargeHashes
)

$ErrorActionPreference = 'Stop'
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$bundledPython = 'C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

if (Test-Path -LiteralPath $bundledPython) {
    $pythonExecutable = $bundledPython
} else {
    $pythonCommand = Get-Command python -ErrorAction Stop
    $pythonExecutable = $pythonCommand.Source
}

$primaryArchive = Join-Path $workspaceRoot 'data\raw\Hass-Avocado-Ripening-Photographic-Dataset-v1.zip'
$primaryExtract = Join-Path $workspaceRoot 'data\raw\hass_avocado_mendeley_v1'
if (-not (Test-Path -LiteralPath $primaryArchive -PathType Leaf)) {
    throw "Missing immutable primary archive: $primaryArchive"
}
if (-not (Test-Path -LiteralPath $primaryExtract -PathType Container)) {
    throw "Missing extracted primary dataset: $primaryExtract"
}

$previousLocation = (Get-Location).Path
$previousPythonPath = $env:PYTHONPATH
$previousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

function Invoke-PythonStep {
    param(
        [string]$Label,
        [string[]]$Arguments
    )
    Write-Host "==> $Label"
    & $pythonExecutable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

try {
    Set-Location -LiteralPath $workspaceRoot
    $env:PYTHONPATH = Join-Path $workspaceRoot 'tmp\python_deps'
    $env:PYTHONDONTWRITEBYTECODE = '1'

    Invoke-PythonStep -Label 'Prepare reconciled metadata and RGB features' `
        -Arguments @('analysis\prepare_rgb_dataset.py')
    Invoke-PythonStep -Label 'Regenerate exploratory analysis' `
        -Arguments @('analysis\run_eda.py')
    Invoke-PythonStep -Label 'Regenerate fruit-grouped ML baselines' `
        -Arguments @('ml\train_grouped_baselines.py')
    Invoke-PythonStep -Label 'Regenerate prototype overview figure' `
        -Arguments @('analysis\draw_prototype_overview.py')

    $validationArguments = @('reproducibility\validate_outputs.py', '--write-report')
    if ($SkipLargeHashes) {
        $validationArguments += '--skip-large-hashes'
    }
    Invoke-PythonStep -Label 'Validate generated outputs and provenance' `
        -Arguments $validationArguments

    Write-Host 'Reproduction completed successfully.'
} finally {
    Set-Location -LiteralPath $previousLocation
    $env:PYTHONPATH = $previousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $previousNoBytecode
}

