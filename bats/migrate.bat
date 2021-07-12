set install=%~1
if "%install%"=="install" ("%~dp0run_command" ccentermigrate) else ("%~dp0run_command" smart_migrate)