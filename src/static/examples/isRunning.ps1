$ErrorActionPreference = "Stop"

if ( -not (Test-Path "$PSScriptRoot\LOGS\status.txt")) {
    # onstart finished, must exist
    [Console]::Error.WriteLine("can not found status.txt after onstart.")
    Exit 0
}
else {
    # if status contain fail exit 1
    $status = Get-Content .\LOGS\status.txt
    if ($status -eq "PASS") {
        Exit 1
    }
    else {
        Exit -1
    }
}
