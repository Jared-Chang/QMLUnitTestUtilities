@setlocal enableextensions enabledelayedexpansion
@echo off

SET all_arg=%1

:lastarg
    set "last_arg=%1"
    shift
    if not "%2"=="" SET all_arg=%all_arg% %1
    if not "%1"=="" goto lastarg 

if "x%last_arg:tst_=%"=="x%last_arg%" (
    FOR %%A in ("%last_arg%") do (
        SET last_arg=%%~dpAPATTERN%%~nxA
    )
)

qmltestrunner %all_arg% %last_arg% | python highlighter.py
pause