cd %~dp0..\

:: imports exported CCenter files from selected directory to the database
:: argument - import_files_path (for ex. resources\import)

"%~dp0run_command" import %1 