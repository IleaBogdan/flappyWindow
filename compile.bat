@echo off

set EXENAME=keycatcher.exe

g++ keycatcher.cpp -o %EXENAME% -luser32 -lgdi32 -DLOGFILE >nul 2>&1

if not exist .\bin mkdir .\bin >nul 2>&1
move .\%EXENAME% .\bin >nul 2>&1