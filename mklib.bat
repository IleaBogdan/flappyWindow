@echo off

set FILENAME=testlib

g++ -shared -o libs\%FILENAME%.dll %FILENAME%.cpp -static-libgcc -static-libstdc++