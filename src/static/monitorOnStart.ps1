Write-Output "$env:PROJECT_NAME $env:VERSION $env:SOURCE_VERSION" > .\LOGS\_start.log
Get-ChildItem env:* | sort-object name > .\LOGS\envs.txt
