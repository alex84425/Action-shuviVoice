$ErrorActionPreference = "Stop"

if ( -not (Test-Path  .\LOGS\status.txt)) {
    # onstart finished, must exist
    [Console]::Error.WriteLine("can not found status.txt after onstart.")
    exit 1
}
else {
    # if status contain fail exit 1
    $status = Get-Content LOGS\status.txt
    if ($status -ne "PASS") {
        [Console]::Error.WriteLine("found FAIL in status.txt")
        exit 1
    }
    $process = Get-Process "powershell"  -ErrorAction SilentlyContinue
    if ( $process) {
        [Console]::Error.WriteLine("process running")
        exit 0
    }
    else {
        [Console]::Error.WriteLine("process not found")
        exit 1
    }
}
