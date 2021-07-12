@ECHO OFF
if [%1]==[] (set admins="") else (set admins=%1)
if [%2]==[] (set guests="") else (set guests=%2)
%~dp0..\run_command mapgroups --adminsgroup=%admins% --guestsgroup=%guests%