Set-Location $PSScriptRoot
if (-not (Test-Path "LOGS")) {
    mkdir LOGS
}
$taskId_filePath = "C:\TestAutomation\taskId.txt"
$content = Get-Content -Path $taskId_filePath

# Create monitor
$taskId_watcher = New-Object System.IO.FileSystemWatcher
$taskId_watcher.Path = (Split-Path -Path $taskId_filePath -Parent)
$taskId_watcher.Filter = (Split-Path -Path $taskId_filePath -Leaf)

# Monitor file modification
Register-ObjectEvent -InputObject $taskId_watcher -EventName Changed -SourceIdentifier taskId_Changed -Action {
    Write-Output "file_change" > taskId_changed.txt

    $newContent = Get-Content -Path $eventArgs.FullPath
    if ($newContent -ne $content) {
        .\monitorOnStop.ps1 >> .\LOGS\monitorOnStop.log
    }
}

# Keep monitor file modification
try {
    Wait-Event -SourceIdentifier taskId_Changed
}
finally {
    Unregister-Event -SourceIdentifier taskId_Changed
    $taskId_watcher.Dispose()
}
