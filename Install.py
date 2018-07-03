import os
import _winreg
import re
import argparse
import shutil
import distutils.dir_util

QT_CREATOR_SETTING_EXTERNAL_TOOLS = "[ExternalTools]"
QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS = "[KeyboardShortcuts]"

TESTRUNNER_EXTERNAL_TOOLS = '''OverrideCategories\\testrunnerx\\size=2
OverrideCategories\\testrunnerx\\1\\Tool=qmltestrunnerx_autoFind
OverrideCategories\\testrunnerx\\2\\Tool=qmltestrunnerx'''

TESTRUNNER_SHORTCUT = '''Tools.External.qmltestrunnerx_autoFind=Ctrl+E
Tools.External.qmltestrunnerx=Ctrl+`
'''

TESTRUNNER_SCRIPT_FOR_AUTO_FIND = '''@setlocal enableextensions enabledelayedexpansion
@echo off

SET all_arg=%1

:lastarg
    set "last_arg=%1"
    shift
    if not "%2"=="" SET all_arg=%all_arg% %1
    if not "%1"=="" goto lastarg 

if "x%last_arg:tst_=%"=="x%last_arg%" (
    FOR %%A in ("%last_arg%") do (
        SET last_arg=%%~dpAUT\\tst_%%~nxA
    )
)

qmltestrunner %all_arg% %last_arg% | python highlighter.py
pause'''

TESTRUNNER_SCRIPT = '''@echo off
qmltestrunner %* | python highlighter.py
pause'''

TESTRUNNER_AUTO_FIND_QT_EXTERNAL_TOOL = '''<?xml version="1.0" encoding="UTF-8"?>
<externaltool id="qmltestrunnerx_autoFind">
    <description></description>
    <displayname>qmltestrunnerx_autoFind</displayname>
    <category></category>
    <executable output="ignore" error="ignore" modifiesdocument="yes">
        <path>C:/Windows/System32/cmd.exe</path>
        <arguments>/c start cmd.exe /c {qt_bin}\\qmltestrunnerx_autoFind.bat -input %{{CurrentDocument:FilePath}}</arguments>
        <workingdirectory>{qt_bin}</workingdirectory>
    </executable>
</externaltool>'''

TESTRUNNER_QT_EXTERNAL_TOOL = '''<?xml version="1.0" encoding="UTF-8"?>
<externaltool id="qmltestrunnerx">
    <description></description>
    <displayname>qmltestrunnerx</displayname>
    <category></category>
    <executable output="ignore" error="ignore" modifiesdocument="yes">
        <path>C:/Windows/System32/cmd.exe</path>
        <arguments>/c start cmd.exe /c {qt_bin}\\qmltestrunnerx.bat -input %{{CurrentDocument:FilePath}}</arguments>
        <workingdirectory>{qt_bin}</workingdirectory>
    </executable>
</externaltool>'''

def backup_qt_setting_file():
    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    shutil.copy2(qt_creator_setting_file_path, qt_creator_setting_file_path + ".bk")


def modify_qt_creator_settings_file():
    
    global QT_CREATOR_SETTING_EXTERNAL_TOOLS
    global QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS
    global TESTRUNNER_EXTERNAL_TOOLS
    global TESTRUNNER_SHORTCUT

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    setting_file = open(qt_creator_setting_file_path, "r")
    settings = setting_file.read()
    setting_file.close()

    external_tools_index = settings.find(QT_CREATOR_SETTING_EXTERNAL_TOOLS)
    if external_tools_index != -1:
        settings = settings[:external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS)] + "\n" + TESTRUNNER_EXTERNAL_TOOLS + settings[external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_EXTERNAL_TOOLS + "\n" + TESTRUNNER_EXTERNAL_TOOLS

    keyboard_shortcuts_index = settings.find(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)
    if keyboard_shortcuts_index != -1:
        settings = settings[:keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)] + "\n" + TESTRUNNER_SHORTCUT + settings[keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS + "\n" + TESTRUNNER_SHORTCUT

    setting_file = open(qt_creator_setting_file_path, "w")
    setting_file.write(settings)
    setting_file.close()


def create_external_tools(qt_path):
    
    global TESTRUNNER_QT_EXTERNAL_TOOL
    global TESTRUNNER_AUTO_FIND_QT_EXTERNAL_TOOL

    qt_creator_setting_path = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools"

    f = open(qt_creator_setting_path + "\\qmltestrunnerx.xml", "w+")
    content = TESTRUNNER_QT_EXTERNAL_TOOL.format(qt_bin = qt_path)
    f.write(content)
    f.close()

    f = open(qt_creator_setting_path + "\\qmltestrunnerx_autoFind.xml", "w+")
    content = TESTRUNNER_AUTO_FIND_QT_EXTERNAL_TOOL.format(qt_bin = qt_path)
    f.write(content)
    f.close()


def create_testrunner_scripts(qt_path):

    global TESTRUNNER_SCRIPT_FOR_AUTO_FIND

    f = open(qt_path + "\\qmltestrunnerX_autoFind.bat", "w+")
    f.write(TESTRUNNER_SCRIPT_FOR_AUTO_FIND)
    f.close()

    f = open(qt_path + "\\qmltestrunnerX.bat", "w+")
    f.write(TESTRUNNER_SCRIPT)
    f.close()


def copy_file_to_qt_path(qt_path):

    shutil.copy2(".\\highlighter.py", qt_path)
    distutils.dir_util.copy_tree(".\\ansiconx64", qt_path + "\\ansiconx64")


def copy_file_to_qt_creator():

    qt_creator_setting_path = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools"

    if not os.path.exists(qt_creator_setting_path):
        os.makedirs(qt_creator_setting_path)


def install(qt_path):

    backup_qt_setting_file()
    modify_qt_creator_settings_file()
    copy_file_to_qt_path(qt_path)
    create_testrunner_scripts(qt_path)
    copy_file_to_qt_creator()
    create_external_tools(qt_path)


def remove_qt_creator_settings():

    global TESTRUNNER_EXTERNAL_TOOLS
    global TESTRUNNER_SHORTCUT

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    setting_file = open(qt_creator_setting_file_path, "r")

    content = ''

    for line in setting_file.readlines():
        not_contain_testrunnerx = line.find('testrunnerx') == -1
        if not_contain_testrunnerx:
            content += line

    setting_file.close()
            
    setting_file = open(qt_creator_setting_file_path, "w")
    setting_file.write(content)
    setting_file.close()


def remove_script_and_binary(qt_path):

    shutil.rmtree(qt_path + '\\ansiconx64')
    os.remove(qt_path + '\\qmltestrunnerX_autoFind.bat')
    os.remove(qt_path + '\\qmltestrunnerX.bat')
    os.remove(qt_path + '\\highlighter.py')


def remove_external_tools():

    qt_creator_setting_path = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools\\"

    os.remove(qt_creator_setting_path + "\\qmltestrunnerx.xml")
    os.remove(qt_creator_setting_path + "\\qmltestrunnerx_autoFind.xml")


def uninstall(qt_path):

    backup_qt_setting_file()
    remove_qt_creator_settings()
    remove_script_and_binary(qt_path)
    remove_external_tools()


def main():
    parser = argparse.ArgumentParser(description='Install QtCreator QmlTestrunnerUtililty')
    
    parser.add_argument('qt_path', help='qt/msvc2017/bin')
    parser.add_argument('--uninstall', '-u', action='store_true')
    
    args = parser.parse_args()

    if args.uninstall:
        uninstall(args.qt_path)
    else:
        install(args.qt_path)


if __name__ == "__main__":
    main()
