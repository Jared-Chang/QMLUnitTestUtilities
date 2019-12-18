@setlocal enableextensions enabledelayedexpansion
%echo off

set "input=%1"
set "filename=%~nx1"

if "x%input:tst_=%"=="x%input%" (
    FOR %%A in ("%input%") do (
        SET input=%%~dpAPATTERN%%~nxA
    )
) else (
    FOR %%A in ("%input%") do (
        SET input=%%~dpA..\\%filename:PREFIX=%
    )
)

%input%