chcp 65001
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%getadmin.vbs" del "%temp%getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || ( echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%getadmin.vbs" && "%temp%getadmin.vbs" && exit /B )
timeout 2

pushd %~dp0
mkdir LOGS
call :LAUNCH >> LOGS\batch.log 2>&1
popd
exit

:LAUNCH
set > .\LOGS\_start_cmd_envs.txt
@powershell -NoProfile (Get-WmiObject Win32_Process -Filter ProcessId=$PID).ParentProcessId > PID.txt
@powershell -NoProfile -ExecutionPolicy Bypass -f "%~dp0monitorOnStart.ps1"
