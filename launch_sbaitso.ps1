# SBAITSO AI Launcher
# Double-click this file or run: powershell -ExecutionPolicy Bypass -File launch_sbaitso.ps1

param(
    [switch]$NoNewWindow = $false
)

# Get the script's directory (where this launcher is)
$scriptDir = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($scriptDir)) {
    $scriptDir = (Get-Location).Path
}

$dosboxPath = Join-Path $scriptDir "ressources\dosbox-x\dosbox-x.exe"
$sbaitsoPath = Join-Path $scriptDir "ressources\SBAITSO"
$pythonScript = Join-Path $scriptDir "sbaitso_ai.py"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   SBAITSO AI - Dr. SBAITSO" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Script Directory: $scriptDir" -ForegroundColor DarkGray
Write-Host ""

# ===== DEPENDENCY CHECKS =====
Write-Host "Checking dependencies..." -ForegroundColor Yellow
Write-Host ""

$allOk = $true

# Check 1: Python installation
Write-Host "▶ Checking Python..." -NoNewline
$pythonExe = $null
try {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
    $pythonVersion = & $pythonExe --version 2>&1
    Write-Host " OK" -ForegroundColor Green
    Write-Host "  $pythonVersion" -ForegroundColor DarkGray
}
catch {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Install from: https://python.org" -ForegroundColor Yellow
    $allOk = $false
}

# Check 2: sbaitso_ai.py exists
Write-Host "▶ Checking sbaitso_ai.py..." -NoNewline
if (Test-Path $pythonScript) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: sbaitso_ai.py not found at $pythonScript" -ForegroundColor Red
    $allOk = $false
}

# Check 3: sbaitso_tts.py exists
Write-Host "▶ Checking sbaitso_tts.py..." -NoNewline
$ttsPy = Join-Path $scriptDir "sbaitso_tts.py"
if (Test-Path $ttsPy) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: sbaitso_tts.py not found at $ttsPy" -ForegroundColor Red
    $allOk = $false
}

# Check 4: DOSBox-X installation
Write-Host "▶ Checking DOSBox-X..." -NoNewline
$dosboxFound = $null
if (Test-Path $dosboxPath) {
    $dosboxFound = $dosboxPath
    Write-Host " OK" -ForegroundColor Green
    Write-Host "  Found: $dosboxPath" -ForegroundColor DarkGray
}
else {
    # Try system PATH
    try {
        $dosboxFound = (Get-Command dosbox-x -ErrorAction Stop).Source
        Write-Host " OK (from PATH)" -ForegroundColor Green
        Write-Host "  Found: $dosboxFound" -ForegroundColor DarkGray
    }
    catch {
        # Try common installation locations
        $commonPaths = @(
            "C:\Program Files\dosbox-x\dosbox-x.exe",
            "C:\dosbox-x\dosbox-x.exe"
        )
        foreach ($path in $commonPaths) {
            if (Test-Path $path) {
                $dosboxFound = $path
                Write-Host " OK (common location)" -ForegroundColor Green
                Write-Host "  Found: $path" -ForegroundColor DarkGray
                break
            }
        }
        
        if (-not $dosboxFound) {
            Write-Host " WARNING" -ForegroundColor Yellow
            Write-Host "  DOSBox-X not found in standard locations" -ForegroundColor Yellow
            Write-Host "  Will attempt to find in system PATH at runtime" -ForegroundColor Yellow
        }
    }
}

# Check 5: SBAITSO directory
Write-Host "▶ Checking SBAITSO directory..." -NoNewline
if (Test-Path $sbaitsoPath) {
    Write-Host " OK" -ForegroundColor Green
    $readExe = Join-Path $sbaitsoPath "READ.EXE"
    if (Test-Path $readExe) {
        Write-Host "  READ.EXE found" -ForegroundColor DarkGray
    } else {
        Write-Host "  WARNING: READ.EXE not found in SBAITSO directory" -ForegroundColor Yellow
    }
} else {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: SBAITSO directory not found at $sbaitsoPath" -ForegroundColor Red
    $allOk = $false
}

# Check 6: Required Python packages
if ($pythonExe) {
    Write-Host "▶ Checking Python packages..." -NoNewline
    try {
        # Check if urllib is available (part of stdlib)
        & $pythonExe -c "import urllib.request" 2>$null
        Write-Host " OK" -ForegroundColor Green
    }
    catch {
        Write-Host " WARNING" -ForegroundColor Yellow
        Write-Host "  Some packages may be missing" -ForegroundColor Yellow
    }
}

Write-Host ""

# ===== FINAL VERDICT =====
if (-not $allOk) {
    Write-Host "ERROR: Some dependencies are missing or misconfigured." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "All dependencies OK!" -ForegroundColor Green
Write-Host ""

# Check and prompt for GROQ_API_KEY
if (-not $env:GROQ_API_KEY) {
    Write-Host "GROQ_API_KEY is not set in environment variables." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please enter your Groq API Key (get one from https://console.groq.com):" -ForegroundColor Cyan
    $apiKey = Read-Host "GROQ_API_KEY"
    
    if ([string]::IsNullOrWhiteSpace($apiKey)) {
        Write-Host "ERROR: API key cannot be empty!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Set environment variable for this session
    $env:GROQ_API_KEY = $apiKey
    Write-Host "API Key set for this session." -ForegroundColor Green
    
    # Optionally save to user environment variables
    Write-Host ""
    Write-Host "Would you like to save this API key to your Windows environment variables?" -ForegroundColor Cyan
    Write-Host "This way you won't need to enter it next time." -ForegroundColor Cyan
    $saveChoice = Read-Host "Enter 'yes' or 'no'"
    
    if ($saveChoice -eq "yes" -or $saveChoice -eq "y") {
        try {
            [Environment]::SetEnvironmentVariable("GROQ_API_KEY", $apiKey, [EnvironmentVariableTarget]::User)
            Write-Host "API Key saved to user environment variables!" -ForegroundColor Green
            Write-Host "NOTE: You may need to restart PowerShell for the change to take effect globally." -ForegroundColor Yellow
        }
        catch {
            Write-Host "ERROR: Could not save API key to environment variables: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "GROQ_API_KEY found in environment variables." -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting SBAITSO AI..." -ForegroundColor Cyan
Write-Host ""

# Build the command with proper paths
$args = @($pythonScript)
# Only pass explicit paths if they were found; otherwise let Python auto-detect
if ($dosboxFound) {
    $args += "--dosbox"
    $args += $dosboxFound
}

# Run the Python script
Write-Host "Launching: python $($args -join ' ')" -ForegroundColor DarkGray
Write-Host ""

& $pythonExe @args

# Keep window open if there was an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Script exited with error code: $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to close"
}
