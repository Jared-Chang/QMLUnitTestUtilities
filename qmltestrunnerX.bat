@echo off
SET path=%PATH%;vast2
qmltestrunner -import "vast2" -plugins "vast2" %* | python %~dp0/highlighter.py
pause