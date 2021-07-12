cd %~dp0..\

:: Running upgrade migration from previous major version.
:: 1. With argument: backward_to_ga - indicates to to check the existing migrations and run backward migration if required.
:: 2. With argument: version_update - to complete normal forward migration and write the last migration to a file
::
:: * If calling with %1==check_db then nothing will be performed if the database is not ready for upgrade.
::   In that case it is expected the OOB PP will run Initial CCenter Database command.
::	 The check_db option should be used on clean installation on CCenter role, to support clean upgrade.

:: "%~dp0run_command" backward_to_ga %1
:: IF %ERRORLEVEL% NEQ 0 (
::      exit /b %ERRORLEVEL%
:: )
:: "%~dp0run_command" version_update %1