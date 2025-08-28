@echo off

set FILENAME=keycatcher

g++ %FILENAME%.cpp -o %FILENAME%.exe -luser32 -lgdi32 -DLOGFILE >nul 2>&1

if not exist .\bin mkdir .\bin >nul 2>&1
move .\%FILENAME%.exe .\bin >nul 2>&1