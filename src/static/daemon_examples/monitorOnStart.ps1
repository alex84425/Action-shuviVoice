Set-Location $PSScriptRoot
. .\TaskScheduler.ps1

# ====================================================
$DAEMON_NAME = "DummyDaemon"
$DAEMON_ABSOLUTE_PATH = (Get-Command "powershell.exe").Definition
$DAEMON_PARAMETER = "-ExecutionPolicy Bypass -File `"$PSScriptRoot\daemon.ps1`""
$RESULT_PATH = "$PSScriptRoot\LOGS\result.txt"
$STATUS_PATH = "$PSScriptRoot\LOGS\status.txt"
$STDOUT_PATH = "$PSScriptRoot\LOGS\stdout.txt"
$STDERR_PATH = "$PSScriptRoot\LOGS\stderr.txt"
# ====================================================

Write-Output "$env:PROJECT_NAME $env:VERSION"
if (-not (Test-Path "LOGS")) {
    mkdir LOGS
}
Get-ChildItem env:* | sort-object name > .\LOGS\monitorOnStartEnvs.log


$WrapperPath = "$PSScriptRoot\daemon_wrapper.cmd"
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
$DaemonDirectory = (get-item $DAEMON_ABSOLUTE_PATH).Directory.FullName

$wrapper = @"
pushd `"$DaemonDirectory`"
$DAEMON_ABSOLUTE_PATH $DAEMON_PARAMETER >>$STDOUT_PATH 2>>$STDERR_PATH
"@
[System.IO.File]::WriteAllLines($WrapperPath, $wrapper, $Utf8NoBomEncoding)


# using the parent folder name as the unique id
$taskId1 = (Get-Item $PSScriptRoot).Parent.Name
$taskId2 = (Get-Item $PSScriptRoot).Name
$TaskNameInstance = "{0}_{1}_instance" -f $taskId1, $taskId2
$TaskNameWatchdog = "{0}_{1}_watchdog" -f $taskId1, $taskId2

try {
    Register-ScheduledTaskVerifyOnce -TaskName $TaskNameInstance `
        -ExecutableAbsolutePath "$WrapperPath" -WorkingDirectory "$PSScriptRoot"
}
catch {
    $stderr = Get-Content $STDERR_PATH
    Add-Content -Path $STATUS_PATH -Value "FAIL" -Encoding UTF8
    $ReturnCode = $Error[0].TargetObject.ReturnCode
    $ErrorMsg = "Fail to launch $DAEMON_NAME, [Error$ReturnCode] $stderr"
    Add-Content -Path $RESULT_PATH -Value $ErrorMsg -Encoding UTF8
    exit 0
}


$powershell_path = (Get-Command "powershell.exe").Definition

try {
    Register-ScheduledTaskVerifyOnce -TaskName $TaskNameWatchdog `
        -ExecutableAbsolutePath $powershell_path `
        -Argument "-ExecutionPolicy Bypass -File $PSScriptRoot\daemonWatchdog.ps1" `
        -WorkingDirectory "$PSScriptRoot"
}
catch {
    $stderr = Get-Content $STDERR_PATH
    Add-Content -Path $STATUS_PATH -Value "FAIL" -Encoding UTF8
    $ReturnCode = $Error[0].TargetObject.ReturnCode
    $ErrorMsg = "Fail to launch watch dog for $DAEMON_NAME, [Error$ReturnCode] $stderr"
    Add-Content -Path $RESULT_PATH -Value $ErrorMsg -Encoding UTF8
}
