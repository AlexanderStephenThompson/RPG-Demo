# Run both pytest tests and doctests
# Usage: powershell -ExecutionPolicy Bypass -File .\scripts\run_all_tests.ps1

Write-Host "Running pytest tests..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe -m pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPytest tests failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`n`nRunning doctests..." -ForegroundColor Cyan
$doctest_files = @(
    "src\rpg\entities\character.py",
    "src\rpg\entities\item.py",
    "src\rpg\services\inventory.py",
    "src\rpg\services\shop.py",
    "src\rpg\services\bank.py",
    "src\rpg\systems\combat.py"
)

$failed = 0
foreach ($file in $doctest_files) {
    Write-Host "  Testing $file..." -NoNewline
    & .\.venv\Scripts\python.exe -m doctest $file 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAILED" -ForegroundColor Red
        $failed++
        & .\.venv\Scripts\python.exe -m doctest $file -v
    }
}

if ($failed -gt 0) {
    Write-Host "`n$failed doctest file(s) failed!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`nAll tests passed!" -ForegroundColor Green
}
