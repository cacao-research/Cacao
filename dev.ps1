# Cacao dev launcher.
#
# Usage:
#   .\dev.ps1                  # run example app (default)
#   .\dev.ps1 run              # run example app
#   .\dev.ps1 validate         # watch Python + JS files and validate on changes
#   .\dev.ps1 build            # build frontend assets

param(
    [ValidateSet("run", "validate", "build")]
    [string]$Mode = "run"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$procs = @()

# --- Helper: kill a process and its entire child tree ---
function Stop-ProcessTree([int]$ParentId) {
    Get-CimInstance Win32_Process -Filter "ParentProcessId=$ParentId" -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-ProcessTree $_.ProcessId }
    Stop-Process -Id $ParentId -Force -ErrorAction SilentlyContinue
}

# --- build mode ---
if ($Mode -eq "build") {
    Write-Host "[dev] Building frontend..." -ForegroundColor Cyan
    Push-Location "$Root\cacao\frontend"
    & npm run build
    Pop-Location
    Write-Host "[dev] Done." -ForegroundColor Green
    return
}

# --- validate mode ---
if ($Mode -eq "validate") {
    $pyPath = "$Root\cacao"
    $jsPath = "$Root\cacao\frontend\src"
    Write-Host "[dev] Watching for lint + type + test errors" -ForegroundColor Cyan
    Write-Host "[dev]   Python : $pyPath" -ForegroundColor DarkGray
    Write-Host "[dev]   JS/LESS: $jsPath" -ForegroundColor DarkGray
    Write-Host "[dev] Press Ctrl+C to stop." -ForegroundColor DarkGray
    Write-Host ""

    function Invoke-AllLint {
        $ts = Get-Date -Format "HH:mm:ss"
        Write-Host "[$ts] " -ForegroundColor DarkGray -NoNewline
        Write-Host "Running linters..." -ForegroundColor Cyan
        Write-Host ""

        # --- Python: ruff check (auto-fix) ---
        Write-Host "  ruff check      " -ForegroundColor Cyan -NoNewline
        $out = & ruff check $pyPath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "ok" -ForegroundColor Green
        } else {
            $fixOut = & ruff check --fix --unsafe-fixes $pyPath 2>&1
            if ($LASTEXITCODE -eq 0) {
                $fixed = ($out | Select-String "^\[").Count
                Write-Host "fixed $fixed issues" -ForegroundColor Yellow
            } else {
                Write-Host "fail" -ForegroundColor Red
                $fixOut | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
            }
        }

        # --- Python: ruff format (auto-fix) ---
        Write-Host "  ruff format     " -ForegroundColor Cyan -NoNewline
        $out = & ruff format --check $pyPath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "ok" -ForegroundColor Green
        } else {
            & ruff format $pyPath 2>&1 | Out-Null
            $fixed = ($out | Select-String "^Would reformat:").Count
            Write-Host "fixed $fixed files" -ForegroundColor Yellow
        }

        # --- Python: mypy type check ---
        Write-Host "  mypy            " -ForegroundColor Cyan -NoNewline
        $out = & mypy $pyPath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "ok" -ForegroundColor Green
        } else {
            $errCount = ($out | Select-String "^Found \d+ error").Count
            if ($errCount -gt 0) {
                $summary = ($out | Select-String "^Found \d+ error").Line
                Write-Host "fail ($summary)" -ForegroundColor Red
            } else {
                Write-Host "fail" -ForegroundColor Red
            }
            $out | Where-Object { $_ -match "error:" } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        }

        # --- Frontend: build ---
        Write-Host "  frontend build  " -ForegroundColor Cyan -NoNewline
        Push-Location "$Root\cacao\frontend"
        $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
        $out = & npm run build 2>&1
        $exitCode = $LASTEXITCODE
        $ErrorActionPreference = $savedEAP
        Pop-Location
        if ($exitCode -eq 0) {
            Write-Host "ok" -ForegroundColor Green
        } else {
            Write-Host "fail" -ForegroundColor Red
            $out | Where-Object { $_ -match "error|Error" } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        }

        # --- Python: pytest ---
        Write-Host "  pytest          " -ForegroundColor Cyan -NoNewline
        $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
        $out = & pytest --tb=short -q 2>&1
        $ErrorActionPreference = $savedEAP
        if ($LASTEXITCODE -eq 0) {
            $passLine = ($out | Select-String "passed").Line
            if ($passLine) {
                Write-Host "ok ($passLine)" -ForegroundColor Green
            } else {
                Write-Host "ok" -ForegroundColor Green
            }
        } elseif ($LASTEXITCODE -eq 5) {
            Write-Host "skipped (no tests)" -ForegroundColor Yellow
        } else {
            $failLine = ($out | Select-String "failed|error").Line | Select-Object -First 1
            if ($failLine) {
                Write-Host "fail ($failLine)" -ForegroundColor Red
            } else {
                Write-Host "fail" -ForegroundColor Red
            }
            $out | Where-Object { $_ -match "FAILED|ERROR" } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        }

        Write-Host ""
    }

    Invoke-AllLint

    # Watch Python and JS/LESS files
    $pyWatcher = [System.IO.FileSystemWatcher]::new($pyPath, "*.py")
    $pyWatcher.IncludeSubdirectories = $true
    $pyWatcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor
                              [System.IO.NotifyFilters]::FileName -bor
                              [System.IO.NotifyFilters]::CreationTime
    $pyWatcher.EnableRaisingEvents = $true

    $jsWatcher = [System.IO.FileSystemWatcher]::new($jsPath)
    $jsWatcher.IncludeSubdirectories = $true
    $jsWatcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor
                              [System.IO.NotifyFilters]::FileName -bor
                              [System.IO.NotifyFilters]::CreationTime
    $jsWatcher.EnableRaisingEvents = $true

    $lastRun = [datetime]::MinValue

    $handler = {
        $now = Get-Date
        $script:lastChange = $now
    }

    $script:lastChange = [datetime]::MinValue

    Register-ObjectEvent $pyWatcher Changed -Action $handler | Out-Null
    Register-ObjectEvent $pyWatcher Created -Action $handler | Out-Null
    Register-ObjectEvent $pyWatcher Renamed -Action $handler | Out-Null
    Register-ObjectEvent $jsWatcher Changed -Action $handler | Out-Null
    Register-ObjectEvent $jsWatcher Created -Action $handler | Out-Null
    Register-ObjectEvent $jsWatcher Renamed -Action $handler | Out-Null

    try {
        while ($true) {
            Start-Sleep -Milliseconds 500
            if ($script:lastChange -ne [datetime]::MinValue -and
                ((Get-Date) - $script:lastChange).TotalMilliseconds -gt 800 -and
                $script:lastChange -ne $lastRun) {
                $lastRun = $script:lastChange
                Invoke-AllLint
            }
        }
    } finally {
        $pyWatcher.Dispose()
        $jsWatcher.Dispose()
        Get-EventSubscriber | Unregister-Event
        Write-Host "[dev] Watcher stopped." -ForegroundColor Green
    }
    return
}

# --- run mode ---

# Kill stale processes on default port
$port = 1502
$stalePids = @()
$lines = netstat -ano | Select-String ":$port\s"
foreach ($line in $lines) {
    if ($line -match '\s(\d+)\s*$') {
        $pid = [int]$Matches[1]
        if ($pid -ne 0 -and $stalePids -notcontains $pid) { $stalePids += $pid }
    }
}
foreach ($stalePid in $stalePids) {
    Write-Host "[dev] Killing stale process on port $port (PID $stalePid)" -ForegroundColor Yellow
    Stop-ProcessTree $stalePid
}

# Clear __pycache__
Write-Host "[dev] Clearing __pycache__..." -ForegroundColor DarkGray
Get-ChildItem -Path "$Root\cacao" -Recurse -Directory -Filter __pycache__ |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Ensure editable install
Write-Host "[dev] Syncing editable install..." -ForegroundColor DarkGray
$savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
Push-Location $Root
$out = & pip install -e ".[dev]" -q 2>&1
if ($LASTEXITCODE -ne 0) { Write-Host "[dev]   install FAILED: $out" -ForegroundColor Red }
else { Write-Host "[dev]   cacao -> $Root (editable)" -ForegroundColor DarkGray }
Pop-Location
$ErrorActionPreference = $savedEAP

# Find an example app to run
$exampleApp = "$Root\examples\chat\app.py"
if (-not (Test-Path $exampleApp)) {
    $exampleApp = Get-ChildItem -Path "$Root\examples" -Filter "app.py" -Recurse | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $exampleApp) {
    Write-Host "[dev] No example app found in examples/" -ForegroundColor Red
    return
}

Write-Host "[dev] cacao run -> " -ForegroundColor Cyan -NoNewline
Write-Host "http://127.0.0.1:$port" -ForegroundColor Green
Write-Host "[dev] App: $exampleApp" -ForegroundColor DarkGray
$procs += Start-Process -NoNewWindow -PassThru -FilePath "cacao" `
    -ArgumentList "run", $exampleApp

Write-Host "[dev] Running. Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

try {
    while ($true) {
        foreach ($p in $procs) {
            if ($p.HasExited) { throw "exit" }
        }
        Start-Sleep -Milliseconds 500
    }
} catch {} finally {
    Write-Host ""
    Write-Host "[dev] Shutting down..." -ForegroundColor Cyan
    foreach ($p in $procs) {
        if (-not $p.HasExited) { Stop-ProcessTree $p.Id }
    }
    Write-Host "[dev] Done." -ForegroundColor Green
}
