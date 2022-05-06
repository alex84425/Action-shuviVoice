@echo off
echo Please input the new action name (title case, [a-zA-Z], no space)
echo example: MyAction
echo.
set /p ActionName=New Action Name: 


set file=docker-compose.yml
powershell -command "$action_name = '%ActionName%'.ToLower(); (Get-Content %file%) -Replace 'executortemplate', $action_name | Set-Content %file%"

set file=src\app\config.py
powershell -command "$action_name = '%ActionName%'; (Get-Content %file%) -Replace 'ExecutorTemplate', $action_name | Set-Content %file%"
pause