@echo off
set proj_command=%1
set arg1=%2

set python2="$DBM_PYHTON_INSTALL_PATH$\python.exe"
if %python2:~1,4%==$DBM set python2="c:\python39_6\python.exe"

IF '%arg1%' NEQ 'app' goto cont

call %~dp0Development\get_app.bat
set arg1=%curapp%

:cont 

@%python2% "%~dp0..\manage.py" %proj_command% %arg1% %3 %4 %5 %6
echo off
echo.
IF '%nopause%'=='true' goto end
pause

:end
IF %ERRORLEVEL% NEQ 0 (
     exit /b %ERRORLEVEL%
)