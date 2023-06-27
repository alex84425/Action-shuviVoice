Write-Output "$env:PROJECT_NAME $env:VERSION" > .\LOGS\_stop.log
Get-ChildItem env:* | sort-object name > .\LOGS\_stop_ps1_envs.txt
