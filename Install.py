import os
import winreg
import re
import argparse
import shutil
import distutils.dir_util

QT_CREATOR_SETTING_EXTERNAL_TOOLS = "[ExternalTools]"
QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS = "[KeyboardShortcuts]"
TOOL_PREFIX = "UnitTestUtilities"

def create_tool(name, shortcut, command):
    global TOOL_PREFIX
    return {'name': TOOL_PREFIX + "_" + name, 'shortcut': shortcut, 'command': command}

tools = [
    create_tool(
        name = 'autoFindAndRun', 
        shortcut = 'Ctrl+E', 
        command = '/c start cmd.exe /c {script_path}\\UnitTestUtilities_autoFindAndRun.bat {imports} -input %{{CurrentDocument:FilePath}}'),

    create_tool(
        name = 'run', 
        shortcut = 'Ctrl+`', 
        command = '/c start cmd.exe /c {script_path}\\UnitTestUtilities_run.bat {imports} -input %{{CurrentDocument:FilePath}}'),

    create_tool(
        name = 'toggleFile', 
        shortcut = 'Ctrl+~', 
        command = '/c {script_path}\\UnitTestUtilities_toggleFile.bat %{{CurrentDocument:FilePath}}')
    ]

def backup_qt_setting_file():
    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    shutil.copy2(qt_creator_setting_file_path, qt_creator_setting_file_path + ".bk")


def generate_external_tool_settings():
    global tools
    global TOOL_PREFIX

    settings_title = 'OverrideCategories\\{tool_prefix}\\size={size}\n'
    settings = 'OverrideCategories\\{tool_prefix}\\{index}\\Tool={name}\n'

    result = settings_title.format(size = len(tools), tool_prefix = TOOL_PREFIX)

    for index in range(1, len(tools) + 1):
        result += settings.format(index = index, name = tools[index-1]['name'], tool_prefix = TOOL_PREFIX)

    return result


def generate_shortcuts():
    global tools

    shortcut = 'Tools.External.{name}={shortcut}\n'

    result = ''

    for tool in tools:
        result += shortcut.format(name = tool['name'], shortcut = tool['shortcut'])

    return result


def modify_qt_creator_settings_file():
    
    global QT_CREATOR_SETTING_EXTERNAL_TOOLS
    global QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"

    settings = ''

    with open(qt_creator_setting_file_path, "r") as setting_file:
        settings = setting_file.read()

    external_tool_settings = generate_external_tool_settings()
    external_tools_index = settings.find(QT_CREATOR_SETTING_EXTERNAL_TOOLS)
    if external_tools_index != -1:
        settings = settings[:external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS)] + "\n" + external_tool_settings + settings[external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_EXTERNAL_TOOLS + "\n" + external_tool_settings

    shortcuts = generate_shortcuts()
    keyboard_shortcuts_index = settings.find(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)
    if keyboard_shortcuts_index != -1:
        settings = settings[:keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)] + "\n" + shortcuts + settings[keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS + "\n" + shortcuts


    with open(qt_creator_setting_file_path, "w") as setting_file:
        setting_file.write(settings)


def generate_external_tools_xml(tool, bin, imports, installer_path):

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<externaltool id="{name}">
    <description></description>
    <displayname>{name}</displayname>
    <category></category>
    <executable output="ignore" error="ignore" modifiesdocument="yes">
        <path>C:/Windows/System32/cmd.exe</path>
        <arguments>{command}</arguments>
        <workingdirectory>{bin}</workingdirectory>
    </executable>
</externaltool>'''

    command = tool['command'].format(script_path = installer_path + "\\bin", imports = imports)

    return xml.format(name = tool['name'], command = command, bin = bin)

def create_external_tools(bin, imports, installer_path):
    
    global tools

    imports = ' '.join(['-import {import_path}'.format(import_path=import_path) for import_path in imports])

    qt_creator_setting_path_pattern = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools\\{name}.xml"

    for tool in tools:
        with open(qt_creator_setting_path_pattern.format(name = tool['name']), "w+") as f:
            f.write(generate_external_tools_xml(tool, bin, imports, installer_path))


def create_scripts(installer_path, pattern, prefix):

    global tools

    template_path = installer_path + '\\template\\{name}.bat'
    output_path = installer_path + '\\bin\\{name}.bat'

    for tool in tools:

        content = ''
        with open(template_path.format(name = tool['name']), "r") as template:
            content = template.read()

        content = re.sub(r"PATTERN\b", pattern, content)
        content = re.sub(r"PREFIX\b", prefix, content)

        with open(output_path.format(name = tool['name']), "w+") as output:
            output.write(content)


def remove_qt_creator_settings():

    global TOOL_PREFIX

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    
    with open(qt_creator_setting_file_path, "r") as setting_file:
        content = ''

        for line in setting_file.readlines():
            if line.find(TOOL_PREFIX) == -1:
                content += line
            
    with open(qt_creator_setting_file_path, "w") as setting_file:
        setting_file.write(content)


def remove_external_tools():

    global tools

    qt_creator_setting_path_pattern = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools\\{name}.xml"

    for tool in tools:
        if os.path.exists(qt_creator_setting_path_pattern.format(name = tool['name'])):
            os.remove(qt_creator_setting_path_pattern.format(name = tool['name']))


def install(bin, imports, installer_path, pattern, prefix):

    backup_qt_setting_file()
    modify_qt_creator_settings_file()
    create_scripts(installer_path, pattern, prefix)
    create_external_tools(bin, imports, installer_path)


def uninstall():

    backup_qt_setting_file()
    remove_qt_creator_settings()
    remove_external_tools()


def main():
    parser = argparse.ArgumentParser(description='Install QtCreator Qml Unit Test Utility')
    
    parser.add_argument('--bin', '-b', default="", help='QT binary folder')
    parser.add_argument('--import_path', '-m', default="", action='append', help='Import path')
    parser.add_argument('--pattern', '-p', default=r"UT\\\\tst_", help='Unit test file path pattern, if your source file is a/b/c.qml then unit test is a/b/c/d/test_c.qml, pattern is d/test_')
    parser.add_argument('--prefix', '-x', default="tst_", help='Unit test file prefix, e.g. prefix of test_c.qml is test_, due to source file is c.qml')
    parser.add_argument('--uninstall', '-u', action='store_true')

    args = parser.parse_args()

    installer_path = os.path.dirname(os.path.abspath(__file__))

    if args.uninstall:
        uninstall()
    else:
        install(args.bin, args.import_path, installer_path, args.pattern, args.prefix)


if __name__ == "__main__":
    main()
