Set-Location $PSScriptRoot
if (-not (Test-Path "LOGS")) {
    mkdir LOGS
}
# ====================================================
$RESULT_PATH = "$PSScriptRoot\LOGS\result.txt"
$STATUS_PATH = "$PSScriptRoot\LOGS\status.txt"
# ====================================================


try {
    Write-Output "$env:PROJECT_NAME $env:VERSION" 
    Get-ChildItem env:* | sort-object name > .\LOGS\monitorOnStopEnvs.log

    # using the parent folder name as the unique id
    $task_id = (Get-Item $PSScriptRoot).Parent.Name
    $task_id2 = (Get-Item $PSScriptRoot).Name
    $task_name_instance = "{0}_{1}_instance" -f $task_id, $task_id2
    $task_name_watchdog = "{0}_{1}_watchdog" -f $task_id, $task_id2

    Stop-ScheduledTask -TaskName $task_name_instance
    Unregister-ScheduledTask -TaskName $task_name_instance -Confirm:$false

    # delete watch log (can not delete self by powershell, so the schtasks)
    # Stop-ScheduledTask -TaskName $task_name_watchdog
    # Unregister-ScheduledTask -TaskName $task_name_watchdog -Confirm:$false
    cmd.exe /c schtasks /end /tn  $task_name_watchdog
    cmd.exe /c schtasks /delete /tn  $task_name_watchdog /f
    if (-not(Test-Path $STATUS_PATH)) {
        Add-Content -Path $RESULT_PATH -Value "PASS" -Encoding UTF8
        Add-Content -Path $STATUS_PATH -Value "PASS" -Encoding UTF8
    }
}
catch {
    $Error[0]
    $ErrorMsg = $Error[0]
    Add-Content -Path $RESULT_PATH -Value "$ErrorMsg" -Encoding UTF8
    Add-Content -Path $STATUS_PATH -Value "FAIL" -Encoding UTF8
}

