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

    $task = Get-ScheduledTask -TaskName $task_name_instance -ErrorAction SilentlyContinue
    if ($task) {
        Stop-ScheduledTask -TaskName $task_name_instance
        Unregister-ScheduledTask -TaskName $task_name_instance -Confirm:$false
    }

    # After kill the scheduler , make sure the process also killed
    # FIXME: please replace the "ProcessName" to your process name
    Get-Process -Name "ProcessName" -ErrorAction SilentlyContinue | Stop-Process -Force

    if (-not(Test-Path $STATUS_PATH)) {
        Add-Content -Path $RESULT_PATH -Value "PASS" -Encoding UTF8
        Add-Content -Path $STATUS_PATH -Value "PASS" -Encoding UTF8
    }
    # disable watch log (can not delete self by powershell)
    # Unregister-ScheduledTask -TaskName $task_name_watchdog -Confirm:$false
    $task = Get-ScheduledTask -TaskName $task_name_watchdog -ErrorAction SilentlyContinue
    if ($task) {
        Disable-ScheduledTask -TaskName $task_name_watchdog
        Stop-ScheduledTask -TaskName $task_name_watchdog
    }
}
catch {
    $Error[0]
    $ErrorMsg = $Error[0]
    Add-Content -Path $RESULT_PATH -Value "$ErrorMsg" -Encoding UTF8
    Add-Content -Path $STATUS_PATH -Value "FAIL" -Encoding UTF8
}

