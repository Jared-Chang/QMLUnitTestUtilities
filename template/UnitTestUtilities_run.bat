@echo off
qmltestrunner %* | python highlighter.py
pause