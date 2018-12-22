@echo off
rd /s /q "%~dp0dist\Ice"
powershell.exe -noexit -command "cd '%~dp0'; pyinstaller '%~dp0Ice.spec'"
pause