@echo off

set FILENAME=keycatcher

g++ %FILENAME%.cpp -o %FILENAME%.exe -luser32 -lgdi32 -DLOGFILE >nul

if not exist .\bin mkdir .\bin >nul
move .\%FILENAME%.exe .\bin >nul