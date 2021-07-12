@echo off

IF EXIST "C:\Program Files\dbMotion\Services\CCenter\Apache2" GOTO DELETEFOLDER
ECHO APACHE FOLDER DOSEN'T EXIST.
GOTO END



:DELETEFOLDER
del /q "C:\Program Files\dbMotion\Services\CCenter\Apache2\*"
FOR /D %%p IN ("C:\Program Files\dbMotion\Services\CCenter\Apache2\*.*") DO rmdir "%%p" /s /q
RMDIR "C:\Program Files\dbMotion\Services\CCenter\Apache2"
ECHO APACHE FOLDER DELETED SUCCESSFULLY.
GOTO END

:END