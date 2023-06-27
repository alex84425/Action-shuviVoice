Write-Output "$env:PROJECT_NAME $env:VERSION" > .\LOGS\_start.log
Get-ChildItem env:* | sort-object name > .\LOGS\_start_ps1_envs.txt
